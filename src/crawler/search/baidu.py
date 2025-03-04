from typing import List, Dict, Any
from bs4 import BeautifulSoup
from loguru import logger

from .engine import SearchEngine

class BaiduSearch(SearchEngine):
    """百度搜索引擎"""
    
    def __init__(self):
        super().__init__('baidu')
    
    def _get_search_params(self, keyword: str, page: int) -> Dict[str, Any]:
        """
        获取百度搜索参数
        
        Args:
            keyword: 搜索关键词
            page: 页码
            
        Returns:
            搜索参数字典
        """
        pn = (page - 1) * 10
        return {
            'wd': keyword,
            'pn': pn,
            'rn': 10,  # 每页结果数
            'ie': 'utf-8'  # 编码
        }
    
    def _parse_results(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        解析百度搜索结果
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            解析后的结果列表
        """
        results = []
        if not soup:
            return results
        
        # 查找所有搜索结果
        for item in soup.find_all('div', {'class': ['result', 'c-container']}):
            try:
                # 提取标题和链接
                title_elem = item.find('h3', {'class': 't'})
                if not title_elem:
                    continue
                
                link = title_elem.find('a')
                if not link:
                    continue
                
                url = link.get('href', '')
                title = link.get_text(strip=True)
                
                # 提取描述
                desc_elem = item.find('div', {'class': 'c-abstract'})
                if not desc_elem:
                    desc_elem = item.find('div', {'class': 'c-span-last'})
                description = desc_elem.get_text(strip=True) if desc_elem else ''
                
                # 提取日期（如果有）
                date_elem = item.find('span', {'class': 'c-color-gray2'})
                date = date_elem.get_text(strip=True) if date_elem else None
                
                # 检查是否是PDF文件
                is_pdf = 'pdf' in description.lower() or url.lower().endswith('.pdf')
                
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
        next_link = soup.find('a', string='下一页>')
        return bool(next_link) 