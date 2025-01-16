# 中文名字生成器 (Chinese Name Generator)

## 项目概述 (Project Overview)
一个帮助外国人取中文名字的网页应用。用户可以输入一些基本信息，系统会通过AI生成合适的中文名字，并提供语音试听功能。所有内容采用中英双语显示。

## 核心功能 (Core Features)
1. 名字生成
   - 用户输入基本信息（性别、出生年月、喜好等）
   - 调用阿里云大模型API生成合适的中文名字
   - 展示名字的含义和文化背景

2. 语音试听
   - 使用阿里云TTS API进行中文名字的语音合成
   - 提供试听按钮，播放名字的标准中文发音

3. 双语显示
   - 所有界面内容同时显示中英文
   - 包括名字含义的中英文解释

## 技术栈 (Tech Stack)

### 后端 (Backend)
- 语言：Python 3.11+
- Web框架：Flask (轻量级，快速开发)
- 数据库：SQLite3 (文件型数据库，无需额外配置)
- API集成：
  - 阿里云智能语音服务 (TTS)
  - 阿里云通义千问大模型

### 前端 (Frontend)
- HTML5 + CSS3
- JavaScript (原生JS，不引入框架)
- Bootstrap 5 (响应式布局)
- Audio API (音频播放)

## 数据库设计 (Database Design)

### 名字记录表 (name_records)
```sql
CREATE TABLE name_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chinese_name TEXT NOT NULL,           -- 中文名
    pinyin TEXT NOT NULL,                 -- 拼音
    meaning TEXT NOT NULL,                -- 含义解释
    english_meaning TEXT NOT NULL,        -- 英文含义
    gender TEXT,                          -- 性别
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API设计 (API Design)

### 1. 生成名字 API
- 路径: `/api/generate_name`
- 方法: POST
- 请求参数:
  ```json
  {
    "gender": "string",      // male/female
    "birth_year": "string",  // 出生年份
    "preferences": "string"  // 个人喜好描述
  }
  ```
- 响应:
  ```json
  {
    "chinese_name": "string",
    "pinyin": "string",
    "meaning": "string",
    "english_meaning": "string"
  }
  ```

### 2. 语音合成 API
- 路径: `/api/synthesize_speech`
- 方法: POST
- 请求参数:
  ```json
  {
    "chinese_name": "string"
  }
  ```
- 响应: 音频文件 (MP3格式)

## 目录结构 (Project Structure)
```
chinese_name_generator/
├── app/
│   ├── __init__.py
│   ├── routes.py          # 路由处理
│   ├── models.py          # 数据模型
│   ├── services/
│   │   ├── name_generator.py    # 名字生成服务
│   │   └── tts_service.py       # 语音合成服务
│   └── templates/         # HTML模板
├── static/
│   ├── css/
│   ├── js/
│   └── audio/            # 临时音频文件存储
├── config.py             # 配置文件
├── requirements.txt      # 依赖包
└── run.py               # 启动文件
```

## 部署需求 (Deployment Requirements)
- Python 3.11+
- 阿里云账号及相关API密钥
  - 智能语音服务 (TTS) 访问密钥
  - 通义千问大模型 API密钥
- SQLite3数据库 