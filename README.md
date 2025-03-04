# 科技奖励数据采集与分析系统

这是一个自动化系统，用于收集和分析全国各级科技奖励信息。系统使用先进的网络爬虫技术和人工智能技术，从互联网上自动获取科技奖励相关数据，并进行深入分析。

## 主要功能

1. 数据采集
   - 多搜索引擎支持（必应、百度等）
   - 智能网页内容提取
   - PDF文档解析
   - 图片文字识别（OCR）
   - 自动数据结构化

2. 数据处理
   - 数据清洗和标准化
   - 重复数据去除
   - 数据格式统一
   - 数据质量验证

3. 数据分析
   - 奖项分布分析
   - 获奖项目分类统计
   - 获奖人员网络分析
   - 地域分布分析
   - 趋势分析

## 项目结构

```
├── README.md
├── requirements.txt
├── config/
│   └── config.py          # 配置文件
├── src/
│   ├── crawler/
│   │   ├── __init__.py
│   │   ├── base.py       # 爬虫基类
│   │   ├── search.py     # 搜索引擎爬虫
│   │   ├── parser.py     # 网页解析器
│   │   └── extractor.py  # 数据提取器
│   ├── processor/
│   │   ├── __init__.py
│   │   ├── cleaner.py    # 数据清洗
│   │   ├── transformer.py # 数据转换
│   │   └── validator.py  # 数据验证
│   ├── analyzer/
│   │   ├── __init__.py
│   │   ├── statistics.py # 统计分析
│   │   ├── network.py    # 网络分析
│   │   └── visualizer.py # 数据可视化
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py    # 工具函数
│   │   ├── logger.py     # 日志工具
│   │   └── ocr.py       # OCR工具
│   └── main.py           # 主程序入口
├── data/
│   ├── raw/              # 原始数据
│   ├── processed/        # 处理后的数据
│   ├── output/           # 分析结果
│   └── temp/            # 临时文件
└── tests/               # 测试用例
```

## 数据结构

系统采集的数据包含以下字段：

```json
{
    "id": "唯一标识符",
    "award_level": "奖项等级（国家级/省级）",
    "award_name": "奖项名称",
    "project_name": "项目名称",
    "winners": [
        {
            "name": "获奖人姓名",
            "role": "角色",
            "organization": "所属机构"
        }
    ],
    "year": "获奖年份",
    "province": "省份",
    "category": "项目类别",
    "source": "数据来源",
    "source_url": "源网页URL",
    "created_at": "数据采集时间"
}
```

## 环境要求

- Python 3.8+
- 依赖包见 requirements.txt

## 安装步骤

1. 克隆项目到本地
2. 创建虚拟环境（推荐）：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. 配置参数：
   - 在 config/config.py 中设置搜索参数和数据处理参数
   - 配置数据保存路径和日志级别

2. 命令行方式：
   ```bash
   # 运行数据采集
   python src/main.py collect
   
   # 运行数据分析
   python src/main.py analyze
   
   # 生成报告
   python src/main.py report
   ```

3. Web界面方式：
   ```bash
   # 启动Web界面
   python src/run_web.py
   ```
   然后在浏览器中访问 http://localhost:5000 即可使用Web界面。

## Web界面功能

科技奖励数据采集与分析系统提供了一个直观的Web界面，方便用户进行操作：

1. 数据采集
   - 设置搜索关键词、搜索引擎和最大结果数
   - 查看和下载采集结果

2. 数据处理
   - 选择原始数据文件进行处理
   - 查看处理结果和数据质量指标

3. 数据分析
   - 选择处理后的数据进行分析
   - 查看统计概览和分析图表

4. 报告生成
   - 选择分析结果生成HTML或PDF报告
   - 查看和下载生成的报告

## 注意事项

1. 请遵守网站的robots协议
2. 建议设置适当的爬取间隔
3. 注意数据安全和隐私保护
4. 定期备份重要数据

## 更新日志

### v2.0.0 (当前版本)
- 新增图片文字识别功能
- 新增数据分析模块
- 优化数据采集流程
- 改进数据存储结构

### v1.0.0 (初始版本)
- 基础爬虫功能实现
- PDF文件下载和解析
- 数据基础清洗功能 