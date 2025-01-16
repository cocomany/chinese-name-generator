import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 阿里云配置
    DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')  # 通义千问API Key
    
    # 音频文件存储路径
    AUDIO_FOLDER = os.path.join('static', 'audio') 