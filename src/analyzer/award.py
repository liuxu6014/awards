from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
import os
import json
from loguru import logger
import networkx as nx

from .base import BaseAnalyzer

class AwardAnalyzer(BaseAnalyzer):
    """奖项分析器"""
    
    def __init__(self, data: Dict[str, pd.DataFrame] = None):
        """
        初始化分析器
        
        Args:
            data: 包含多个DataFrame的字典，可选
        """
        if data is None:
            data = {
                'awards': pd.DataFrame(),
                'projects': pd.DataFrame(),
                'winners': pd.DataFrame()
            }
        super().__init__(data)
        self.results = {}
    
    def load_data(self, excel_path: str) -> None:
        """
        从Excel文件加载数据
        
        Args:
            excel_path: Excel文件路径
        """
        try:
            logger.info(f"从Excel文件加载数据: {excel_path}")
            
            # 读取Excel文件中的所有sheet
            data = {}
            with pd.ExcelFile(excel_path) as xls:
                for sheet_name in xls.sheet_names:
                    data[sheet_name] = pd.read_excel(xls, sheet_name)
            
            # 更新DataFrame
            self.awards_df = data.get('awards', pd.DataFrame())
            self.projects_df = data.get('projects', pd.DataFrame())
            self.winners_df = data.get('winners', pd.DataFrame())
            
            logger.info(f"数据加载成功: {len(self.awards_df)} 条奖项, {len(self.projects_df)} 个项目, {len(self.winners_df)} 名获奖人")
            
        except Exception as e:
            logger.error(f"加载数据失败: {str(e)}")
    
    def load_results(self, results_dir: str) -> None:
        """
        从结果目录加载分析结果
        
        Args:
            results_dir: 结果目录路径
        """
        try:
            logger.info(f"从结果目录加载分析结果: {results_dir}")
            
            # 加载基础统计信息
            stats_path = os.path.join(results_dir, "basic_stats.json")
            if os.path.exists(stats_path):
                with open(stats_path, 'r', encoding='utf-8') as f:
                    self.results['basic_stats'] = json.load(f)
            
            # 加载年度统计信息
            yearly_path = os.path.join(results_dir, "yearly_stats.csv")
            if os.path.exists(yearly_path):
                self.results['yearly_stats'] = pd.read_csv(yearly_path)
            
            # 加载类型统计信息
            type_path = os.path.join(results_dir, "type_stats.csv")
            if os.path.exists(type_path):
                self.results['type_stats'] = pd.read_csv(type_path)
            
            # 加载机构统计信息
            org_path = os.path.join(results_dir, "organization_stats.csv")
            if os.path.exists(org_path):
                self.results['organization_stats'] = pd.read_csv(org_path)
            
            # 加载获奖人统计信息
            winner_path = os.path.join(results_dir, "winner_stats.csv")
            if os.path.exists(winner_path):
                self.results['winner_stats'] = pd.read_csv(winner_path)
            
            logger.info(f"分析结果加载成功")
            
        except Exception as e:
            logger.error(f"加载分析结果失败: {str(e)}")
    
    def analyze(self) -> None:
        """
        执行分析
        """
        try:
            logger.info("开始执行分析")
            
            # 执行各种分析
            self.results['basic_stats'] = self.get_basic_stats()
            self.results['yearly_stats'] = self.get_yearly_stats()
            self.results['type_stats'] = self.get_type_stats()
            self.results['organization_stats'] = self.get_organization_stats()
            self.results['winner_stats'] = self.get_winner_stats()
            self.results['trend_analysis'] = self.get_trend_analysis()
            self.results['regional_analysis'] = self.get_regional_analysis()
            self.results['collaboration_analysis'] = self.get_collaboration_analysis()
            self.results['field_analysis'] = self.get_field_analysis()
            self.results['impact_analysis'] = self.get_impact_analysis()
            
            logger.info("分析完成")
            
        except Exception as e:
            logger.error(f"执行分析失败: {str(e)}")
    
    def save_results(self, output_dir: str) -> None:
        """
        保存分析结果
        
        Args:
            output_dir: 输出目录
        """
        try:
            logger.info(f"保存分析结果到: {output_dir}")
            
            # 保存基础统计信息
            stats_path = os.path.join(output_dir, "basic_stats.json")
            with open(stats_path, 'w', encoding='utf-8') as f:
                json.dump(self.results.get('basic_stats', {}), f, ensure_ascii=False, indent=2)
            
            # 保存年度统计信息
            yearly_stats = self.results.get('yearly_stats')
            if isinstance(yearly_stats, pd.DataFrame) and not yearly_stats.empty:
                yearly_path = os.path.join(output_dir, "yearly_stats.csv")
                yearly_stats.to_csv(yearly_path, index=False, encoding='utf-8')
            
            # 保存类型统计信息
            type_stats = self.results.get('type_stats')
            if isinstance(type_stats, pd.DataFrame) and not type_stats.empty:
                type_path = os.path.join(output_dir, "type_stats.csv")
                type_stats.to_csv(type_path, index=False, encoding='utf-8')
            
            # 保存机构统计信息
            org_stats = self.results.get('organization_stats')
            if isinstance(org_stats, pd.DataFrame) and not org_stats.empty:
                org_path = os.path.join(output_dir, "organization_stats.csv")
                org_stats.to_csv(org_path, index=False, encoding='utf-8')
            
            # 保存获奖人统计信息
            winner_stats = self.results.get('winner_stats')
            if isinstance(winner_stats, pd.DataFrame) and not winner_stats.empty:
                winner_path = os.path.join(output_dir, "winner_stats.csv")
                winner_stats.to_csv(winner_path, index=False, encoding='utf-8')
            
            logger.info(f"分析结果保存成功")
            
        except Exception as e:
            logger.error(f"保存分析结果失败: {str(e)}")
    
    def get_trend_analysis(self) -> Dict[str, pd.DataFrame]:
        """
        获取趋势分析
        
        Returns:
            趋势分析结果字典
        """
        try:
            results = {}
            
            # 年度奖项数量趋势
            yearly_counts = self.awards_df.groupby('year').size().reset_index()
            yearly_counts.columns = ['年份', '奖项数量']
            results['yearly_counts'] = yearly_counts
            
            # 年度奖项类型分布趋势
            type_trends = self.awards_df.pivot_table(
                index='year',
                columns='award_type',
                aggfunc='size',
                fill_value=0
            ).reset_index()
            results['type_trends'] = type_trends
            
            # 年度奖项等级分布趋势
            level_trends = self.awards_df.pivot_table(
                index='year',
                columns='award_level',
                aggfunc='size',
                fill_value=0
            ).reset_index()
            results['level_trends'] = level_trends
            
            return results
            
        except Exception as e:
            logger.error(f"获取趋势分析失败: {str(e)}")
            return {}
    
    def get_regional_analysis(self) -> pd.DataFrame:
        """
        获取地区分析
        
        Returns:
            地区分析DataFrame
        """
        try:
            # 检查数据框是否包含必要的字段
            if 'organization' not in self.projects_df.columns and 'organization' not in self.winners_df.columns:
                logger.warning("数据中缺少'organization'字段，无法进行地区分析")
                return pd.DataFrame(columns=['地区', '获奖次数'])
            
            # 提取机构所在地区（假设机构名称第一个字符为省份/地区名）
            def extract_region(org: str) -> str:
                if not org or not isinstance(org, str):
                    return '未知'
                return org[:2]
            
            # 合并项目和获奖人的机构
            all_orgs = []
            if 'organization' in self.projects_df.columns:
                all_orgs.append(self.projects_df['organization'])
            if 'organization' in self.winners_df.columns:
                all_orgs.append(self.winners_df['organization'])
            
            if not all_orgs:
                return pd.DataFrame(columns=['地区', '获奖次数'])
                
            all_orgs_series = pd.concat(all_orgs)
            
            # 统计地区分布
            region_stats = all_orgs_series.map(extract_region).value_counts().reset_index()
            region_stats.columns = ['地区', '获奖次数']
            
            return region_stats
            
        except Exception as e:
            logger.error(f"获取地区分析失败: {str(e)}")
            return pd.DataFrame(columns=['地区', '获奖次数'])
    
    def get_collaboration_analysis(self) -> Dict[str, Any]:
        """
        获取合作关系分析
        
        Returns:
            合作关系分析结果字典
        """
        try:
            results = {}
            
            # 检查数据框是否包含必要的字段
            if 'name' not in self.projects_df.columns:
                logger.warning("项目数据中缺少'name'字段，无法进行合作关系分析")
                return {
                    'collaboration_stats': {
                        'single_org': 0,
                        'multi_org': 0,
                        'max_orgs': 0
                    },
                    'top_collaborations': []
                }
            
            if 'organization' not in self.projects_df.columns:
                logger.warning("项目数据中缺少'organization'字段，无法进行合作关系分析")
                return {
                    'collaboration_stats': {
                        'single_org': 0,
                        'multi_org': 0,
                        'max_orgs': 0
                    },
                    'top_collaborations': []
                }
            
            # 统计多机构合作项目
            project_orgs = self.projects_df.groupby('name')['organization'].nunique()
            results['collaboration_stats'] = {
                'single_org': len(project_orgs[project_orgs == 1]),
                'multi_org': len(project_orgs[project_orgs > 1]),
                'max_orgs': project_orgs.max() if not project_orgs.empty else 0
            }
            
            # 检查获奖人数据框是否包含必要的字段
            if 'project_name' not in self.winners_df.columns or 'organization' not in self.winners_df.columns:
                logger.warning("获奖人数据中缺少必要字段，无法分析合作机构")
                results['top_collaborations'] = []
                return results
            
            # 找出合作最多的机构对
            org_pairs = []
            for _, group in self.winners_df.groupby('project_name'):
                orgs = group['organization'].unique()
                if len(orgs) > 1:
                    for i in range(len(orgs)):
                        for j in range(i + 1, len(orgs)):
                            org_pairs.append(tuple(sorted([orgs[i], orgs[j]])))
            
            if org_pairs:
                pair_counts = pd.Series(org_pairs).value_counts().head(10)
                results['top_collaborations'] = [
                    {
                        'organizations': list(pair),
                        'count': count
                    }
                    for pair, count in pair_counts.items()
                ]
            else:
                results['top_collaborations'] = []
            
            return results
            
        except Exception as e:
            logger.error(f"获取合作关系分析失败: {str(e)}")
            return {
                'collaboration_stats': {
                    'single_org': 0,
                    'multi_org': 0,
                    'max_orgs': 0
                },
                'top_collaborations': []
            }
    
    def get_field_analysis(self) -> pd.DataFrame:
        """
        获取研究领域分析
        
        Returns:
            研究领域分析DataFrame
        """
        try:
            # 检查数据框是否包含必要的字段
            if 'name' not in self.projects_df.columns:
                logger.warning("项目数据中缺少'name'字段，无法进行研究领域分析")
                return pd.DataFrame(columns=['关键词', '出现次数'])
            
            # 提取项目名称中的关键词
            def extract_keywords(text: str) -> List[str]:
                if not text or not isinstance(text, str):
                    return []
                # 这里可以使用更复杂的关键词提取算法
                words = text.split()
                return [w for w in words if len(w) >= 2]
            
            # 统计关键词频率
            keywords = []
            for name in self.projects_df['name']:
                keywords.extend(extract_keywords(name))
            
            if keywords:
                keyword_stats = pd.Series(keywords).value_counts().head(20).reset_index()
                keyword_stats.columns = ['关键词', '出现次数']
                return keyword_stats
            
            return pd.DataFrame(columns=['关键词', '出现次数'])
            
        except Exception as e:
            logger.error(f"获取研究领域分析失败: {str(e)}")
            return pd.DataFrame(columns=['关键词', '出现次数'])
    
    def get_impact_analysis(self) -> Dict[str, Any]:
        """
        获取影响力分析
        
        Returns:
            影响力分析结果字典
        """
        try:
            results = {}
            
            # 计算机构影响力得分
            org_scores = {}
            award_weights = {
                '特等奖': 5,
                '一等奖': 4,
                '二等奖': 3,
                '三等奖': 2,
                '优秀奖': 1,
                '提名奖': 0.5
            }
            
            for _, row in self.projects_df.iterrows():
                org = row.get('organization')
                level = row.get('level')
                if org and level:
                    score = award_weights.get(level, 1)
                    org_scores[org] = org_scores.get(org, 0) + score
            
            if org_scores:
                org_impact = pd.DataFrame([
                    {'机构': org, '影响力得分': score}
                    for org, score in org_scores.items()
                ]).sort_values('影响力得分', ascending=False).head(10)
                
                results['top_organizations'] = org_impact.to_dict('records')
            else:
                results['top_organizations'] = []
            
            # 计算获奖人影响力得分
            winner_scores = {}
            for _, row in self.winners_df.iterrows():
                name = row.get('name')
                project_name = row.get('project_name')
                if name and project_name:
                    project_level = self.projects_df[
                        self.projects_df['name'] == project_name
                    ]['level'].iloc[0]
                    score = award_weights.get(project_level, 1)
                    winner_scores[name] = winner_scores.get(name, 0) + score
            
            if winner_scores:
                winner_impact = pd.DataFrame([
                    {'获奖人': name, '影响力得分': score}
                    for name, score in winner_scores.items()
                ]).sort_values('影响力得分', ascending=False).head(10)
                
                results['top_winners'] = winner_impact.to_dict('records')
            else:
                results['top_winners'] = []
            
            return results
            
        except Exception as e:
            logger.error(f"获取影响力分析失败: {str(e)}")
            return {}
    
    def get_network_analysis(self, min_weight: int = None) -> Dict[str, Any]:
        """
        获取合作网络分析
        
        Args:
            min_weight: 最小权重阈值
            
        Returns:
            网络分析结果
        """
        try:
            # 创建合作网络
            G = nx.Graph()
            
            # 遍历项目数据
            for _, project in self.projects_df.iterrows():
                # 获取项目相关的获奖人
                winners = self.winners_df[self.winners_df['project_name'] == project['name']]
                
                # 添加节点和边
                winner_list = winners['name'].tolist()
                for i in range(len(winner_list)):
                    for j in range(i + 1, len(winner_list)):
                        if G.has_edge(winner_list[i], winner_list[j]):
                            G[winner_list[i]][winner_list[j]]['weight'] += 1
                        else:
                            G.add_edge(winner_list[i], winner_list[j], weight=1)
            
            # 过滤低权重的边
            if min_weight:
                edges_to_remove = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] < min_weight]
                G.remove_edges_from(edges_to_remove)
            
            # 计算网络指标
            results = {
                'node_count': G.number_of_nodes(),
                'edge_count': G.number_of_edges(),
                'average_degree': sum(dict(G.degree()).values()) / G.number_of_nodes(),
                'density': nx.density(G),
                'clustering_coefficient': nx.average_clustering(G),
                'components': list(nx.connected_components(G)),
                'centrality': {
                    'degree': nx.degree_centrality(G),
                    'betweenness': nx.betweenness_centrality(G),
                    'closeness': nx.closeness_centrality(G)
                }
            }
            
            return results
            
        except Exception as e:
            logger.error(f"获取网络分析失败: {str(e)}")
            return {}
    
    def get_text_analysis(self) -> Dict[str, Any]:
        """
        获取文本分析结果
        
        Returns:
            文本分析结果
        """
        try:
            from collections import Counter
            import jieba
            import jieba.analyse
            
            # 合并所有项目名称和描述
            text = ' '.join(self.projects_df['name'].dropna().tolist())
            
            # 提取关键词
            keywords = jieba.analyse.extract_tags(text, topK=20, withWeight=True)
            
            # 分词统计
            words = jieba.cut(text)
            word_freq = Counter(words)
            
            # 计算词频统计
            results = {
                'keywords': {word: weight for word, weight in keywords},
                'word_frequency': dict(word_freq.most_common(50)),
                'total_words': sum(word_freq.values()),
                'unique_words': len(word_freq)
            }
            
            return results
            
        except Exception as e:
            logger.error(f"获取文本分析失败: {str(e)}")
            return {} 