from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# 初始化数据库
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    
    # 注册蓝图
    from app.routes import main
    app.register_blueprint(main)
    
    # 确保音频文件夹存在
    import os
    os.makedirs(os.path.join(app.static_folder, 'audio'), exist_ok=True)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app
