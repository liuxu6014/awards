import re
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger

from config.config import MIN_TEXT_LENGTH, MAX_TEXT_LENGTH

class DataCleaner:
    """数据清洗类"""
    
    def clean_file(self, filepath: str) -> List[Dict[str, Any]]:
        """
        清理文件数据
        
        Args:
            filepath: 文件路径
            
        Returns:
            清理后的数据列表
        """
        try:
            logger.info(f"开始清理文件: {filepath}")
            
            # 读取JSON文件
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                logger.error(f"文件格式错误，应为JSON数组: {filepath}")
                return []
            
            # 处理搜索结果数据
            cleaned_data = []
            for item in data:
                # 尝试修复编码问题
                fixed_item = self._fix_encoding(item)
                
                # 构建基本数据结构
                cleaned_item = {
                    'title': fixed_item.get('title', ''),
                    'content': fixed_item.get('description', ''),
                    'year': self._extract_year(fixed_item),
                    'award_level': self._extract_award_level(fixed_item),
                    'award_type': self._extract_award_type(fixed_item),
                    'source_url': fixed_item.get('url', ''),
                    'source_title': fixed_item.get('title', ''),
                    'source_engine': 'search',
                    'crawled_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'projects': self._extract_projects(fixed_item)
                }
                
                # 清理数据
                cleaned_result = self.clean_award_data(cleaned_item)
                if cleaned_result:
                    cleaned_data.append(cleaned_result)
            
            logger.info(f"文件清理完成，共处理 {len(data)} 条数据，有效数据 {len(cleaned_data)} 条")
            return cleaned_data
            
        except Exception as e:
            logger.error(f"清理文件失败: {str(e)}")
            return []
    
    def _fix_encoding(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        修复编码问题
        
        Args:
            item: 原始数据项
            
        Returns:
            修复编码后的数据项
        """
        fixed_item = {}
        for key, value in item.items():
            if isinstance(value, str):
                try:
                    # 尝试修复编码问题
                    fixed_value = value.encode('latin1').decode('utf-8')
                except Exception:
                    fixed_value = value
                fixed_item[key] = fixed_value
            else:
                fixed_item[key] = value
        return fixed_item
    
    def _extract_year(self, item: Dict[str, Any]) -> Optional[int]:
        """
        提取年份
        
        Args:
            item: 数据项
            
        Returns:
            年份
        """
        # 从标题和描述中提取年份
        text = item.get('title', '') + ' ' + item.get('description', '')
        year_match = re.search(r'(20\d{2})年', text)
        if year_match:
            try:
                return int(year_match.group(1))
            except ValueError:
                pass
        return None
    
    def _extract_award_level(self, item: Dict[str, Any]) -> Optional[str]:
        """
        提取奖励等级
        
        Args:
            item: 数据项
            
        Returns:
            奖励等级
        """
        # 从描述中提取奖励等级
        text = item.get('description', '')
        if '一等奖' in text or '一等' in text:
            return '一等奖'
        elif '二等奖' in text or '二等' in text:
            return '二等奖'
        elif '特等奖' in text or '特等' in text:
            return '特等奖'
        return None
    
    def _extract_award_type(self, item: Dict[str, Any]) -> Optional[str]:
        """
        提取奖励类型
        
        Args:
            item: 数据项
            
        Returns:
            奖励类型
        """
        # 从标题和描述中提取奖励类型
        text = item.get('title', '') + ' ' + item.get('description', '')
        if '自然科学奖' in text:
            return '自然科学奖'
        elif '技术发明奖' in text:
            return '技术发明奖'
        elif '科技进步奖' in text:
            return '科技进步奖'
        elif '国际科技合作奖' in text:
            return '国际科技合作奖'
        return '科学技术奖'
    
    def _extract_projects(self, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        提取项目信息
        
        Args:
            item: 数据项
            
        Returns:
            项目信息列表
        """
        # 简单提取项目信息，实际应用中可能需要更复杂的逻辑
        projects = []
        text = item.get('description', '')
        
        # 尝试从描述中提取项目名称
        project_matches = re.findall(r'《([^》]+)》', text)
        if not project_matches:
            project_matches = re.findall(r'"([^"]+)"', text)
        
        if project_matches:
            for match in project_matches:
                projects.append({
                    'name': match,
                    'winners': [],
                    'organization': None,
                    'level': None
                })
        else:
            # 如果没有找到项目名称，使用标题作为项目名称
            title = item.get('title', '')
            if title:
                projects.append({
                    'name': title,
                    'winners': [],
                    'organization': None,
                    'level': None
                })
        
        return projects
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        清理文本
        
        Args:
            text: 原始文本
            
        Returns:
            清理后的文本
        """
        if not text:
            return ""
        
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        
        # 移除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff，。：；！？、（）《》【】""'']+', '', text)
        
        return text.strip()
    
    @staticmethod
    def clean_url(url: str) -> Optional[str]:
        """
        清理URL
        
        Args:
            url: 原始URL
            
        Returns:
            清理后的URL
        """
        if not url:
            return None
        
        # 移除URL中的特殊字符
        url = re.sub(r'[<>"\']+', '', url)
        
        # 验证URL格式
        if not re.match(r'^https?://', url):
            return None
        
        return url.strip()
    
    @staticmethod
    def clean_date(date: str) -> Optional[str]:
        """
        清理日期
        
        Args:
            date: 原始日期字符串
            
        Returns:
            标准格式的日期字符串
        """
        if not date:
            return None
        
        try:
            # 移除日期中的特殊字符
            date = re.sub(r'[年月日\s]+', '-', date)
            date = re.sub(r'-+', '-', date)
            date = date.strip('-')
            
            # 尝试解析多种日期格式
            for fmt in ['%Y-%m-%d', '%Y-%m', '%Y']:
                try:
                    dt = datetime.strptime(date, fmt)
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            return None
            
        except Exception:
            return None
    
    @staticmethod
    def clean_name(name: str) -> Optional[str]:
        """
        清理名称
        
        Args:
            name: 原始名称
            
        Returns:
            清理后的名称
        """
        if not name:
            return None
        
        # 移除特殊字符
        name = re.sub(r'[^\w\s\u4e00-\u9fff]+', '', name)
        name = name.strip()
        
        # 验证长度
        if len(name) < 2:
            return None
        
        return name
    
    @staticmethod
    def clean_organization(org: str) -> Optional[str]:
        """
        清理机构名称
        
        Args:
            org: 原始机构名称
            
        Returns:
            清理后的机构名称
        """
        if not org:
            return None
        
        # 移除特殊字符
        org = re.sub(r'[^\w\s\u4e00-\u9fff]+', '', org)
        org = org.strip()
        
        # 验证长度
        if len(org) < 4:
            return None
        
        return org
    
    def clean_award_data(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        清理奖项数据
        
        Args:
            data: 原始数据
            
        Returns:
            清理后的数据
        """
        try:
            # 清理基本字段
            title = self.clean_text(data.get('title', ''))
            if not title or len(title) < MIN_TEXT_LENGTH:
                return None
                
            content = self.clean_text(data.get('content', ''))
            if not content or len(content) > MAX_TEXT_LENGTH:
                content = content[:MAX_TEXT_LENGTH]
            
            url = self.clean_url(data.get('source_url'))
            if not url:
                return None
            
            # 清理项目列表
            projects = []
            for project in data.get('projects', []):
                cleaned_project = self.clean_project(project)
                if cleaned_project:
                    projects.append(cleaned_project)
            
            if not projects:
                return None
            
            # 返回清理后的数据
            return {
                'title': title,
                'content': content,
                'year': data.get('year'),
                'award_level': data.get('award_level'),
                'award_type': data.get('award_type'),
                'source_url': url,
                'source_title': self.clean_text(data.get('source_title', '')),
                'source_engine': data.get('source_engine'),
                'crawled_at': data.get('crawled_at'),
                'projects': projects
            }
            
        except Exception as e:
            logger.error(f"清理数据失败: {str(e)}")
            return None
    
    def clean_project(self, project: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        清理项目数据
        
        Args:
            project: 原始项目数据
            
        Returns:
            清理后的项目数据
        """
        try:
            # 清理项目名称
            name = self.clean_name(project.get('name'))
            if not name:
                return None
            
            # 清理获奖人列表
            winners = []
            for winner in project.get('winners', []):
                cleaned_winner = self.clean_winner(winner)
                if cleaned_winner:
                    winners.append(cleaned_winner)
            
            # 清理机构名称
            organization = self.clean_organization(project.get('organization'))
            
            # 返回清理后的项目数据
            return {
                'name': name,
                'winners': winners,
                'organization': organization,
                'level': project.get('level')
            }
            
        except Exception as e:
            logger.error(f"清理项目数据失败: {str(e)}")
            return None
    
    def clean_winner(self, winner: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        清理获奖人数据
        
        Args:
            winner: 原始获奖人数据
            
        Returns:
            清理后的获奖人数据
        """
        try:
            # 清理姓名
            name = self.clean_name(winner.get('name'))
            if not name:
                return None
            
            # 清理机构名称
            organization = self.clean_organization(winner.get('organization'))
            
            # 返回清理后的获奖人数据
            return {
                'name': name,
                'organization': organization
            }
            
        except Exception as e:
            logger.error(f"清理获奖人数据失败: {str(e)}")
            return None 