"""
Web展示界面模块

提供科技奖励数据采集与分析系统的Web界面，包括：
1. 数据采集管理
2. 数据处理管理
3. 数据分析展示
4. 报告生成与查看
"""

import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify, send_file
from loguru import logger
import pandas as pd

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入项目模块
from crawler.search import SearchEngine
from crawler.search.factory import SearchEngineFactory
from processor.cleaner import DataCleaner
from processor.transformer import DataTransformer
from analyzer.award import AwardAnalyzer
from visualizer.award import AwardVisualizer
from reporter.award import AwardReporter
from utils.logger import setup_logger
from validator.data import DataValidator

# 创建Flask应用
app = Flask(__name__)
app.secret_key = os.urandom(24)

# 设置日志
setup_logger()

# 确保目录存在
def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"创建目录: {directory}")

# 确保必要的目录存在
ensure_dir_exists("data/raw")
ensure_dir_exists("data/processed")
ensure_dir_exists("data/output")
ensure_dir_exists("reports")
ensure_dir_exists("reports/charts")

# 首页路由
@app.route('/')
def index():
    return render_template('index.html', title="科技奖励数据采集与分析系统")

# 数据采集页面
@app.route('/collect', methods=['GET', 'POST'])
def collect():
    if request.method == 'POST':
        try:
            # 获取表单数据
            keywords = request.form.get('keywords', '')
            search_engine = request.form.get('search_engine', 'bing')
            max_pages = int(request.form.get('max_results', 10))
            
            # 执行数据采集
            engine = SearchEngineFactory.create(search_engine)
            results = engine.search(keywords, max_pages=max_pages)
            
            # 保存结果
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/raw/search_results_{timestamp}.json"
            engine.save_results(results, filename)
            
            flash(f"成功采集 {len(results)} 条数据，已保存到 {filename}", "success")
            return redirect(url_for('collect'))
            
        except Exception as e:
            logger.error(f"数据采集失败: {str(e)}")
            flash(f"数据采集失败: {str(e)}", "danger")
    
    # 获取已采集的数据文件列表
    raw_files = [f for f in os.listdir("data/raw") if f.endswith('.json')]
    raw_files.sort(reverse=True)
    
    return render_template('collect.html', title="数据采集", raw_files=raw_files)

# 数据处理页面
@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        try:
            # 获取表单数据
            input_file = request.form.get('input_file', '')
            
            if not input_file:
                flash("请选择输入文件", "warning")
                return redirect(url_for('process'))
            
            # 执行数据处理
            input_path = os.path.join("data/raw", input_file)
            
            # 数据清洗
            cleaner = DataCleaner()
            cleaned_data = cleaner.clean_file(input_path)
            
            # 数据转换
            transformer = DataTransformer()
            dataframes = transformer.to_dataframe(cleaned_data)
            
            # 保存处理后的数据
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"data/processed/{timestamp}"
            ensure_dir_exists(output_dir)
            
            # 保存为CSV和Excel
            transformer.to_csv(dataframes, output_dir)
            excel_path = os.path.join(output_dir, "award_data.xlsx")
            transformer.to_excel(dataframes, excel_path)
            
            flash(f"数据处理成功，结果已保存到 {output_dir}", "success")
            return redirect(url_for('process'))
            
        except Exception as e:
            logger.error(f"数据处理失败: {str(e)}")
            flash(f"数据处理失败: {str(e)}", "danger")
    
    # 获取原始数据文件列表
    raw_files = [f for f in os.listdir("data/raw") if f.endswith('.json')]
    raw_files.sort(reverse=True)
    
    # 获取已处理的数据目录列表
    processed_dirs = [d for d in os.listdir("data/processed") if os.path.isdir(os.path.join("data/processed", d))]
    processed_dirs.sort(reverse=True)
    
    return render_template('process.html', title="数据处理", 
                          raw_files=raw_files, processed_dirs=processed_dirs)

# 数据分析页面
@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        try:
            # 获取表单数据
            input_dir = request.form.get('input_dir', '')
            
            if not input_dir:
                flash("请选择输入目录", "warning")
                return redirect(url_for('analyze'))
            
            # 执行数据分析
            input_path = os.path.join("data/processed", input_dir)
            excel_path = os.path.join(input_path, "award_data.xlsx")
            
            # 创建分析器
            analyzer = AwardAnalyzer()
            analyzer.load_data(excel_path)
            
            # 执行分析
            analyzer.analyze()
            
            # 保存分析结果
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"data/output/{timestamp}"
            ensure_dir_exists(output_dir)
            analyzer.save_results(output_dir)
            
            # 创建可视化器
            visualizer = AwardVisualizer(analyzer)
            
            # 生成图表
            charts_dir = os.path.join(output_dir, "charts")
            ensure_dir_exists(charts_dir)
            visualizer.plot_all(charts_dir)
            
            flash(f"数据分析成功，结果已保存到 {output_dir}", "success")
            return redirect(url_for('analyze'))
            
        except Exception as e:
            logger.error(f"数据分析失败: {str(e)}")
            flash(f"数据分析失败: {str(e)}", "danger")
    
    # 获取已处理的数据目录列表
    processed_dirs = [d for d in os.listdir("data/processed") if os.path.isdir(os.path.join("data/processed", d))]
    processed_dirs.sort(reverse=True)
    
    # 获取已分析的数据目录列表
    output_dirs = [d for d in os.listdir("data/output") if os.path.isdir(os.path.join("data/output", d))]
    output_dirs.sort(reverse=True)
    
    return render_template('analyze.html', title="数据分析", 
                          processed_dirs=processed_dirs, output_dirs=output_dirs)

# 报告生成页面
@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        try:
            # 获取表单数据
            output_dir = request.form.get('output_dir', '')
            report_format = request.form.get('report_format', 'html')
            
            if not output_dir:
                flash("请选择分析结果目录", "warning")
                return redirect(url_for('report'))
            
            # 加载分析结果
            input_path = os.path.join("data/output", output_dir)
            
            # 创建分析器和可视化器
            analyzer = AwardAnalyzer()
            analyzer.load_results(input_path)
            visualizer = AwardVisualizer(analyzer)
            
            # 创建报告生成器
            reporter = AwardReporter(analyzer, visualizer)
            
            # 生成报告
            report_path = reporter.generate_report(format=report_format)
            
            if report_path:
                flash(f"报告生成成功: {report_path}", "success")
            else:
                flash("报告生成失败", "danger")
                
            return redirect(url_for('report'))
            
        except Exception as e:
            logger.error(f"报告生成失败: {str(e)}")
            flash(f"报告生成失败: {str(e)}", "danger")
    
    # 获取已分析的数据目录列表
    output_dirs = [d for d in os.listdir("data/output") if os.path.isdir(os.path.join("data/output", d))]
    output_dirs.sort(reverse=True)
    
    # 获取已生成的报告列表
    reports = []
    if os.path.exists("reports"):
        reports = [f for f in os.listdir("reports") if f.endswith('.html') or f.endswith('.pdf')]
        reports.sort(reverse=True)
    
    return render_template('report.html', title="报告生成", 
                          output_dirs=output_dirs, reports=reports)

# 查看报告
@app.route('/view_report/<filename>')
def view_report(filename):
    try:
        # 检查reports目录是否存在
        if not os.path.exists('reports'):
            os.makedirs('reports')
            flash("报告目录不存在，已创建新目录", "warning")
            return redirect(url_for('report'))
        
        # 检查文件是否存在
        if not os.path.exists(os.path.join('reports', filename)):
            flash(f"报告文件 {filename} 不存在", "danger")
            return redirect(url_for('report'))
        
        return send_from_directory('reports', filename)
    except Exception as e:
        logger.error(f"查看报告失败: {str(e)}")
        flash(f"查看报告失败: {str(e)}", "danger")
        return redirect(url_for('report'))

# 下载文件
@app.route('/download/<path:filepath>')
def download_file(filepath):
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    return send_from_directory(directory, filename, as_attachment=True)

# API路由 - 获取基础统计信息
@app.route('/api/stats/<output_dir>')
def api_stats(output_dir):
    try:
        input_path = os.path.join("data/output", output_dir)
        
        # 创建分析器
        analyzer = AwardAnalyzer()
        analyzer.load_results(input_path)
        
        # 获取基础统计信息
        stats = analyzer.get_basic_stats()
        return jsonify({"success": True, "data": stats})
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/network_analysis/<output_dir>')
def network_analysis(output_dir):
    """网络分析页面"""
    try:
        # 加载分析结果
        input_path = os.path.join("data/output", output_dir)
        
        # 创建分析器和可视化器
        analyzer = AwardAnalyzer()
        analyzer.load_results(input_path)
        
        # 获取网络分析数据
        network_data = analyzer.get_network_analysis()
        
        # 生成网络图
        charts_dir = os.path.join(input_path, "charts")
        ensure_dir_exists(charts_dir)
        
        visualizer = AwardVisualizer(analyzer)
        visualizer.plot_network_analysis(charts_dir)
        
        return render_template('network.html',
                             title="合作网络分析",
                             network_data=network_data,
                             output_dir=output_dir)
                             
    except Exception as e:
        logger.error(f"网络分析失败: {str(e)}")
        flash(f"网络分析失败: {str(e)}", "danger")
        return redirect(url_for('analyze'))

@app.route('/text_analysis/<output_dir>')
def text_analysis(output_dir):
    """文本分析页面"""
    try:
        # 加载分析结果
        input_path = os.path.join("data/output", output_dir)
        
        # 创建分析器和可视化器
        analyzer = AwardAnalyzer()
        analyzer.load_results(input_path)
        
        # 获取文本分析数据
        text_data = analyzer.get_text_analysis()
        
        # 生成可视化图表
        charts_dir = os.path.join(input_path, "charts")
        ensure_dir_exists(charts_dir)
        
        visualizer = AwardVisualizer(analyzer)
        visualizer.plot_text_analysis(charts_dir)
        
        return render_template('text.html',
                             title="文本分析",
                             text_data=text_data,
                             output_dir=output_dir)
                             
    except Exception as e:
        logger.error(f"文本分析失败: {str(e)}")
        flash(f"文本分析失败: {str(e)}", "danger")
        return redirect(url_for('analyze'))

@app.route('/api/export/<output_dir>/<data_type>')
def api_export_data(output_dir, data_type):
    """
    导出数据API
    
    Args:
        output_dir: 输出目录
        data_type: 数据类型(awards/projects/winners/network/text)
    """
    try:
        input_path = os.path.join("data/output", output_dir)
        
        # 创建分析器
        analyzer = AwardAnalyzer()
        analyzer.load_results(input_path)
        
        # 根据数据类型返回不同的数据
        if data_type == 'awards':
            data = analyzer.awards_df.to_dict('records')
        elif data_type == 'projects':
            data = analyzer.projects_df.to_dict('records')
        elif data_type == 'winners':
            data = analyzer.winners_df.to_dict('records')
        elif data_type == 'network':
            data = analyzer.get_network_analysis()
        elif data_type == 'text':
            data = analyzer.get_text_analysis()
        else:
            return jsonify({"success": False, "error": "不支持的数据类型"})
            
        return jsonify({
            "success": True,
            "data": data,
            "total": len(data) if isinstance(data, list) else None,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    except Exception as e:
        logger.error(f"导出数据失败: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/export_excel/<output_dir>')
def api_export_excel(output_dir):
    """导出Excel数据"""
    try:
        input_path = os.path.join("data/output", output_dir)
        
        # 创建分析器
        analyzer = AwardAnalyzer()
        analyzer.load_results(input_path)
        
        # 生成Excel文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_path = os.path.join("data/output", output_dir, f"export_{timestamp}.xlsx")
        
        with pd.ExcelWriter(excel_path) as writer:
            analyzer.awards_df.to_excel(writer, sheet_name='奖项数据', index=False)
            analyzer.projects_df.to_excel(writer, sheet_name='项目数据', index=False)
            analyzer.winners_df.to_excel(writer, sheet_name='获奖人数据', index=False)
        
        return send_file(
            excel_path,
            as_attachment=True,
            download_name=f"科技奖励数据_{timestamp}.xlsx"
        )
        
    except Exception as e:
        logger.error(f"导出Excel失败: {str(e)}")
        flash(f"导出Excel失败: {str(e)}", "danger")
        return redirect(url_for('analyze'))

@app.route('/data_quality/<input_dir>')
def data_quality(input_dir):
    """数据质量评估页面"""
    try:
        # 加载数据
        input_path = os.path.join("data/processed", input_dir)
        excel_path = os.path.join(input_path, "award_data.xlsx")
        
        # 读取Excel文件
        data = {}
        with pd.ExcelFile(excel_path) as xls:
            for sheet_name in xls.sheet_names:
                data[sheet_name] = pd.read_excel(xls, sheet_name)
        
        # 创建验证器
        validator = DataValidator()
        
        # 评估数据质量
        quality_metrics = validator.evaluate_data_quality(data)
        
        return render_template('quality.html',
                             title="数据质量评估",
                             quality_metrics=quality_metrics,
                             input_dir=input_dir)
                             
    except Exception as e:
        logger.error(f"数据质量评估失败: {str(e)}")
        flash(f"数据质量评估失败: {str(e)}", "danger")
        return redirect(url_for('process'))

@app.route('/api/quality/<input_dir>')
def api_quality(input_dir):
    """数据质量评估API"""
    try:
        # 加载数据
        input_path = os.path.join("data/processed", input_dir)
        excel_path = os.path.join(input_path, "award_data.xlsx")
        
        # 读取Excel文件
        data = {}
        with pd.ExcelFile(excel_path) as xls:
            for sheet_name in xls.sheet_names:
                data[sheet_name] = pd.read_excel(xls, sheet_name)
        
        # 创建验证器
        validator = DataValidator()
        
        # 评估数据质量
        quality_metrics = validator.evaluate_data_quality(data)
        
        return jsonify({
            "success": True,
            "data": quality_metrics,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    except Exception as e:
        logger.error(f"数据质量评估失败: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

# 启动应用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 