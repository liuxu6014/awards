from typing import List, Dict, Any
from abc import ABC, abstractmethod
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from loguru import logger
import requests
from fake_useragent import UserAgent
import os
import sys
import json
import random
import re
from datetime import datetime

# 修复导入路径
try:
    from config.config import SEARCH_ENGINES, REQUEST_DELAY, MAX_PAGES, USER_AGENT
except ImportError:
    # 尝试相对导入
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from config.config import SEARCH_ENGINES, REQUEST_DELAY, MAX_PAGES, USER_AGENT

class SearchEngine(ABC):
    """搜索引擎基类"""
    
    def __init__(self, engine_name: str):
        """
        初始化搜索引擎
        
        Args:
            engine_name: 搜索引擎名称
        """
        self.config = SEARCH_ENGINES.get(engine_name)
        if not self.config:
            raise ValueError(f"不支持的搜索引擎: {engine_name}")
            
        self.headers = {"User-Agent": USER_AGENT}
        self.base_url = self.config['url']
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def search(self, keyword: str, max_pages: int = MAX_PAGES) -> List[Dict[str, Any]]:
        """
        执行搜索
        
        Args:
            keyword: 搜索关键词
            max_pages: 最大页数
            
        Returns:
            搜索结果列表
        """
        results = []
        page = 1
        retry_count = 0
        max_retries = 3
        
        while page <= max_pages:
            try:
                logger.info(f"正在搜索第 {page} 页: {keyword}")
                
                # 获取搜索结果页
                params = self._get_search_params(keyword, page)
                response = self._get_page(params)
                
                if not response:
                    if retry_count < max_retries:
                        retry_count += 1
                        logger.warning(f"获取页面失败，第 {retry_count} 次重试")
                        time.sleep(REQUEST_DELAY * 2)
                        continue
                    else:
                        logger.error("重试次数已达上限，停止搜索")
                        break
                
                # 重置重试计数
                retry_count = 0
                
                # 解析搜索结果
                page_results = self._parse_results(response)
                if not page_results:
                    break
                
                # 过滤和处理结果
                filtered_results = self._filter_results(page_results)
                if filtered_results:
                    results.extend(filtered_results)
                    
                    # 检查是否已收集足够的结果
                    if len(results) >= max_pages * 10:
                        logger.info("已收集足够的结果")
                        break
                
                # 检查是否有下一页
                if not self._has_next_page(response):
                    break
                
                # 随机延迟请求
                delay = REQUEST_DELAY + random.uniform(0, 1)
                time.sleep(delay)
                page += 1
                
            except Exception as e:
                logger.error(f"搜索出错: {str(e)}")
                if retry_count < max_retries:
                    retry_count += 1
                    logger.warning(f"搜索出错，第 {retry_count} 次重试")
                    time.sleep(REQUEST_DELAY * 2)
                    continue
                else:
                    break
        
        return results
    
    def _get_page(self, params: Dict[str, Any]) -> BeautifulSoup:
        """
        获取页面内容
        
        Args:
            params: 请求参数
            
        Returns:
            BeautifulSoup对象
        """
        try:
            # 随机选择User-Agent
            self.headers['User-Agent'] = UserAgent().random
            
            # 设置代理（如果需要）
            proxies = self._get_proxy() if hasattr(self, '_get_proxy') else None
            
            # 发送请求
            response = self.session.get(
                self.base_url,
                params=params,
                headers=self.headers,
                proxies=proxies,
                timeout=30
            )
            
            # 检查响应状态
            response.raise_for_status()
            
            # 检查是否被封禁
            if self._is_banned(response.text):
                logger.warning("检测到搜索被限制，等待恢复")
                time.sleep(60)  # 等待1分钟
                return None
            
            return BeautifulSoup(response.text, 'lxml')
            
        except Exception as e:
            logger.error(f"获取页面失败: {str(e)}")
            return None
    
    @abstractmethod
    def _get_search_params(self, keyword: str, page: int) -> Dict[str, Any]:
        """
        获取搜索参数
        
        Args:
            keyword: 搜索关键词
            page: 页码
            
        Returns:
            搜索参数字典
        """
        pass
    
    @abstractmethod
    def _parse_results(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        解析搜索结果
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            解析后的结果列表
        """
        pass
    
    @abstractmethod
    def _has_next_page(self, soup: BeautifulSoup) -> bool:
        """
        检查是否有下一页
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            是否有下一页
        """
        pass
    
    def close(self):
        """关闭会话"""
        self.session.close()
        
    def save_results(self, results: List[Dict[str, Any]], filename: str) -> None:
        """
        保存搜索结果
        
        Args:
            results: 搜索结果列表
            filename: 文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            logger.info(f"搜索结果已保存到: {filename}")
        except Exception as e:
            logger.error(f"保存搜索结果失败: {str(e)}")

    def _filter_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        过滤和处理搜索结果
        
        Args:
            results: 原始搜索结果
            
        Returns:
            处理后的结果列表
        """
        filtered = []
        
        for result in results:
            try:
                # 检查标题相关性
                title = result.get('title', '')
                if not any(keyword in title for keyword in ['奖', '科技', '创新', '成果']):
                    continue
                
                # 检查描述相关性
                description = result.get('description', '')
                if not any(keyword in description for keyword in ['获奖', '授予', '表彰']):
                    continue
                
                # 检查时间范围
                date = result.get('date')
                if date:
                    try:
                        year = int(re.search(r'20\d{2}', date).group())
                        if not (2010 <= year <= datetime.now().year):
                            continue
                    except:
                        pass
                
                # 添加额外信息
                result['crawled_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                result['search_keyword'] = self.current_keyword
                
                filtered.append(result)
                
            except Exception as e:
                logger.error(f"过滤结果失败: {str(e)}")
                continue
        
        return filtered

    def _is_banned(self, html: str) -> bool:
        """
        检查是否被封禁
        
        Args:
            html: 页面内容
            
        Returns:
            是否被封禁
        """
        # 检查常见的封禁特征
        ban_keywords = [
            '访问频率过高',
            '请输入验证码',
            'robot',
            'forbidden',
            'banned'
        ]
        
        return any(keyword in html.lower() for keyword in ban_keywords) 