from typing import Dict, Any, List
import pandas as pd
from loguru import logger

class DataTransformer:
    """数据转换类"""
    
    @staticmethod
    def to_dataframe(data: List[Dict[str, Any]]) -> Dict[str, pd.DataFrame]:
        """
        将数据转换为DataFrame格式
        
        Args:
            data: 原始数据列表
            
        Returns:
            包含多个DataFrame的字典
        """
        try:
            # 创建空的DataFrame
            awards_df = pd.DataFrame()
            projects_df = pd.DataFrame()
            winners_df = pd.DataFrame()
            
            # 处理每条数据
            for item in data:
                try:
                    # 提取奖项基本信息
                    award_info = {
                        'title': item.get('title'),
                        'content': item.get('content'),
                        'year': item.get('year'),
                        'award_level': item.get('award_level'),
                        'award_type': item.get('award_type'),
                        'source_url': item.get('source_url'),
                        'source_title': item.get('source_title'),
                        'source_engine': item.get('source_engine'),
                        'crawled_at': item.get('crawled_at')
                    }
                    awards_df = pd.concat([awards_df, pd.DataFrame([award_info])], ignore_index=True)
                    
                    # 处理项目信息
                    for project in item.get('projects', []):
                        project_info = {
                            'award_title': item.get('title'),
                            'year': item.get('year'),
                            'name': project.get('name'),
                            'organization': project.get('organization'),
                            'level': project.get('level')
                        }
                        projects_df = pd.concat([projects_df, pd.DataFrame([project_info])], ignore_index=True)
                        
                        # 处理获奖人信息
                        for winner in project.get('winners', []):
                            winner_info = {
                                'project_name': project.get('name'),
                                'name': winner.get('name'),
                                'organization': winner.get('organization')
                            }
                            winners_df = pd.concat([winners_df, pd.DataFrame([winner_info])], ignore_index=True)
                            
                except Exception as e:
                    logger.error(f"转换单条数据失败: {str(e)}")
                    continue
            
            return {
                'awards': awards_df,
                'projects': projects_df,
                'winners': winners_df
            }
            
        except Exception as e:
            logger.error(f"数据转换失败: {str(e)}")
            return {
                'awards': pd.DataFrame(),
                'projects': pd.DataFrame(),
                'winners': pd.DataFrame()
            }
    
    @staticmethod
    def to_excel(data: Dict[str, pd.DataFrame], output_file: str):
        """
        将数据保存为Excel文件
        
        Args:
            data: DataFrame字典
            output_file: 输出文件路径
        """
        try:
            with pd.ExcelWriter(output_file) as writer:
                for sheet_name, df in data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            logger.info(f"数据已保存到Excel文件: {output_file}")
            
        except Exception as e:
            logger.error(f"保存Excel文件失败: {str(e)}")
    
    @staticmethod
    def to_csv(data: Dict[str, pd.DataFrame], output_dir: str):
        """
        将数据保存为CSV文件
        
        Args:
            data: DataFrame字典
            output_dir: 输出目录
        """
        try:
            for name, df in data.items():
                output_file = f"{output_dir}/{name}.csv"
                df.to_csv(output_file, index=False, encoding='utf-8')
                logger.info(f"数据已保存到CSV文件: {output_file}")
                
        except Exception as e:
            logger.error(f"保存CSV文件失败: {str(e)}")
    
    @staticmethod
    def merge_dataframes(dfs: List[Dict[str, pd.DataFrame]]) -> Dict[str, pd.DataFrame]:
        """
        合并多个DataFrame字典
        
        Args:
            dfs: DataFrame字典列表
            
        Returns:
            合并后的DataFrame字典
        """
        try:
            result = {}
            
            # 获取所有可能的键
            keys = set()
            for df_dict in dfs:
                keys.update(df_dict.keys())
            
            # 合并每个键对应的DataFrame
            for key in keys:
                frames = [df_dict[key] for df_dict in dfs if key in df_dict]
                if frames:
                    result[key] = pd.concat(frames, ignore_index=True)
                else:
                    result[key] = pd.DataFrame()
            
            return result
            
        except Exception as e:
            logger.error(f"合并DataFrame失败: {str(e)}")
            return {} 