"""
数据可视化模块

包含以下功能：
1. 基础图表绘制
   - 柱状图
   - 折线图
   - 饼图
   - 热力图
   - 散点图
   - 箱线图
   - 多子图

2. 奖项数据可视化
   - 趋势分析图表
   - 地区分析图表
   - 合作关系分析图表
   - 研究领域分析图表
   - 影响力分析图表
   - 总体概况图表
"""

from .base import BaseVisualizer
from .award import AwardVisualizer

__all__ = [
    'BaseVisualizer',
    'AwardVisualizer'
] 