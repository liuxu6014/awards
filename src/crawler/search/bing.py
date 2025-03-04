from typing import List, Dict, Any
from bs4 import BeautifulSoup
from loguru import logger

from .engine import SearchEngine

class BingSearch(SearchEngine):
    """必应搜索引擎"""
    
    def __init__(self):
        super().__init__('bing')
    
    def _get_search_params(self, keyword: str, page: int) -> Dict[str, Any]:
        """
        获取必应搜索参数
        
        Args:
            keyword: 搜索关键词
            page: 页码
            
        Returns:
            搜索参数字典
        """
        first = (page - 1) * 10 + 1
        return {
            'q': keyword,
            'first': first
        }
    
    def _parse_results(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        解析必应搜索结果
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            解析后的结果列表
        """
        results = []
        if not soup:
            return results
        
        # 查找所有搜索结果
        for item in soup.find_all('li', {'class': 'b_algo'}):
            try:
                # 提取标题和链接
                title_elem = item.find('h2')
                if not title_elem:
                    continue
                
                link = title_elem.find('a')
                if not link:
                    continue
                
                url = link.get('href', '')
                title = link.get_text(strip=True)
                
                # 提取描述
                desc_elem = item.find('div', {'class': 'b_caption'})
                description = desc_elem.get_text(strip=True) if desc_elem else ''
                
                # 提取日期（如果有）
                date_elem = item.find('div', {'class': 'news_dt'})
                date = date_elem.get_text(strip=True) if date_elem else None
                
                # 检查是否是PDF文件
                is_pdf = url.lower().endswith('.pdf')
                
                results.append({
                    'title': title,
                    'url': url,
                    'description': description,
                    'date': date,
                    'is_pdf': is_pdf
                })
                
            except Exception as e:
                logger.error(f"解析搜索结果失败: {str(e)}")
                continue
        
        return results
    
    def _has_next_page(self, soup: BeautifulSoup) -> bool:
        """
        检查是否有下一页
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            是否有下一页
        """
        if not soup:
            return False
        
        # 查找下一页按钮
        next_link = soup.find('a', {'class': 'sb_pagN'})
        return bool(next_link) 