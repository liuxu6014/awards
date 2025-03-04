import os
from typing import Optional
from PIL import Image
import pytesseract
from loguru import logger

from config.config import OCR_CONFIG

class OCRTool:
    """OCR工具类"""
    
    @staticmethod
    def image_to_text(image_path: str) -> Optional[str]:
        """
        将图片转换为文本
        
        Args:
            image_path: 图片路径
            
        Returns:
            提取的文本，失败返回None
        """
        try:
            if not os.path.exists(image_path):
                logger.error(f"图片不存在: {image_path}")
                return None
            
            # 打开图片
            image = Image.open(image_path)
            
            # 使用pytesseract进行OCR
            text = pytesseract.image_to_string(
                image, 
                lang=OCR_CONFIG.get('lang', 'chi_sim'),
                timeout=OCR_CONFIG.get('timeout', 30)
            )
            
            if not text:
                logger.warning(f"未能从图片中提取文本: {image_path}")
                return None
                
            return text.strip()
            
        except Exception as e:
            logger.error(f"图片OCR失败: {str(e)}")
            return None
    
    @staticmethod
    def pdf_to_text(pdf_path: str) -> Optional[str]:
        """
        将PDF转换为文本
        
        Args:
            pdf_path: PDF路径
            
        Returns:
            提取的文本，失败返回None
        """
        try:
            import pdfplumber
            import tempfile
            
            if not os.path.exists(pdf_path):
                logger.error(f"PDF不存在: {pdf_path}")
                return None
            
            # 创建临时目录
            temp_dir = OCR_CONFIG.get('temp_dir', 'temp')
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            # 打开PDF
            with pdfplumber.open(pdf_path) as pdf:
                text_parts = []
                
                # 遍历每一页
                for page in pdf.pages:
                    # 尝试直接提取文本
                    page_text = page.extract_text()
                    
                    # 如果文本提取失败，使用OCR
                    if not page_text:
                        # 将页面转换为图片
                        img_path = os.path.join(temp_dir, f"page_{page.page_number}.png")
                        img = page.to_image(resolution=OCR_CONFIG.get('pdf_resolution', 300))
                        img.save(img_path)
                        
                        # 对图片进行OCR
                        page_text = OCRTool.image_to_text(img_path)
                        
                        # 删除临时图片
                        if os.path.exists(img_path):
                            os.remove(img_path)
                    
                    if page_text:
                        text_parts.append(page_text)
                
                return "\n\n".join(text_parts) if text_parts else None
                
        except Exception as e:
            logger.error(f"PDF OCR失败: {str(e)}")
            return None 