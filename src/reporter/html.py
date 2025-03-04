from typing import Dict, Any, List, Optional
import os
import time
from datetime import datetime
from loguru import logger
import pandas as pd
import jinja2

from .base import BaseReporter

class HTMLReporter(BaseReporter):
    """HTML报告生成器"""
    
    def __init__(self, output_dir: str = "reports", template_dir: str = "templates"):
        """
        初始化HTML报告生成器
        
        Args:
            output_dir: 报告输出目录
            template_dir: 模板目录
        """
        super().__init__(output_dir)
        self.template_dir = template_dir
        self._ensure_dir_exists(template_dir)
        self._init_jinja_env()
    
    def _init_jinja_env(self) -> None:
        """初始化Jinja2环境"""
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
    
    def generate_report(self, data: Dict[str, Any], template: str = "report.html") -> str:
        """
        生成HTML报告
        
        Args:
            data: 报告数据
            template: 模板文件名
            
        Returns:
            生成的报告路径
        """
        try:
            # 确保模板存在，如果不存在则创建默认模板
            template_path = os.path.join(self.template_dir, template)
            if not os.path.exists(template_path):
                self._create_default_template(template_path)
            
            # 准备模板数据
            template_data = self._prepare_template_data(data)
            
            # 渲染模板
            template_obj = self.jinja_env.get_template(template)
            html_content = template_obj.render(**template_data)
            
            # 保存报告
            report_path = self._get_report_path("award_analysis", "html")
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML报告已生成: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"生成HTML报告失败: {str(e)}")
            return ""
    
    def _create_default_template(self, template_path: str) -> None:
        """
        创建默认HTML模板
        
        Args:
            template_path: 模板文件路径
        """
        default_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: "Microsoft YaHei", sans-serif;
            padding: 20px;
        }
        .report-header {
            margin-bottom: 30px;
            text-align: center;
        }
        .report-section {
            margin-bottom: 40px;
        }
        .chart-container {
            margin: 20px 0;
        }
        footer {
            margin-top: 50px;
            text-align: center;
            font-size: 0.9em;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="report-header">
            <h1>{{ title }}</h1>
            <p class="text-muted">{{ subtitle }}</p>
            <p>生成时间: {{ timestamp }}</p>
        </div>

        <div class="report-section">
            <h2>1. 总体概况</h2>
            {{ summary_html|safe }}
            
            <div class="row">
                {% for chart in summary_charts %}
                <div class="col-md-6 chart-container">
                    <h4>{{ chart.title }}</h4>
                    {{ chart.html|safe }}
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="report-section">
            <h2>2. 趋势分析</h2>
            <p>{{ trend_description }}</p>
            
            <div class="row">
                {% for chart in trend_charts %}
                <div class="col-md-6 chart-container">
                    <h4>{{ chart.title }}</h4>
                    {{ chart.html|safe }}
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="report-section">
            <h2>3. 地区分析</h2>
            <p>{{ region_description }}</p>
            
            <div class="row">
                {% for chart in region_charts %}
                <div class="col-md-6 chart-container">
                    <h4>{{ chart.title }}</h4>
                    {{ chart.html|safe }}
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="report-section">
            <h2>4. 合作关系分析</h2>
            <p>{{ collaboration_description }}</p>
            
            <div class="row">
                {% for chart in collaboration_charts %}
                <div class="col-md-6 chart-container">
                    <h4>{{ chart.title }}</h4>
                    {{ chart.html|safe }}
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="report-section">
            <h2>5. 研究领域分析</h2>
            <p>{{ field_description }}</p>
            
            <div class="row">
                {% for chart in field_charts %}
                <div class="col-md-12 chart-container">
                    <h4>{{ chart.title }}</h4>
                    {{ chart.html|safe }}
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="report-section">
            <h2>6. 影响力分析</h2>
            <p>{{ impact_description }}</p>
            
            <div class="row">
                {% for chart in impact_charts %}
                <div class="col-md-6 chart-container">
                    <h4>{{ chart.title }}</h4>
                    {{ chart.html|safe }}
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="report-section">
            <h2>7. 详细数据</h2>
            
            <h3>7.1 奖项数据</h3>
            {{ awards_table|safe }}
            
            <h3>7.2 项目数据</h3>
            {{ projects_table|safe }}
            
            <h3>7.3 获奖人数据</h3>
            {{ winners_table|safe }}
        </div>

        <footer>
            <p>科技奖励数据采集与分析系统 &copy; {{ year }}</p>
        </footer>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(default_template)
        
        logger.info(f"创建默认HTML模板: {template_path}")
    
    def _prepare_template_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        准备模板数据
        
        Args:
            data: 原始数据
            
        Returns:
            处理后的模板数据
        """
        template_data = {
            'title': data.get('title', '科技奖励数据分析报告'),
            'subtitle': data.get('subtitle', '基于科技奖励数据的综合分析'),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'year': datetime.now().year,
            
            # 总体概况
            'summary_html': self._format_dict(data.get('summary', {}), '基础统计信息'),
            'summary_charts': self._prepare_chart_data(data.get('summary_charts', [])),
            
            # 趋势分析
            'trend_description': data.get('trend_description', '本部分展示了科技奖励数据的时间趋势变化。'),
            'trend_charts': self._prepare_chart_data(data.get('trend_charts', [])),
            
            # 地区分析
            'region_description': data.get('region_description', '本部分展示了科技奖励数据的地区分布情况。'),
            'region_charts': self._prepare_chart_data(data.get('region_charts', [])),
            
            # 合作关系分析
            'collaboration_description': data.get('collaboration_description', '本部分展示了科技奖励项目中的机构合作情况。'),
            'collaboration_charts': self._prepare_chart_data(data.get('collaboration_charts', [])),
            
            # 研究领域分析
            'field_description': data.get('field_description', '本部分展示了科技奖励项目的研究领域分布。'),
            'field_charts': self._prepare_chart_data(data.get('field_charts', [])),
            
            # 影响力分析
            'impact_description': data.get('impact_description', '本部分展示了机构和个人的影响力排名。'),
            'impact_charts': self._prepare_chart_data(data.get('impact_charts', [])),
            
            # 详细数据表格
            'awards_table': self._format_dataframe(data.get('awards_df', pd.DataFrame()), 20),
            'projects_table': self._format_dataframe(data.get('projects_df', pd.DataFrame()), 20),
            'winners_table': self._format_dataframe(data.get('winners_df', pd.DataFrame()), 20)
        }
        
        return template_data
    
    def _prepare_chart_data(self, charts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        准备图表数据
        
        Args:
            charts: 图表数据列表
            
        Returns:
            处理后的图表数据列表
        """
        result = []
        
        for chart in charts:
            chart_html = self._get_image_html(
                chart.get('path', ''),
                chart.get('alt', chart.get('title', '')),
                chart.get('width', '100%')
            )
            
            result.append({
                'title': chart.get('title', ''),
                'html': chart_html
            })
        
        return result 