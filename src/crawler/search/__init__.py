"""
搜索引擎模块

提供多个搜索引擎的统一接口，支持：
- 必应搜索
- 百度搜索
"""

from .engine import SearchEngine
from .bing import BingSearch
from .baidu import BaiduSearch
from .factory import SearchEngineFactory

__all__ = ['SearchEngine', 'BingSearch', 'BaiduSearch', 'SearchEngineFactory'] 