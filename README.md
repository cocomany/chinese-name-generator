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

## 快速开始

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

4. 配置环境变量（重要！）
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入你的API密钥
# 必须配置DASHSCOPE_API_KEY，否则无法使用！
```

5. 运行应用
```bash
python run.py
```

访问 http://localhost:5000 即可使用应用。

## 项目结构
```
chinese_name_generator/
├── app/
│   ├── __init__.py          # 应用初始化
│   ├── routes.py            # 路由处理
│   ├── models/              # 数据模型
│   ├── services/            # 业务服务
│   ├── templates/           # HTML模板
│   └── static/              # 静态文件
├── config.py                # 配置文件
├── requirements.txt         # 依赖包
├── .env.example            # 环境变量模板
└── run.py                  # 启动文件
```

## 管理后台

访问 `/admin` 路径进入管理后台，默认密码为 `hao123`。

管理后台功能：
- 查看访问统计
- 查看生成记录
- 性别比例分析
- 24小时访问量统计

## 注意事项

1. **必须配置环境变量**：
   - 复制 `.env.example` 到 `.env`
   - 在 `.env` 中填入你的通义千问API密钥
   - 没有API密钥？访问[阿里云通义千问](https://dashscope.aliyun.com/)控制台申请

2. 其他注意事项：
   - 确保Python版本 >= 3.8
   - 音频文件会临时存储在 `app/static/audio` 目录
   - 建议定期清理音频文件
   - 生产环境部署时请修改管理后台密码

## 开发计划

- [ ] 添加更多中文名字生成策略
- [ ] 支持按五行八字生成名字
- [ ] 添加名字历史记录功能
- [ ] 支持导出名字卡片
- [ ] 添加更多语音合成声音选项
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