from typing import Dict, Any, List, Optional
import os
import time
from datetime import datetime
from loguru import logger
import pandas as pd
import jinja2
import pdfkit
import tempfile

from .base import BaseReporter
from .html import HTMLReporter

class PDFReporter(BaseReporter):
    """PDF报告生成器"""
    
    def __init__(self, output_dir: str = "reports", template_dir: str = "templates"):
        """
        初始化PDF报告生成器
        
        Args:
            output_dir: 报告输出目录
            template_dir: 模板目录
        """
        super().__init__(output_dir)
        self.template_dir = template_dir
        self._ensure_dir_exists(template_dir)
        self.html_reporter = HTMLReporter(output_dir, template_dir)
    
    def generate_report(self, data: Dict[str, Any], template: str = "report.html") -> str:
        """
        生成PDF报告
        
        Args:
            data: 报告数据
            template: 模板文件名
            
        Returns:
            生成的报告路径
        """
        try:
            # 首先生成HTML内容
            html_content = self._generate_html_content(data, template)
            
            # 保存为临时HTML文件
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
                temp_html_path = temp_html.name
                temp_html.write(html_content.encode('utf-8'))
            
            # 转换为PDF
            report_path = self._get_report_path("award_analysis", "pdf")
            
            try:
                self._html_to_pdf(temp_html_path, report_path)
            except Exception as e:
                # 如果PDF生成失败，生成HTML报告
                html_report_path = report_path.replace('.pdf', '.html')
                with open(temp_html_path, 'r', encoding='utf-8') as src, open(html_report_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
                logger.warning(f"PDF生成失败，已生成HTML报告: {html_report_path}")
                report_path = html_report_path
            
            # 删除临时HTML文件
            os.unlink(temp_html_path)
            
            logger.info(f"报告已生成: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"生成PDF报告失败: {str(e)}")
            return ""
    
    def _generate_html_content(self, data: Dict[str, Any], template: str) -> str:
        """
        生成HTML内容
        
        Args:
            data: 报告数据
            template: 模板文件名
            
        Returns:
            HTML内容
        """
        # 准备模板数据
        template_data = self.html_reporter._prepare_template_data(data)
        
        # 确保模板存在
        template_path = os.path.join(self.template_dir, template)
        if not os.path.exists(template_path):
            self.html_reporter._create_default_template(template_path)
        
        # 渲染模板
        template_obj = self.html_reporter.jinja_env.get_template(template)
        html_content = template_obj.render(**template_data)
        
        return html_content
    
    def _html_to_pdf(self, html_path: str, pdf_path: str) -> None:
        """
        将HTML转换为PDF
        
        Args:
            html_path: HTML文件路径
            pdf_path: PDF文件路径
        """
        try:
            # 配置wkhtmltopdf选项
            options = {
                'page-size': 'A4',
                'margin-top': '10mm',
                'margin-right': '10mm',
                'margin-bottom': '10mm',
                'margin-left': '10mm',
                'encoding': 'UTF-8',
                'no-outline': None,
                'enable-local-file-access': None
            }
            
            # 尝试查找wkhtmltopdf路径
            wkhtmltopdf_path = None
            possible_paths = [
                r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe',
                r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe',
                '/usr/bin/wkhtmltopdf',
                '/usr/local/bin/wkhtmltopdf'
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    wkhtmltopdf_path = path
                    break
            
            if wkhtmltopdf_path:
                logger.info(f"找到wkhtmltopdf路径: {wkhtmltopdf_path}")
                config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
                pdfkit.from_file(html_path, pdf_path, options=options, configuration=config)
            else:
                # 如果找不到wkhtmltopdf，则生成一个简单的HTML报告
                logger.warning("未找到wkhtmltopdf，将生成HTML报告代替PDF报告")
                html_report_path = pdf_path.replace('.pdf', '.html')
                with open(html_path, 'r', encoding='utf-8') as src, open(html_report_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
                # 添加一个提示信息
                with open(html_report_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                warning_msg = '<div style="background-color: #fff3cd; color: #856404; padding: 10px; margin: 10px 0; border-radius: 5px;">注意：由于未找到wkhtmltopdf，无法生成PDF报告。请安装wkhtmltopdf后重试。</div>'
                content = content.replace('<body>', f'<body>{warning_msg}')
                with open(html_report_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # 更新报告路径
                logger.info(f"已生成HTML报告代替PDF报告: {html_report_path}")
                raise Exception("未找到wkhtmltopdf，已生成HTML报告代替PDF报告")
            
        except Exception as e:
            logger.error(f"HTML转PDF失败: {str(e)}")
            raise 