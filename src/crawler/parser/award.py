import re
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
from loguru import logger

from .base import BaseParser
from config.config import AWARD_LEVELS, AWARD_TYPES

class AwardParser(BaseParser):
    """科技奖励网页解析器"""
    
    def parse(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        解析科技奖励网页
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            解析结果字典
        """
        if not soup:
            return {}
        
        try:
            # 提取基本信息
            title = self._extract_title(soup)
            content = self._extract_content(soup)
            year = self._extract_year(title, content)
            award_level = self._extract_award_level(title, content)
            award_type = self._extract_award_type(title, content)
            
            # 提取获奖项目列表
            projects = self._extract_projects(soup)
            
            return {
                'title': title,
                'content': content,
                'year': year,
                'award_level': award_level,
                'award_type': award_type,
                'projects': projects
            }
            
        except Exception as e:
            logger.error(f"解析网页失败: {str(e)}")
            return {}
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取标题"""
        # 尝试多个可能的标题标签
        for selector in ['h1', '.title', '#title', '.article-title']:
            title = soup.select_one(selector)
            if title:
                return self.extract_text(title)
        return ""
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """提取正文内容"""
        # 尝试多个可能的正文标签
        for selector in ['.content', '#content', '.article-content', '#article-content']:
            content = soup.select_one(selector)
            if content:
                return self.extract_text(content)
        return ""
    
    def _extract_year(self, title: str, content: str) -> Optional[int]:
        """提取年份"""
        # 匹配四位数字年份
        year_pattern = r'20[1-2][0-9]'
        
        # 先从标题中查找
        match = re.search(year_pattern, title)
        if match:
            return int(match.group())
        
        # 再从正文中查找
        match = re.search(year_pattern, content)
        if match:
            return int(match.group())
        
        return None
    
    def _extract_award_level(self, title: str, content: str) -> Optional[str]:
        """提取奖项等级"""
        text = title + content
        for level in AWARD_LEVELS:
            if level in text:
                return level
        return None
    
    def _extract_award_type(self, title: str, content: str) -> Optional[str]:
        """提取奖项类型"""
        text = title + content
        for award_type in AWARD_TYPES:
            if award_type in text:
                return award_type
        return None
    
    def _extract_projects(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """提取获奖项目列表"""
        projects = []
        
        # 尝试查找表格
        tables = soup.find_all('table')
        for table in tables:
            projects.extend(self._parse_table(table))
        
        # 如果没有找到表格，尝试查找列表
        if not projects:
            lists = soup.find_all(['ul', 'ol'])
            for list_elem in lists:
                projects.extend(self._parse_list(list_elem))
        
        return projects
    
    def _parse_table(self, table) -> List[Dict[str, Any]]:
        """解析表格中的项目信息"""
        projects = []
        
        try:
            rows = table.find_all('tr')
            if not rows:
                return projects
            
            # 获取表头
            headers = []
            header_row = rows[0]
            for cell in header_row.find_all(['th', 'td']):
                headers.append(self.extract_text(cell).lower())
            
            # 解析数据行
            for row in rows[1:]:
                cells = row.find_all('td')
                if not cells:
                    continue
                
                project = {}
                for i, cell in enumerate(cells):
                    if i < len(headers):
                        header = headers[i]
                        value = self.extract_text(cell)
                        
                        # 根据表头匹配字段
                        if any(key in header for key in ['项目', '成果']):
                            project['name'] = value
                        elif any(key in header for key in ['完成人', '获奖人', '作者']):
                            project['winners'] = self._parse_winners(value)
                        elif any(key in header for key in ['单位', '机构']):
                            project['organization'] = value
                        elif any(key in header for key in ['等级', '级别']):
                            project['level'] = value
                
                if project:
                    projects.append(project)
                
        except Exception as e:
            logger.error(f"解析表格失败: {str(e)}")
        
        return projects
    
    def _parse_list(self, list_elem) -> List[Dict[str, Any]]:
        """解析列表中的项目信息"""
        projects = []
        
        try:
            items = list_elem.find_all('li')
            for item in items:
                text = self.extract_text(item)
                
                # 尝试从文本中提取项目信息
                project = {
                    'name': self._extract_project_name(text),
                    'winners': self._parse_winners(text),
                    'organization': self._extract_organization(text)
                }
                
                if project['name']:
                    projects.append(project)
                
        except Exception as e:
            logger.error(f"解析列表失败: {str(e)}")
        
        return projects
    
    def _parse_winners(self, text: str) -> List[Dict[str, str]]:
        """解析获奖人信息"""
        winners = []
        
        # 移除括号内的内容
        text = re.sub(r'\([^)]*\)', '', text)
        
        # 按常见分隔符分割
        parts = re.split(r'[,，、;；]', text)
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # 尝试分离姓名和单位
            match = re.match(r'^(.+?)(?:（|【|［|\s)*(.+?)(?:）|】|］|\s)*$', part)
            if match:
                name, org = match.groups()
                winners.append({
                    'name': name.strip(),
                    'organization': org.strip() if org else None
                })
            else:
                winners.append({
                    'name': part,
                    'organization': None
                })
        
        return winners
    
    def _extract_project_name(self, text: str) -> Optional[str]:
        """从文本中提取项目名称"""
        # 常见的项目名称模式
        patterns = [
            r'《(.+?)》',  # 书名号中的内容
            r'"(.+?)"',   # 双引号中的内容
            r'"(.+?)"',   # 中文双引号中的内容
            r'项目名称[：:]\s*(.+?)(?=\s|$)',  # "项目名称："后面的内容
            r'^(\d+[、.．]\s*.*?)(?=\s|$)'  # 序号开头的内容
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_organization(self, text: str) -> Optional[str]:
        """从文本中提取单位名称"""
        # 常见的单位名称模式
        patterns = [
            r'单位[：:]\s*(.+?)(?=\s|$)',  # "单位："后面的内容
            r'(\S+(?:大学|研究所|公司|企业|集团|中心|实验室))',  # 包含机构关键词的内容
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return None 