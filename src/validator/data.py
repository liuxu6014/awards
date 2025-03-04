from typing import Dict, Any, List, Tuple
import re
from datetime import datetime
from loguru import logger
import pandas as pd
import numpy as np

from config.config import (
    AWARD_LEVELS,
    AWARD_TYPES,
    MIN_TEXT_LENGTH,
    MAX_TEXT_LENGTH
)

class DataValidator:
    """数据验证类"""
    
    @staticmethod
    def validate_text(text: str, field_name: str, min_length: int = MIN_TEXT_LENGTH,
                     max_length: int = MAX_TEXT_LENGTH) -> Tuple[bool, List[str]]:
        """
        验证文本字段
        
        Args:
            text: 文本内容
            field_name: 字段名称
            min_length: 最小长度
            max_length: 最大长度
            
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        
        if not text:
            errors.append(f"{field_name}不能为空")
            return False, errors
        
        if len(text) < min_length:
            errors.append(f"{field_name}长度不能小于{min_length}个字符")
            
        if len(text) > max_length:
            errors.append(f"{field_name}长度不能大于{max_length}个字符")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, List[str]]:
        """
        验证URL
        
        Args:
            url: URL字符串
            
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        
        if not url:
            errors.append("URL不能为空")
            return False, errors
        
        # 验证URL格式
        if not re.match(r'^https?://', url):
            errors.append("URL格式无效")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_year(year: int) -> Tuple[bool, List[str]]:
        """
        验证年份
        
        Args:
            year: 年份
            
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        
        if not year:
            errors.append("年份不能为空")
            return False, errors
        
        current_year = datetime.now().year
        
        if not (2010 <= year <= current_year):
            errors.append(f"年份必须在2010到{current_year}之间")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_award_level(level: str) -> Tuple[bool, List[str]]:
        """
        验证奖项等级
        
        Args:
            level: 奖项等级
            
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        
        if not level:
            errors.append("奖项等级不能为空")
            return False, errors
        
        if level not in AWARD_LEVELS:
            errors.append(f"奖项等级必须是以下之一: {', '.join(AWARD_LEVELS)}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_award_type(award_type: str) -> Tuple[bool, List[str]]:
        """
        验证奖项类型
        
        Args:
            award_type: 奖项类型
            
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        
        if not award_type:
            errors.append("奖项类型不能为空")
            return False, errors
        
        if award_type not in AWARD_TYPES:
            errors.append(f"奖项类型必须是以下之一: {', '.join(AWARD_TYPES)}")
        
        return len(errors) == 0, errors
    
    def evaluate_data_quality(self, data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        评估数据质量
        
        Args:
            data: 包含多个DataFrame的字典
            
        Returns:
            数据质量评估结果
        """
        try:
            quality_metrics = {
                'completeness': self._evaluate_completeness(data),
                'accuracy': self._evaluate_accuracy(data),
                'consistency': self._evaluate_consistency(data),
                'timeliness': self._evaluate_timeliness(data),
                'overall_score': 0.0
            }
            
            # 计算总体得分
            weights = {
                'completeness': 0.3,
                'accuracy': 0.3,
                'consistency': 0.2,
                'timeliness': 0.2
            }
            
            quality_metrics['overall_score'] = sum(
                quality_metrics[metric]['score'] * weights[metric]
                for metric in weights.keys()
            )
            
            return quality_metrics
            
        except Exception as e:
            logger.error(f"评估数据质量失败: {str(e)}")
            return {}

    def _evaluate_completeness(self, data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """评估数据完整性"""
        try:
            completeness = {
                'score': 0.0,
                'details': {},
                'issues': []
            }
            
            for name, df in data.items():
                # 计算非空值比例
                non_null_ratio = 1 - df.isnull().sum() / len(df)
                avg_completeness = non_null_ratio.mean()
                
                # 记录详细信息
                completeness['details'][name] = {
                    'total_rows': len(df),
                    'non_null_ratio': non_null_ratio.to_dict(),
                    'score': avg_completeness
                }
                
                # 记录问题字段
                for col, ratio in non_null_ratio.items():
                    if ratio < 0.9:  # 非空率低于90%
                        completeness['issues'].append(
                            f"{name}表中{col}字段的完整性为{ratio:.1%}"
                        )
            
            # 计算总体完整性得分
            completeness['score'] = np.mean([
                details['score'] for details in completeness['details'].values()
            ])
            
            return completeness
            
        except Exception as e:
            logger.error(f"评估数据完整性失败: {str(e)}")
            return {'score': 0.0, 'details': {}, 'issues': [str(e)]}

    def _evaluate_accuracy(self, data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """评估数据准确性"""
        try:
            accuracy = {
                'score': 0.0,
                'details': {},
                'issues': []
            }
            
            for name, df in data.items():
                field_scores = {}
                
                # 检查年份字段
                if 'year' in df.columns:
                    valid_years = df['year'].between(1990, datetime.now().year)
                    field_scores['year'] = valid_years.mean()
                    if field_scores['year'] < 1:
                        accuracy['issues'].append(
                            f"{name}表中存在{(~valid_years).sum()}个无效年份"
                        )
                
                # 检查奖项等级
                if 'award_level' in df.columns:
                    valid_levels = df['award_level'].isin(AWARD_LEVELS)
                    field_scores['award_level'] = valid_levels.mean()
                    if field_scores['award_level'] < 1:
                        accuracy['issues'].append(
                            f"{name}表中存在{(~valid_levels).sum()}个无效奖项等级"
                        )
                
                # 检查奖项类型
                if 'award_type' in df.columns:
                    valid_types = df['award_type'].isin(AWARD_TYPES)
                    field_scores['award_type'] = valid_types.mean()
                    if field_scores['award_type'] < 1:
                        accuracy['issues'].append(
                            f"{name}表中存在{(~valid_types).sum()}个无效奖项类型"
                        )
                
                # 记录详细信息
                accuracy['details'][name] = {
                    'field_scores': field_scores,
                    'score': np.mean(list(field_scores.values())) if field_scores else 1.0
                }
            
            # 计算总体准确性得分
            accuracy['score'] = np.mean([
                details['score'] for details in accuracy['details'].values()
            ])
            
            return accuracy
            
        except Exception as e:
            logger.error(f"评估数据准确性失败: {str(e)}")
            return {'score': 0.0, 'details': {}, 'issues': [str(e)]}

    def _evaluate_consistency(self, data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """评估数据一致性"""
        try:
            consistency = {
                'score': 0.0,
                'details': {},
                'issues': []
            }
            
            # 检查项目和获奖人的关联一致性
            if 'projects' in data and 'winners' in data:
                projects_df = data['projects']
                winners_df = data['winners']
                
                # 检查获奖人关联的项目是否存在
                valid_projects = winners_df['project_name'].isin(projects_df['name'])
                project_consistency = valid_projects.mean()
                
                consistency['details']['project_winner_relation'] = {
                    'score': project_consistency,
                    'invalid_count': (~valid_projects).sum()
                }
                
                if project_consistency < 1:
                    consistency['issues'].append(
                        f"存在{(~valid_projects).sum()}个获奖人关联了不存在的项目"
                    )
            
            # 检查奖项和项目的关联一致性
            if 'awards' in data and 'projects' in data:
                awards_df = data['awards']
                projects_df = data['projects']
                
                # 检查项目关联的奖项是否存在
                valid_awards = projects_df['award_title'].isin(awards_df['title'])
                award_consistency = valid_awards.mean()
                
                consistency['details']['award_project_relation'] = {
                    'score': award_consistency,
                    'invalid_count': (~valid_awards).sum()
                }
                
                if award_consistency < 1:
                    consistency['issues'].append(
                        f"存在{(~valid_awards).sum()}个项目关联了不存在的奖项"
                    )
            
            # 计算总体一致性得分
            consistency['score'] = np.mean([
                details['score'] for details in consistency['details'].values()
            ])
            
            return consistency
            
        except Exception as e:
            logger.error(f"评估数据一致性失败: {str(e)}")
            return {'score': 0.0, 'details': {}, 'issues': [str(e)]}

    def _evaluate_timeliness(self, data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """评估数据时效性"""
        try:
            timeliness = {
                'score': 0.0,
                'details': {},
                'issues': []
            }
            
            current_year = datetime.now().year
            
            for name, df in data.items():
                if 'year' in df.columns:
                    # 计算数据的年份分布
                    year_stats = {
                        'min_year': df['year'].min(),
                        'max_year': df['year'].max(),
                        'mean_year': df['year'].mean(),
                        'recent_years_ratio': (df['year'] >= current_year - 5).mean()
                    }
                    
                    # 计算时效性得分
                    # 1. 最新数据权重：0.4
                    # 2. 数据跨度权重：0.3
                    # 3. 近5年数据比例权重：0.3
                    latest_score = 1 - (current_year - year_stats['max_year']) / 10
                    span_score = (year_stats['max_year'] - year_stats['min_year']) / 30
                    recent_score = year_stats['recent_years_ratio']
                    
                    score = 0.4 * latest_score + 0.3 * span_score + 0.3 * recent_score
                    
                    timeliness['details'][name] = {
                        'year_stats': year_stats,
                        'score': score
                    }
                    
                    # 记录时效性问题
                    if year_stats['max_year'] < current_year - 2:
                        timeliness['issues'].append(
                            f"{name}表最新数据为{year_stats['max_year']}年，可能需要更新"
                        )
            
            # 计算总体时效性得分
            timeliness['score'] = np.mean([
                details['score'] for details in timeliness['details'].values()
            ])
            
            return timeliness
            
        except Exception as e:
            logger.error(f"评估数据时效性失败: {str(e)}")
            return {'score': 0.0, 'details': {}, 'issues': [str(e)]} 