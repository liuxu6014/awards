"""
数据分析模块

包含以下功能：
1. 基础统计分析
2. 趋势分析
3. 地区分析
4. 合作关系分析
5. 研究领域分析
6. 影响力分析
"""

from .base import BaseAnalyzer
from .award import AwardAnalyzer

__all__ = [
    'BaseAnalyzer',
    'AwardAnalyzer'
] 