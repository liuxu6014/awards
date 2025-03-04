"""
报告生成模块

包含以下功能：
1. 基础报告生成
2. HTML报告生成
3. PDF报告生成
4. 奖项报告生成
"""

from .base import BaseReporter
from .html import HTMLReporter
from .pdf import PDFReporter
from .award import AwardReporter

__all__ = [
    'BaseReporter',
    'HTMLReporter',
    'PDFReporter',
    'AwardReporter'
] 