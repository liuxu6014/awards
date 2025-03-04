from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import requests
from loguru import logger

class BaseParser(ABC):
    """网页解析器基类"""
    
    def __init__(self, headers: Optional[Dict[str, str]] = None):
        """
        初始化解析器
        
        Args:
            headers: 请求头
        """
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        获取网页内容
        
        Args:
            url: 网页URL
            
        Returns:
            BeautifulSoup对象
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except Exception as e:
            logger.error(f"获取网页失败 {url}: {str(e)}")
            return None
    
    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        解析网页内容
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            解析结果字典
        """
        pass
    
    def extract_text(self, element) -> str:
        """
        提取元素文本
        
        Args:
            element: BeautifulSoup元素
            
        Returns:
            清理后的文本
        """
        if not element:
            return ""
        return element.get_text(strip=True)
    
    def extract_attribute(self, element, attr: str) -> str:
        """
        提取元素属性
        
        Args:
            element: BeautifulSoup元素
            attr: 属性名
            
        Returns:
            属性值
        """
        if not element:
            return ""
        return element.get(attr, "")
    
    def close(self):
        """关闭会话"""
        self.session.close() 