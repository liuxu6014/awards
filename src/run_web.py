#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Web应用启动脚本

用于启动科技奖励数据采集与分析系统的Web界面
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入Web应用
from web.app import app
from utils.logger import setup_logger

if __name__ == "__main__":
    # 设置日志
    setup_logger()
    
    # 确保必要的目录存在
    for directory in ["data/raw", "data/processed", "data/output", "reports", "reports/charts"]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # 启动Web应用
    app.jinja_env.globals.update(now=datetime.now())
    app.run(debug=True, host='0.0.0.0', port=5000) 