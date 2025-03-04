"""
配置文件
"""

# 文本长度限制
MIN_TEXT_LENGTH = 2  # 最小文本长度
MAX_TEXT_LENGTH = 1000  # 最大文本长度

# 奖项等级
AWARD_LEVELS = [
    "一等奖",
    "二等奖", 
    "三等奖",
    "特等奖",
    "优秀奖",
    "提名奖"
]

# 奖项类型
AWARD_TYPES = [
    "自然科学奖",
    "技术发明奖",
    "科技进步奖",
    "国际科技合作奖",
    "企业创新奖",
    "青年科技奖"
]

# 搜索引擎配置
SEARCH_ENGINES = {
    "baidu": {
        "name": "百度",
        "url": "https://www.baidu.com/s",
        "params": {
            "wd": "",  # 搜索关键词
            "pn": 0,  # 页码，每页10条
            "rn": 10  # 每页结果数
        }
    },
    "bing": {
        "name": "必应",
        "url": "https://cn.bing.com/search",
        "params": {
            "q": "",  # 搜索关键词
            "first": 1,  # 起始结果索引
            "count": 10  # 每页结果数
        }
    }
}

# 爬虫配置
REQUEST_DELAY = 2  # 请求间隔时间（秒）
MAX_PAGES = 10  # 最大爬取页数
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# 日志配置
LOG_CONFIG = {
    "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    "level": "INFO",
    "rotation": "500 MB",
    "retention": "10 days"
}

# OCR配置
OCR_CONFIG = {
    "lang": "chi_sim",  # 中文简体
    "timeout": 30,  # 超时时间（秒）
    "temp_dir": "temp",  # 临时文件目录
    "pdf_resolution": 300  # PDF转图片分辨率
}

# 数据处理配置
PROCESSOR_CONFIG = {
    "batch_size": 100,  # 批处理大小
    "max_workers": 4,  # 最大工作线程数
    "retry_times": 3,  # 重试次数
    "retry_interval": 5  # 重试间隔（秒）
}

# 输出配置
OUTPUT_CONFIG = {
    "excel": {
        "sheet_names": {
            "awards": "奖项信息",
            "projects": "项目信息",
            "winners": "获奖人信息"
        },
        "file_name": "科技奖励数据.xlsx"
    },
    "csv": {
        "encoding": "utf-8-sig",
        "file_names": {
            "awards": "奖项信息.csv",
            "projects": "项目信息.csv",
            "winners": "获奖人信息.csv"
        }
    }
} 