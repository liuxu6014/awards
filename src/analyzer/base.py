from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from loguru import logger

class BaseAnalyzer:
    """数据分析基类"""
    
    def __init__(self, data: Dict[str, pd.DataFrame]):
        """
        初始化分析器
        
        Args:
            data: 包含多个DataFrame的字典
        """
        self.awards_df = data.get('awards', pd.DataFrame())
        self.projects_df = data.get('projects', pd.DataFrame())
        self.winners_df = data.get('winners', pd.DataFrame())
        
    def get_basic_stats(self) -> Dict[str, Any]:
        """
        获取基础统计信息
        
        Returns:
            统计信息字典
        """
        try:
            stats = {
                'total_awards': len(self.awards_df),
                'total_projects': len(self.projects_df),
                'total_winners': len(self.winners_df),
                'year_range': self._get_year_range(),
                'award_types': self._get_award_types(),
                'award_levels': self._get_award_levels()
            }
            return stats
            
        except Exception as e:
            logger.error(f"获取基础统计信息失败: {str(e)}")
            return {}
    
    def get_yearly_stats(self) -> pd.DataFrame:
        """
        获取年度统计信息
        
        Returns:
            年度统计DataFrame
        """
        try:
            yearly_stats = self.awards_df.groupby('year').agg({
                'award_type': 'count',
                'award_level': lambda x: x.value_counts().to_dict()
            }).reset_index()
            
            yearly_stats.columns = ['年份', '奖项数量', '等级分布']
            return yearly_stats
            
        except Exception as e:
            logger.error(f"获取年度统计信息失败: {str(e)}")
            return pd.DataFrame()
    
    def get_type_stats(self) -> pd.DataFrame:
        """
        获取奖项类型统计信息
        
        Returns:
            类型统计DataFrame
        """
        try:
            type_stats = self.awards_df.groupby('award_type').agg({
                'year': 'count',
                'award_level': lambda x: x.value_counts().to_dict()
            }).reset_index()
            
            type_stats.columns = ['奖项类型', '数量', '等级分布']
            return type_stats
            
        except Exception as e:
            logger.error(f"获取奖项类型统计信息失败: {str(e)}")
            return pd.DataFrame()
    
    def get_organization_stats(self, top_n: int = 10) -> pd.DataFrame:
        """
        获取机构统计信息
        
        Args:
            top_n: 返回前N个机构
            
        Returns:
            机构统计DataFrame
        """
        try:
            # 合并项目和获奖人的机构
            org_stats = pd.concat([
                self.projects_df['organization'].value_counts(),
                self.winners_df['organization'].value_counts()
            ]).groupby(level=0).sum()
            
            # 获取前N个机构
            org_stats = org_stats.nlargest(top_n).reset_index()
            org_stats.columns = ['机构名称', '获奖次数']
            
            return org_stats
            
        except Exception as e:
            logger.error(f"获取机构统计信息失败: {str(e)}")
            return pd.DataFrame()
    
    def get_winner_stats(self, top_n: int = 10) -> pd.DataFrame:
        """
        获取获奖人统计信息
        
        Args:
            top_n: 返回前N个获奖人
            
        Returns:
            获奖人统计DataFrame
        """
        try:
            winner_stats = self.winners_df['name'].value_counts().nlargest(top_n).reset_index()
            winner_stats.columns = ['获奖人', '获奖次数']
            
            # 添加最近获奖机构
            winner_stats['最近获奖机构'] = winner_stats['获奖人'].map(
                lambda x: self.winners_df[self.winners_df['name'] == x]['organization'].iloc[-1]
                if len(self.winners_df[self.winners_df['name'] == x]) > 0 else None
            )
            
            return winner_stats
            
        except Exception as e:
            logger.error(f"获取获奖人统计信息失败: {str(e)}")
            return pd.DataFrame()
    
    def _get_year_range(self) -> Dict[str, int]:
        """获取年份范围"""
        try:
            if len(self.awards_df) > 0:
                return {
                    'min_year': self.awards_df['year'].min(),
                    'max_year': self.awards_df['year'].max()
                }
            return {'min_year': None, 'max_year': None}
            
        except Exception:
            return {'min_year': None, 'max_year': None}
    
    def _get_award_types(self) -> Dict[str, int]:
        """获取奖项类型分布"""
        try:
            if len(self.awards_df) > 0:
                return self.awards_df['award_type'].value_counts().to_dict()
            return {}
            
        except Exception:
            return {}
    
    def _get_award_levels(self) -> Dict[str, int]:
        """获取奖项等级分布"""
        try:
            if len(self.awards_df) > 0:
                return self.awards_df['award_level'].value_counts().to_dict()
            return {}
            
        except Exception:
            return {} 