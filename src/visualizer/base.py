from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger

class BaseVisualizer:
    """可视化基类"""
    
    def __init__(self):
        """初始化可视化器"""
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 设置Seaborn样式
        sns.set_style("whitegrid")
        sns.set_palette("husl")
    
    def plot_bar(self, data: pd.DataFrame, x: str, y: str, title: str,
                xlabel: str = None, ylabel: str = None, figsize: Tuple[int, int] = (10, 6),
                rotation: int = 0, save_path: str = None) -> None:
        """
        绘制柱状图
        
        Args:
            data: 数据
            x: x轴字段
            y: y轴字段
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            figsize: 图表大小
            rotation: x轴标签旋转角度
            save_path: 保存路径
        """
        try:
            plt.figure(figsize=figsize)
            sns.barplot(data=data, x=x, y=y)
            
            plt.title(title)
            plt.xlabel(xlabel or x)
            plt.ylabel(ylabel or y)
            plt.xticks(rotation=rotation)
            
            if save_path:
                plt.savefig(save_path, bbox_inches='tight', dpi=300)
                plt.close()
            else:
                plt.show()
                
        except Exception as e:
            logger.error(f"绘制柱状图失败: {str(e)}")
    
    def plot_line(self, data: pd.DataFrame, x: str, y: str, title: str,
                 xlabel: str = None, ylabel: str = None, figsize: Tuple[int, int] = (10, 6),
                 rotation: int = 0, save_path: str = None) -> None:
        """
        绘制折线图
        
        Args:
            data: 数据
            x: x轴字段
            y: y轴字段
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            figsize: 图表大小
            rotation: x轴标签旋转角度
            save_path: 保存路径
        """
        try:
            plt.figure(figsize=figsize)
            sns.lineplot(data=data, x=x, y=y, markers=True, dashes=False)
            
            plt.title(title)
            plt.xlabel(xlabel or x)
            plt.ylabel(ylabel or y)
            plt.xticks(rotation=rotation)
            
            if save_path:
                plt.savefig(save_path, bbox_inches='tight', dpi=300)
                plt.close()
            else:
                plt.show()
                
        except Exception as e:
            logger.error(f"绘制折线图失败: {str(e)}")
    
    def plot_pie(self, data: pd.Series, title: str, figsize: Tuple[int, int] = (10, 10),
                save_path: str = None) -> None:
        """
        绘制饼图
        
        Args:
            data: 数据
            title: 图表标题
            figsize: 图表大小
            save_path: 保存路径
        """
        try:
            plt.figure(figsize=figsize)
            plt.pie(data.values, labels=data.index, autopct='%1.1f%%')
            
            plt.title(title)
            
            if save_path:
                plt.savefig(save_path, bbox_inches='tight', dpi=300)
                plt.close()
            else:
                plt.show()
                
        except Exception as e:
            logger.error(f"绘制饼图失败: {str(e)}")
    
    def plot_heatmap(self, data: pd.DataFrame, title: str,
                    figsize: Tuple[int, int] = (12, 8), save_path: str = None) -> None:
        """
        绘制热力图
        
        Args:
            data: 数据
            title: 图表标题
            figsize: 图表大小
            save_path: 保存路径
        """
        try:
            plt.figure(figsize=figsize)
            sns.heatmap(data, annot=True, fmt='.2f', cmap='YlOrRd')
            
            plt.title(title)
            
            if save_path:
                plt.savefig(save_path, bbox_inches='tight', dpi=300)
                plt.close()
            else:
                plt.show()
                
        except Exception as e:
            logger.error(f"绘制热力图失败: {str(e)}")
    
    def plot_scatter(self, data: pd.DataFrame, x: str, y: str, title: str,
                    xlabel: str = None, ylabel: str = None, figsize: Tuple[int, int] = (10, 6),
                    save_path: str = None) -> None:
        """
        绘制散点图
        
        Args:
            data: 数据
            x: x轴字段
            y: y轴字段
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            figsize: 图表大小
            save_path: 保存路径
        """
        try:
            plt.figure(figsize=figsize)
            sns.scatterplot(data=data, x=x, y=y)
            
            plt.title(title)
            plt.xlabel(xlabel or x)
            plt.ylabel(ylabel or y)
            
            if save_path:
                plt.savefig(save_path, bbox_inches='tight', dpi=300)
                plt.close()
            else:
                plt.show()
                
        except Exception as e:
            logger.error(f"绘制散点图失败: {str(e)}")
    
    def plot_box(self, data: pd.DataFrame, x: str, y: str, title: str,
                xlabel: str = None, ylabel: str = None, figsize: Tuple[int, int] = (10, 6),
                rotation: int = 0, save_path: str = None) -> None:
        """
        绘制箱线图
        
        Args:
            data: 数据
            x: x轴字段
            y: y轴字段
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            figsize: 图表大小
            rotation: x轴标签旋转角度
            save_path: 保存路径
        """
        try:
            plt.figure(figsize=figsize)
            sns.boxplot(data=data, x=x, y=y)
            
            plt.title(title)
            plt.xlabel(xlabel or x)
            plt.ylabel(ylabel or y)
            plt.xticks(rotation=rotation)
            
            if save_path:
                plt.savefig(save_path, bbox_inches='tight', dpi=300)
                plt.close()
            else:
                plt.show()
                
        except Exception as e:
            logger.error(f"绘制箱线图失败: {str(e)}")
    
    def plot_multiple(self, plots: List[Dict[str, Any]], title: str,
                     layout: Tuple[int, int], figsize: Tuple[int, int] = (15, 10),
                     save_path: str = None) -> None:
        """
        绘制多子图
        
        Args:
            plots: 子图配置列表
            title: 总标题
            layout: 子图布局
            figsize: 图表大小
            save_path: 保存路径
        """
        try:
            fig, axes = plt.subplots(layout[0], layout[1], figsize=figsize)
            fig.suptitle(title)
            
            for i, plot in enumerate(plots):
                row = i // layout[1]
                col = i % layout[1]
                ax = axes[row, col] if layout[0] > 1 and layout[1] > 1 else axes[i]
                
                plot_type = plot.get('type', 'line')
                data = plot.get('data')
                
                if plot_type == 'bar':
                    sns.barplot(data=data, x=plot.get('x'), y=plot.get('y'), ax=ax)
                elif plot_type == 'line':
                    sns.lineplot(data=data, x=plot.get('x'), y=plot.get('y'), ax=ax)
                elif plot_type == 'scatter':
                    sns.scatterplot(data=data, x=plot.get('x'), y=plot.get('y'), ax=ax)
                
                ax.set_title(plot.get('title', ''))
                ax.set_xlabel(plot.get('xlabel', ''))
                ax.set_ylabel(plot.get('ylabel', ''))
                
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, bbox_inches='tight', dpi=300)
                plt.close()
            else:
                plt.show()
                
        except Exception as e:
            logger.error(f"绘制多子图失败: {str(e)}") 