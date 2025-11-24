#!/usr/bin/env python3
"""
运行PDF导入前端界面的脚本
"""

import subprocess
import sys
import os

def main():
    """启动Streamlit应用"""
    try:
        # 获取当前脚本目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 构建应用路径
        app_path = os.path.join(current_dir, "pdf_import_ui.py")
        
        # 检查应用文件是否存在
        if not os.path.exists(app_path):
            print(f"错误: 找不到应用文件 {app_path}")
            sys.exit(1)
        
        # 启动Streamlit应用
        print("正在启动PDF导入前端界面...")
        print("请在浏览器中打开显示的地址")
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_path
        ])
        
    except KeyboardInterrupt:
        print("\n应用已停止")
    except Exception as e:
        print(f"启动应用时出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()