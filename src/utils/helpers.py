"""
辅助函数模块

提供各种辅助函数，用于文本处理、文件操作等
"""

import os
import re
import uuid
import requests
from datetime import datetime
from urllib.parse import urlparse
from loguru import logger

def is_valid_pdf_url(url: str) -> bool:
    """
    检查URL是否是有效的PDF链接
    
    Args:
        url: 要检查的URL
        
    Returns:
        是否是有效的PDF链接
    """
    if not url:
        return False
        
    # 检查URL格式
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
    except:
        return False
    
    # 检查是否是PDF链接
    if url.lower().endswith('.pdf'):
        return True
        
    # 尝试获取Content-Type
    try:
        response = requests.head(url, timeout=5)
        content_type = response.headers.get('Content-Type', '')
        return 'application/pdf' in content_type.lower()
    except:
        return False

def generate_filename(prefix: str = '', suffix: str = '') -> str:
    """
    生成唯一文件名
    
    Args:
        prefix: 文件名前缀
        suffix: 文件名后缀
        
    Returns:
        生成的文件名
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    
    filename = f"{prefix}_{timestamp}_{unique_id}"
    if suffix:
        if not suffix.startswith('.'):
            suffix = '.' + suffix
        filename += suffix
        
    return filename

def download_pdf(url: str, save_dir: str = 'data/raw') -> str:
    """
    下载PDF文件
    
    Args:
        url: PDF文件URL
        save_dir: 保存目录
        
    Returns:
        保存的文件路径，失败返回空字符串
    """
    try:
        # 检查URL是否有效
        if not is_valid_pdf_url(url):
            logger.warning(f"无效的PDF URL: {url}")
            return ""
            
        # 确保保存目录存在
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        # 生成文件名
        filename = generate_filename(prefix='pdf', suffix='.pdf')
        filepath = os.path.join(save_dir, filename)
        
        # 下载文件
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        logger.info(f"PDF下载成功: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"PDF下载失败: {str(e)}")
        return ""

def clean_text(text: str) -> str:
    """
    清理文本
    
    Args:
        text: 要清理的文本
        
    Returns:
        清理后的文本
    """
    if not text:
        return ""
        
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 移除多余空白字符
    text = re.sub(r'\s+', ' ', text)
    
    # 移除特殊字符
    text = re.sub(r'[^\w\s\u4e00-\u9fff,.，。、:：;；!！?？()（）[\]【】""\'\']+', '', text)
    
    return text.strip()

def extract_year_from_text(text: str) -> int:
    """
    从文本中提取年份
    
    Args:
        text: 要提取年份的文本
        
    Returns:
        提取的年份，如果没有找到则返回当前年份
    """
    if not text:
        return datetime.now().year
        
    # 查找四位数字年份
    year_match = re.search(r'(19|20)\d{2}', text)
    if year_match:
        year = int(year_match.group(0))
        # 确保年份合理
        current_year = datetime.now().year
        if 1990 <= year <= current_year:
            return year
            
    # 查找中文年份表示
    cn_year_match = re.search(r'(\d+)\s*年', text)
    if cn_year_match:
        year = int(cn_year_match.group(1))
        # 处理两位数年份
        if 0 <= year <= 99:
            if year <= 30:  # 假设30以下是21世纪
                year += 2000
            else:
                year += 1900
        # 确保年份合理
        current_year = datetime.now().year
        if 1990 <= year <= current_year:
            return year
            
    # 默认返回当前年份
    return datetime.now().year 