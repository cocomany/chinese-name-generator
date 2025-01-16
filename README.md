# 中国名字生成器 (Chinese Name Generator)

一个帮助外国人取中文名字的网页应用。通过AI生成有意义的中文名字，并提供语音试听功能。

## 功能特点

- 🎯 基于个人信息生成定制化中文名字
- 🈺 所有内容中英文双语显示
- 🔊 提供中文名字的标准发音
- 📱 响应式设计，支持移动端访问
- 📊 访问统计和管理后台

## 技术栈

- 后端：Python + Flask
- 数据库：SQLite
- 前端：HTML5 + CSS3 + JavaScript
- UI框架：Bootstrap 5
- AI服务：阿里云通义千问 + 语音合成服务

## 本地开发

1. 克隆项目
```bash
git clone [项目地址]
cd chinese-name-generator
```

2. 创建并激活虚拟环境
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
创建 `.env` 文件并填入以下内容：
```env
SECRET_KEY=your-secret-key-here
DASHSCOPE_API_KEY=your-dashscope-api-key
```

5. 运行开发服务器
```bash
python run.py
```

访问 http://localhost:5000 即可使用应用。

## 部署指南

### 使用 Docker 部署

1. 构建镜像
```bash
docker build -t chinese-name-generator .
```

2. 运行容器
```bash
docker run -d -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e DASHSCOPE_API_KEY=your-api-key \
  chinese-name-generator
```

### 使用 Nginx + Gunicorn 部署

1. 安装 Gunicorn
```bash
pip install gunicorn
```

2. 创建 Gunicorn 配置文件 `gunicorn.conf.py`
```python
workers = 4
bind = '127.0.0.1:8000'
```

3. 配置 Nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/your/app/static;
    }
}
```

4. 启动应用
```bash
gunicorn -c gunicorn.conf.py run:app
```

### 使用 Supervisor 管理进程

1. 安装 Supervisor
```bash
apt-get install supervisor  # Ubuntu/Debian
```

2. 创建配置文件 `/etc/supervisor/conf.d/chinese-name-generator.conf`
```ini
[program:chinese-name-generator]
directory=/path/to/your/app
command=/path/to/venv/bin/gunicorn -c gunicorn.conf.py run:app
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/chinese-name-generator/err.log
stdout_logfile=/var/log/chinese-name-generator/out.log
```

3. 更新并启动服务
```bash
supervisorctl reread
supervisorctl update
supervisorctl start chinese-name-generator
```

## 管理后台

访问 `/admin` 路径进入管理后台，默认密码为 `hao123`。

管理后台功能：
- 查看访问统计
- 查看生成记录
- 性别比例分析
- 24小时访问量统计

## 项目结构
```
chinese_name_generator/
├── app/
│   ├── __init__.py          # 应用初始化
│   ├── routes.py            # 路由处理
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   └── record.py
│   ├── services/            # 业务服务
│   │   ├── __init__.py
│   │   ├── name_generator.py
│   │   └── tts_service.py
│   ├── templates/           # HTML模板
│   │   ├── index.html
│   │   └── admin.html
│   └── static/              # 静态文件
│       ├── css/
│       ├── js/
│       └── audio/
├── config.py                # 配置文件
├── requirements.txt         # 依赖包
└── run.py                   # 启动文件
```

## 注意事项

1. 需要阿里云账号和通义千问API密钥
2. 确保Python版本 >= 3.8
3. 音频文件会临时存储在 `app/static/audio` 目录
4. 建议定期清理音频文件
5. 生产环境部署时请修改管理后台密码

## 开发计划

- [ ] 添加更多中文名字生成策略
- [ ] 支持按五行八字生成名字
- [ ] 添加名字历史记录功能
- [ ] 支持导出名字卡片
- [ ] 添加更多语音合成声音选项
- [ ] 支持Docker容器化部署
- [ ] 添加API文档
- [ ] 优化数据库性能
- [ ] 添加单元测试

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件 