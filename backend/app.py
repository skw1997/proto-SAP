import sys
import os

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.web_app import app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)