from typing import Dict, Any, List, Optional
import os
import time
from datetime import datetime
from loguru import logger
import pandas as pd

class BaseReporter:
    """报告生成基类"""
    
    def __init__(self, output_dir: str = "reports"):
        """
        初始化报告生成器
        
        Args:
            output_dir: 报告输出目录
        """
        self.output_dir = output_dir
        self._ensure_dir_exists(output_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def generate_report(self, data: Dict[str, Any], template: str = None) -> str:
        """
        生成报告
        
        Args:
            data: 报告数据
            template: 报告模板路径
            
        Returns:
            生成的报告路径
        """
        raise NotImplementedError("子类必须实现此方法")
    
    def _ensure_dir_exists(self, directory: str) -> None:
        """
        确保目录存在
        
        Args:
            directory: 目录路径
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"创建目录: {directory}")
    
    def _get_report_path(self, report_type: str, extension: str) -> str:
        """
        获取报告文件路径
        
        Args:
            report_type: 报告类型
            extension: 文件扩展名
            
        Returns:
            报告文件路径
        """
        filename = f"{report_type}_{self.timestamp}.{extension}"
        return os.path.join(self.output_dir, filename)
    
    def _format_dataframe(self, df: pd.DataFrame, max_rows: int = None) -> str:
        """
        格式化DataFrame为HTML表格
        
        Args:
            df: DataFrame数据
            max_rows: 最大行数
            
        Returns:
            HTML表格字符串
        """
        if df.empty:
            return "<p>无数据</p>"
        
        if max_rows and len(df) > max_rows:
            df = df.head(max_rows)
            footer = f"<p><i>显示前{max_rows}行，共{len(df)}行</i></p>"
        else:
            footer = ""
        
        table_html = df.to_html(index=False, classes="table table-striped table-hover")
        return table_html + footer
    
    def _format_dict(self, data: Dict[str, Any], title: str = None) -> str:
        """
        格式化字典为HTML表格
        
        Args:
            data: 字典数据
            title: 表格标题
            
        Returns:
            HTML表格字符串
        """
        if not data:
            return "<p>无数据</p>"
        
        header = f"<h4>{title}</h4>" if title else ""
        
        rows = []
        for key, value in data.items():
            if isinstance(value, dict):
                value_str = "<ul>"
                for k, v in value.items():
                    value_str += f"<li>{k}: {v}</li>"
                value_str += "</ul>"
            elif isinstance(value, list):
                value_str = "<ul>"
                for item in value:
                    value_str += f"<li>{item}</li>"
                value_str += "</ul>"
            else:
                value_str = str(value)
            
            rows.append(f"<tr><td>{key}</td><td>{value_str}</td></tr>")
        
        table = f"""
        <table class="table table-striped table-hover">
            <thead>
                <tr>
                    <th>项目</th>
                    <th>值</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows)}
            </tbody>
        </table>
        """
        
        return header + table
    
    def _get_image_html(self, image_path: str, alt: str = "", width: str = "100%") -> str:
        """
        获取图片HTML代码
        
        Args:
            image_path: 图片路径
            alt: 替代文本
            width: 图片宽度
            
        Returns:
            图片HTML代码
        """
        if not os.path.exists(image_path):
            return f"<p>图片不存在: {image_path}</p>"
        
        # 获取相对路径
        rel_path = os.path.relpath(image_path, self.output_dir)
        return f'<img src="{rel_path}" alt="{alt}" width="{width}" class="img-fluid">' 