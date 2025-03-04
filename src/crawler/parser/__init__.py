"""
网页解析器模块

提供网页内容解析功能，支持：
- 基础网页解析
- 科技奖励网页解析
"""

from .base import BaseParser
from .award import AwardParser

__all__ = ['BaseParser', 'AwardParser'] 