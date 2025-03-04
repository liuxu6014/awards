import os

# 要创建的目录列表
directories = [
    'src/processor',
    'src/analyzer',
    'data/raw',
    'data/processed',
    'data/temp',
    'tests',
    'src/crawler/search',
    'src/crawler/parser',
    'src/processor/cleaner',
    'src/processor/transformer',
    'src/analyzer/statistics',
    'src/analyzer/network',
    'src/analyzer/visualizer'
]

# 创建目录
for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f'Created directory: {directory}') 