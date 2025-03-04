from typing import Dict, Type
from .engine import SearchEngine
from .bing import BingSearch
from .baidu import BaiduSearch

class SearchEngineFactory:
    """搜索引擎工厂类"""
    
    # 注册支持的搜索引擎
    _engines: Dict[str, Type[SearchEngine]] = {
        'bing': BingSearch,
        'baidu': BaiduSearch
    }
    
    @classmethod
    def create(cls, engine_name: str) -> SearchEngine:
        """
        创建搜索引擎实例
        
        Args:
            engine_name: 搜索引擎名称
            
        Returns:
            搜索引擎实例
            
        Raises:
            ValueError: 不支持的搜索引擎
        """
        engine_class = cls._engines.get(engine_name.lower())
        if not engine_class:
            raise ValueError(f"不支持的搜索引擎: {engine_name}")
        
        return engine_class()
    
    @classmethod
    def get_supported_engines(cls) -> list:
        """
        获取支持的搜索引擎列表
        
        Returns:
            搜索引擎名称列表
        """
        return list(cls._engines.keys()) 