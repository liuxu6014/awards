from typing import Dict, Any, List, Optional
import os
import time
from datetime import datetime
from loguru import logger
import pandas as pd

from .base import BaseReporter
from .html import HTMLReporter
from .pdf import PDFReporter
from analyzer.award import AwardAnalyzer
from visualizer.award import AwardVisualizer

class AwardReporter:
    """奖项报告生成器"""
    
    def __init__(self, analyzer: AwardAnalyzer, visualizer: AwardVisualizer,
                output_dir: str = "reports", template_dir: str = "templates"):
        """
        初始化奖项报告生成器
        
        Args:
            analyzer: 奖项分析器
            visualizer: 奖项可视化器
            output_dir: 报告输出目录
            template_dir: 模板目录
        """
        self.analyzer = analyzer
        self.visualizer = visualizer
        self.output_dir = output_dir
        self.template_dir = template_dir
        
        # 创建报告生成器
        self.html_reporter = HTMLReporter(output_dir, template_dir)
        self.pdf_reporter = PDFReporter(output_dir, template_dir)
        
        # 创建图表目录
        self.charts_dir = os.path.join(output_dir, "charts")
        if not os.path.exists(self.charts_dir):
            os.makedirs(self.charts_dir)
    
    def generate_report(self, format: str = "html") -> str:
        """
        生成奖项分析报告
        
        Args:
            format: 报告格式，支持html和pdf
            
        Returns:
            生成的报告路径
        """
        try:
            # 生成图表
            chart_paths = self._generate_charts()
            
            # 准备报告数据
            report_data = self._prepare_report_data(chart_paths)
            
            # 根据格式生成报告
            if format.lower() == "pdf":
                return self.pdf_reporter.generate_report(report_data)
            else:
                return self.html_reporter.generate_report(report_data)
                
        except Exception as e:
            logger.error(f"生成奖项分析报告失败: {str(e)}")
            return ""
    
    def _generate_charts(self) -> Dict[str, str]:
        """
        生成图表
        
        Returns:
            图表路径字典
        """
        chart_paths = {}
        
        try:
            # 生成总体概况图表
            self.visualizer.plot_summary(self.charts_dir)
            chart_paths.update({
                'summary': os.path.join(self.charts_dir, "summary.png"),
                'award_types': os.path.join(self.charts_dir, "award_types.png"),
                'award_levels': os.path.join(self.charts_dir, "award_levels.png")
            })
            
            # 生成趋势分析图表
            self.visualizer.plot_trend_analysis(self.charts_dir)
            chart_paths.update({
                'yearly_counts': os.path.join(self.charts_dir, "yearly_counts.png"),
                'type_trends': os.path.join(self.charts_dir, "type_trends.png"),
                'level_trends': os.path.join(self.charts_dir, "level_trends.png")
            })
            
            # 生成地区分析图表
            self.visualizer.plot_regional_analysis(self.charts_dir)
            chart_paths.update({
                'region_stats': os.path.join(self.charts_dir, "region_stats.png"),
                'region_pie': os.path.join(self.charts_dir, "region_pie.png")
            })
            
            # 生成合作关系分析图表
            self.visualizer.plot_collaboration_analysis(self.charts_dir)
            chart_paths.update({
                'collaboration_pie': os.path.join(self.charts_dir, "collaboration_pie.png"),
                'top_collaborations': os.path.join(self.charts_dir, "top_collaborations.png")
            })
            
            # 生成研究领域分析图表
            self.visualizer.plot_field_analysis(self.charts_dir)
            chart_paths.update({
                'field_stats': os.path.join(self.charts_dir, "field_stats.png")
            })
            
            # 生成影响力分析图表
            self.visualizer.plot_impact_analysis(self.charts_dir)
            chart_paths.update({
                'org_impact': os.path.join(self.charts_dir, "org_impact.png"),
                'winner_impact': os.path.join(self.charts_dir, "winner_impact.png")
            })
            
            return chart_paths
            
        except Exception as e:
            logger.error(f"生成图表失败: {str(e)}")
            return chart_paths
    
    def _prepare_report_data(self, chart_paths: Dict[str, str]) -> Dict[str, Any]:
        """
        准备报告数据
        
        Args:
            chart_paths: 图表路径字典
            
        Returns:
            报告数据字典
        """
        # 获取基础统计信息
        basic_stats = self.analyzer.get_basic_stats()
        
        # 获取趋势分析数据
        trend_data = self.analyzer.get_trend_analysis()
        
        # 获取地区分析数据
        region_data = self.analyzer.get_regional_analysis()
        
        # 获取合作关系分析数据
        collab_data = self.analyzer.get_collaboration_analysis()
        
        # 获取研究领域分析数据
        field_data = self.analyzer.get_field_analysis()
        
        # 获取影响力分析数据
        impact_data = self.analyzer.get_impact_analysis()
        
        # 获取网络分析数据
        network_data = self.analyzer.get_network_analysis()
        
        # 获取文本分析数据
        text_data = self.analyzer.get_text_analysis()
        
        # 准备报告数据
        report_data = {
            'title': '科技奖励数据分析报告',
            'subtitle': f'分析时间范围: {basic_stats.get("year_range", {}).get("min_year", "")} - {basic_stats.get("year_range", {}).get("max_year", "")}',
            'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            
            # 总体概况
            'summary': {
                'basic_stats': basic_stats,
                'key_findings': self._generate_key_findings(basic_stats),
                'charts': [
                    {'title': '总体统计', 'path': chart_paths.get('summary')},
                    {'title': '奖项类型分布', 'path': chart_paths.get('award_types')},
                    {'title': '奖项等级分布', 'path': chart_paths.get('award_levels')}
                ]
            },
            
            # 趋势分析
            'trend_analysis': {
                'description': '本部分展示了科技奖励数据的时间趋势变化，包括年度奖项数量、类型分布和等级分布的变化趋势。',
                'data': trend_data,
                'insights': self._analyze_trends(trend_data),
                'charts': [
                    {'title': '年度奖项数量趋势', 'path': chart_paths.get('yearly_counts')},
                    {'title': '年度奖项类型分布趋势', 'path': chart_paths.get('type_trends')},
                    {'title': '年度奖项等级分布趋势', 'path': chart_paths.get('level_trends')}
                ]
            },
            
            # 地区分析
            'regional_analysis': {
                'description': '本部分展示了科技奖励数据的地区分布情况，包括各地区获奖数量和占比。',
                'data': region_data,
                'insights': self._analyze_regional_distribution(region_data),
                'charts': [
                    {'title': '地区获奖分布', 'path': chart_paths.get('region_stats')},
                    {'title': '地区获奖占比', 'path': chart_paths.get('region_pie')}
                ]
            },
            
            # 合作关系分析
            'collaboration_analysis': {
                'description': '本部分展示了科技奖励项目中的机构合作情况，包括单机构和多机构项目的比例，以及热门合作机构对。',
                'data': collab_data,
                'insights': self._analyze_collaboration(collab_data),
                'charts': [
                    {'title': '项目合作情况分布', 'path': chart_paths.get('collaboration_pie')},
                    {'title': '热门合作机构对', 'path': chart_paths.get('top_collaborations')}
                ]
            },
            
            # 研究领域分析
            'field_analysis': {
                'description': '本部分展示了科技奖励项目的研究领域分布，通过项目名称中的关键词频率来反映研究热点。',
                'data': field_data,
                'insights': self._analyze_research_fields(field_data),
                'charts': [
                    {'title': '研究领域热点词频统计', 'path': chart_paths.get('field_stats')}
                ]
            },
            
            # 影响力分析
            'impact_analysis': {
                'description': '本部分展示了机构和个人的影响力排名，基于获奖等级和数量计算影响力得分。',
                'data': impact_data,
                'insights': self._analyze_impact(impact_data),
                'charts': [
                    {'title': '机构影响力排名', 'path': chart_paths.get('org_impact')},
                    {'title': '获奖人影响力排名', 'path': chart_paths.get('winner_impact')}
                ]
            },
            
            # 网络分析
            'network_analysis': {
                'description': '本部分展示了获奖人之间的合作网络关系，包括网络结构特征和关键节点分析。',
                'data': network_data,
                'insights': self._analyze_network(network_data),
                'charts': [
                    {'title': '合作网络图', 'path': chart_paths.get('network_analysis')}
                ]
            },
            
            # 文本分析
            'text_analysis': {
                'description': '本部分展示了项目文本的关键词和主题分析结果。',
                'data': text_data,
                'insights': self._analyze_text(text_data),
                'charts': [
                    {'title': '关键词词云图', 'path': chart_paths.get('wordcloud')},
                    {'title': '高频词统计', 'path': chart_paths.get('word_frequency')}
                ]
            },
            
            # 详细数据
            'data_tables': {
                'awards': self.analyzer.awards_df,
                'projects': self.analyzer.projects_df,
                'winners': self.analyzer.winners_df
            }
        }
        
        return report_data

    def _generate_key_findings(self, stats: Dict[str, Any]) -> List[str]:
        """生成关键发现"""
        findings = []
        
        try:
            # 总体规模
            findings.append(f"共分析了{stats.get('total_awards', 0)}个奖项，涉及{stats.get('total_projects', 0)}个项目和{stats.get('total_winners', 0)}名获奖人。")
            
            # 时间跨度
            year_range = stats.get('year_range', {})
            if year_range:
                findings.append(f"数据覆盖{year_range.get('min_year', '')}至{year_range.get('max_year', '')}年。")
            
            # 奖项类型分布
            award_types = stats.get('award_types', {})
            if award_types:
                top_type = max(award_types.items(), key=lambda x: x[1])
                findings.append(f"最主要的奖项类型是{top_type[0]}，占比{(top_type[1]/sum(award_types.values())*100):.1f}%。")
            
            # 奖项等级分布
            award_levels = stats.get('award_levels', {})
            if award_levels:
                top_level = max(award_levels.items(), key=lambda x: x[1])
                findings.append(f"最多的奖项等级是{top_level[0]}，共{top_level[1]}项。")
                
        except Exception as e:
            logger.error(f"生成关键发现失败: {str(e)}")
        
        return findings

    def _analyze_trends(self, trend_data: Dict[str, Any]) -> List[str]:
        """分析趋势"""
        insights = []
        
        try:
            yearly_counts = trend_data.get('yearly_counts')
            if not yearly_counts.empty:
                # 计算增长率
                growth = (yearly_counts['奖项数量'].iloc[-1] / yearly_counts['奖项数量'].iloc[0] - 1) * 100
                insights.append(f"奖项数量总体{('增长' if growth > 0 else '下降')}了{abs(growth):.1f}%。")
                
                # 找出峰值
                peak_year = yearly_counts.loc[yearly_counts['奖项数量'].idxmax()]
                insights.append(f"{peak_year['年份']}年达到峰值，共{peak_year['奖项数量']}项。")
                
        except Exception as e:
            logger.error(f"分析趋势失败: {str(e)}")
        
        return insights

    def _analyze_regional_distribution(self, region_data: Dict[str, Any]) -> List[str]:
        """分析地区分布"""
        insights = []
        
        try:
            # 实现地区分布分析逻辑
            # 这里可以根据实际需求添加具体的分析逻辑
            insights.append("地区分布分析逻辑未实现")
            
        except Exception as e:
            logger.error(f"分析地区分布失败: {str(e)}")
        
        return insights

    def _analyze_collaboration(self, collab_data: Dict[str, Any]) -> List[str]:
        """分析合作关系"""
        insights = []
        
        try:
            # 实现合作关系分析逻辑
            # 这里可以根据实际需求添加具体的分析逻辑
            insights.append("合作关系分析逻辑未实现")
            
        except Exception as e:
            logger.error(f"分析合作关系失败: {str(e)}")
        
        return insights

    def _analyze_research_fields(self, field_data: Dict[str, Any]) -> List[str]:
        """分析研究领域"""
        insights = []
        
        try:
            # 实现研究领域分析逻辑
            # 这里可以根据实际需求添加具体的分析逻辑
            insights.append("研究领域分析逻辑未实现")
            
        except Exception as e:
            logger.error(f"分析研究领域失败: {str(e)}")
        
        return insights

    def _analyze_impact(self, impact_data: Dict[str, Any]) -> List[str]:
        """分析影响力"""
        insights = []
        
        try:
            # 实现影响力分析逻辑
            # 这里可以根据实际需求添加具体的分析逻辑
            insights.append("影响力分析逻辑未实现")
            
        except Exception as e:
            logger.error(f"分析影响力失败: {str(e)}")
        
        return insights

    def _analyze_network(self, network_data: Dict[str, Any]) -> List[str]:
        """分析网络关系"""
        insights = []
        
        try:
            # 实现网络分析逻辑
            # 这里可以根据实际需求添加具体的分析逻辑
            insights.append("网络分析逻辑未实现")
            
        except Exception as e:
            logger.error(f"分析网络关系失败: {str(e)}")
        
        return insights

    def _analyze_text(self, text_data: Dict[str, Any]) -> List[str]:
        """分析文本"""
        insights = []
        
        try:
            # 实现文本分析逻辑
            # 这里可以根据实际需求添加具体的分析逻辑
            insights.append("文本分析逻辑未实现")
            
        except Exception as e:
            logger.error(f"分析文本失败: {str(e)}")
        
        return insights 