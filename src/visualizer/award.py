from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
from loguru import logger
import matplotlib.pyplot as plt
import networkx as nx
from wordcloud import WordCloud

from .base import BaseVisualizer
from analyzer.award import AwardAnalyzer

class AwardVisualizer(BaseVisualizer):
    """奖项可视化器"""
    
    def __init__(self, analyzer: AwardAnalyzer):
        """
        初始化可视化器
        
        Args:
            analyzer: 奖项分析器
        """
        super().__init__()
        self.analyzer = analyzer
    
    def plot_trend_analysis(self, save_dir: str = None) -> None:
        """
        绘制趋势分析图表
        
        Args:
            save_dir: 保存目录
        """
        try:
            # 获取趋势分析数据
            trend_data = self.analyzer.get_trend_analysis()
            
            # 绘制年度奖项数量趋势
            yearly_counts = trend_data.get('yearly_counts')
            if not yearly_counts.empty:
                self.plot_line(
                    data=yearly_counts,
                    x='年份',
                    y='奖项数量',
                    title='年度奖项数量趋势',
                    save_path=f"{save_dir}/yearly_counts.png" if save_dir else None
                )
            
            # 绘制年度奖项类型分布趋势
            type_trends = trend_data.get('type_trends')
            if not type_trends.empty:
                self.plot_multiple(
                    plots=[{
                        'type': 'line',
                        'data': type_trends,
                        'x': 'year',
                        'y': col,
                        'title': f'{col}趋势',
                        'xlabel': '年份',
                        'ylabel': '数量'
                    } for col in type_trends.columns if col != 'year'],
                    title='年度奖项类型分布趋势',
                    layout=(2, 3),
                    save_path=f"{save_dir}/type_trends.png" if save_dir else None
                )
            
            # 绘制年度奖项等级分布趋势
            level_trends = trend_data.get('level_trends')
            if not level_trends.empty:
                self.plot_multiple(
                    plots=[{
                        'type': 'line',
                        'data': level_trends,
                        'x': 'year',
                        'y': col,
                        'title': f'{col}趋势',
                        'xlabel': '年份',
                        'ylabel': '数量'
                    } for col in level_trends.columns if col != 'year'],
                    title='年度奖项等级分布趋势',
                    layout=(2, 3),
                    save_path=f"{save_dir}/level_trends.png" if save_dir else None
                )
                
        except Exception as e:
            logger.error(f"绘制趋势分析图表失败: {str(e)}")
    
    def plot_regional_analysis(self, save_dir: str = None) -> None:
        """
        绘制地区分析图表
        
        Args:
            save_dir: 保存目录
        """
        try:
            # 获取地区分析数据
            region_stats = self.analyzer.get_regional_analysis()
            
            if not region_stats.empty:
                # 绘制地区分布柱状图
                self.plot_bar(
                    data=region_stats,
                    x='地区',
                    y='获奖次数',
                    title='地区获奖分布',
                    rotation=45,
                    save_path=f"{save_dir}/region_stats.png" if save_dir else None
                )
                
                # 绘制地区分布饼图
                self.plot_pie(
                    data=region_stats.set_index('地区')['获奖次数'],
                    title='地区获奖占比',
                    save_path=f"{save_dir}/region_pie.png" if save_dir else None
                )
                
        except Exception as e:
            logger.error(f"绘制地区分析图表失败: {str(e)}")
    
    def plot_collaboration_analysis(self, save_dir: str = None) -> None:
        """
        绘制合作关系分析图表
        
        Args:
            save_dir: 保存目录
        """
        try:
            # 获取合作关系分析数据
            collab_data = self.analyzer.get_collaboration_analysis()
            
            # 绘制合作统计饼图
            stats = collab_data.get('collaboration_stats', {})
            if stats:
                collab_series = pd.Series({
                    '单机构项目': stats.get('single_org', 0),
                    '多机构项目': stats.get('multi_org', 0)
                })
                
                self.plot_pie(
                    data=collab_series,
                    title='项目合作情况分布',
                    save_path=f"{save_dir}/collaboration_pie.png" if save_dir else None
                )
            
            # 绘制热门合作机构对
            top_collabs = collab_data.get('top_collaborations', [])
            if top_collabs:
                collab_df = pd.DataFrame(top_collabs)
                collab_df['机构对'] = collab_df['organizations'].apply(lambda x: ' & '.join(x))
                
                self.plot_bar(
                    data=collab_df,
                    x='机构对',
                    y='count',
                    title='热门合作机构对',
                    xlabel='机构对',
                    ylabel='合作次数',
                    rotation=45,
                    save_path=f"{save_dir}/top_collaborations.png" if save_dir else None
                )
                
        except Exception as e:
            logger.error(f"绘制合作关系分析图表失败: {str(e)}")
    
    def plot_field_analysis(self, save_dir: str = None) -> None:
        """
        绘制研究领域分析图表
        
        Args:
            save_dir: 保存目录
        """
        try:
            # 获取研究领域分析数据
            field_stats = self.analyzer.get_field_analysis()
            
            if not field_stats.empty:
                # 绘制研究领域词频统计
                self.plot_bar(
                    data=field_stats,
                    x='关键词',
                    y='出现次数',
                    title='研究领域热点词频统计',
                    rotation=45,
                    save_path=f"{save_dir}/field_stats.png" if save_dir else None
                )
                
        except Exception as e:
            logger.error(f"绘制研究领域分析图表失败: {str(e)}")
    
    def plot_impact_analysis(self, save_dir: str = None) -> None:
        """
        绘制影响力分析图表
        
        Args:
            save_dir: 保存目录
        """
        try:
            # 获取影响力分析数据
            impact_data = self.analyzer.get_impact_analysis()
            
            # 绘制机构影响力排名
            top_orgs = impact_data.get('top_organizations', [])
            if top_orgs:
                org_df = pd.DataFrame(top_orgs)
                
                self.plot_bar(
                    data=org_df,
                    x='机构',
                    y='影响力得分',
                    title='机构影响力排名',
                    rotation=45,
                    save_path=f"{save_dir}/org_impact.png" if save_dir else None
                )
            
            # 绘制获奖人影响力排名
            top_winners = impact_data.get('top_winners', [])
            if top_winners:
                winner_df = pd.DataFrame(top_winners)
                
                self.plot_bar(
                    data=winner_df,
                    x='获奖人',
                    y='影响力得分',
                    title='获奖人影响力排名',
                    rotation=45,
                    save_path=f"{save_dir}/winner_impact.png" if save_dir else None
                )
                
        except Exception as e:
            logger.error(f"绘制影响力分析图表失败: {str(e)}")
    
    def plot_summary(self, save_dir: str = None) -> None:
        """
        绘制总体概况图表
        
        Args:
            save_dir: 保存目录
        """
        try:
            # 获取基础统计信息
            stats = self.analyzer.get_basic_stats()
            
            # 绘制奖项类型分布
            award_types = stats.get('award_types', {})
            if award_types:
                self.plot_pie(
                    data=pd.Series(award_types),
                    title='奖项类型分布',
                    save_path=f"{save_dir}/award_types.png" if save_dir else None
                )
            
            # 绘制奖项等级分布
            award_levels = stats.get('award_levels', {})
            if award_levels:
                self.plot_pie(
                    data=pd.Series(award_levels),
                    title='奖项等级分布',
                    save_path=f"{save_dir}/award_levels.png" if save_dir else None
                )
            
            # 绘制总体统计数据
            summary_data = pd.DataFrame([{
                '统计项': '奖项总数',
                '数量': stats.get('total_awards', 0)
            }, {
                '统计项': '项目总数',
                '数量': stats.get('total_projects', 0)
            }, {
                '统计项': '获奖人总数',
                '数量': stats.get('total_winners', 0)
            }])
            
            self.plot_bar(
                data=summary_data,
                x='统计项',
                y='数量',
                title='总体统计',
                save_path=f"{save_dir}/summary.png" if save_dir else None
            )
                
        except Exception as e:
            logger.error(f"绘制总体概况图表失败: {str(e)}")

    def plot_network_analysis(self, save_dir: str = None) -> None:
        """
        绘制网络分析图表
        
        Args:
            save_dir: 保存目录
        """
        try:
            # 获取网络分析数据
            network_data = self.analyzer.get_network_analysis(
                min_weight=self.analyzer.config.get('network_min_weight', 2)
            )
            
            if not network_data:
                return
            
            # 创建图形
            plt.figure(figsize=(12, 8))
            
            # 构建网络图
            G = nx.Graph()
            centrality = network_data['centrality']['degree']
            
            # 添加节点和边
            for component in network_data['components']:
                for node in component:
                    G.add_node(node)
            
            # 设置节点大小和颜色
            node_size = [v * 3000 for v in centrality.values()]
            node_color = list(centrality.values())
            
            # 绘制网络图
            pos = nx.spring_layout(G)
            nx.draw(G, pos,
                    node_color=node_color,
                    node_size=node_size,
                    cmap=plt.cm.viridis,
                    with_labels=True,
                    font_size=8,
                    font_color='black')
            
            plt.title('获奖人合作网络')
            
            if save_dir:
                plt.savefig(f"{save_dir}/network_analysis.png", bbox_inches='tight', dpi=300)
                plt.close()
            else:
                plt.show()
            
        except Exception as e:
            logger.error(f"绘制网络分析图表失败: {str(e)}")

    def plot_text_analysis(self, save_dir: str = None) -> None:
        """
        绘制文本分析图表
        
        Args:
            save_dir: 保存目录
        """
        try:
            # 获取文本分析数据
            text_data = self.analyzer.get_text_analysis()
            
            if not text_data:
                return
            
            # 绘制关键词词云图
            wc = WordCloud(width=800, height=400,
                          background_color='white',
                          font_path='SimHei.ttf',  # 使用黑体
                          max_words=100)
            
            # 生成词云
            wc.generate_from_frequencies(text_data['keywords'])
            
            # 显示词云图
            plt.figure(figsize=(10, 6))
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            plt.title('项目关键词词云图')
            
            if save_dir:
                plt.savefig(f"{save_dir}/wordcloud.png", bbox_inches='tight', dpi=300)
                plt.close()
            else:
                plt.show()
            
            # 绘制词频统计图
            word_freq = pd.Series(text_data['word_frequency']).head(20)
            
            plt.figure(figsize=(12, 6))
            word_freq.plot(kind='bar')
            plt.title('高频词统计')
            plt.xlabel('词语')
            plt.ylabel('频次')
            plt.xticks(rotation=45)
            
            if save_dir:
                plt.savefig(f"{save_dir}/word_frequency.png", bbox_inches='tight', dpi=300)
                plt.close()
            else:
                plt.show()
            
        except Exception as e:
            logger.error(f"绘制文本分析图表失败: {str(e)}") 