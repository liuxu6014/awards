import os
from loguru import logger

from config.config import LOG_CONFIG

def setup_logger():
    """配置日志"""
    # 移除默认的处理器
    logger.remove()
    
    # 获取日志配置
    log_level = LOG_CONFIG.get('level', 'INFO')
    log_format = LOG_CONFIG.get('format', '<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>')
    log_rotation = LOG_CONFIG.get('rotation', '500 MB')
    log_retention = LOG_CONFIG.get('retention', '10 days')
    
    # 确保日志目录存在
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, "app.log")
    
    # 添加控制台输出
    logger.add(
        sink=lambda msg: print(msg),
        format=log_format,
        level=log_level,
        colorize=True
    )
    
    # 添加文件输出
    logger.add(
        sink=log_file,
        format=log_format,
        level=log_level,
        rotation=log_rotation,
        retention=log_retention,
        encoding="utf-8"
    )
    
    logger.info("日志系统初始化完成") 