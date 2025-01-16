import os
import json
import requests
import pinyin
from config import Config

def generate_chinese_name(gender, preferences, english_name=''):
    """
    使用阿里云通义千问大模型生成中文名字
    """
    try:
        # 构建性别文本
        gender_text = "男" if gender == "male" else "女" if gender == "female" else "未指定"
        
        print(f"开始生成名字，参数: gender={gender}, preferences={preferences}, english_name={english_name}")
        
        # 构建提示词
        prompt_parts = ["""请你作为一个专业的中文起名专家，为一个外国人生成3个特别简单的中文名字。

### 取名基本原则

1. **发音相近原则**
- 尽量选择与原名发音相近的汉字
- 避免使用生僻字，确保读音自然顺口

2. **字义美好原则**
- 选择含义积极、典雅的汉字
- 避免负面或不雅的含义
- 注意文化内涵

3. **约定俗成原则**
- 有很多名字已经约定俗成，比如"马克"，"大卫"，"奥黛丽"，"李安"等
- 姓氏尽量选用常见的单字中国姓氏

4. **性别适配原则**
- 男性名字偏阳刚、气势
- 女性名字偏优雅、柔美

### 优秀案例：

1. **马克·扎克伯格 (Mark Zuckerberg)**
- 姓"马"对应"M"音
- "克"对应"k"音
- 简单易记，符合中文习惯

2. **大卫·贝克汉姆 (David Beckham)**
- "贝克汉姆"音译自然
- 读音朗朗上口
- 避免了生僻字

3. **史蒂芬·库里 (Stephen Curry)**
- "史蒂芬"已成为约定俗成的译名
- "库里"简单好记

4. **奥黛丽·赫本 (Audrey Hepburn)**
- "奥黛丽"优雅feminine
- 音译自然，符合原名发音

5. **李安 (Ang Lee)**
- 完美示范了简洁原则
- 保留了原有姓氏的发音特点
- 体现了中文名字的简约美
                        
"""]
        
        # 添加可选信息
        if english_name:
            prompt_parts.append(f"他/她的英文名是：{english_name}")
        if gender != '':
            prompt_parts.append(f"性别：{gender_text}")
        if preferences:
            prompt_parts.append(f"个人喜好和特点：{preferences}")
            
        # 添加生成要求
        prompt_parts.append("""
请按照以下JSON格式返回3个名字，不要返回其他内容：
{
    "names": [
        {
            "chinese_name": "第一个中文名",
            "pinyin": "拼音",
            "meaning": "名字的中文含义解释（100字以内）",
            "english_meaning": "名字的英文含义解释（200字以内）"
        },
        {
            "chinese_name": "第二个中文名",
            "pinyin": "拼音",
            "meaning": "名字的中文含义解释（100字以内）",
            "english_meaning": "名字的英文含义解释（200字以内）"
        },
        {
            "chinese_name": "第三个中文名",
            "pinyin": "拼音",
            "meaning": "名字的中文含义解释（100字以内）",
            "english_meaning": "名字的英文含义解释（200字以内）"
        }
    ]
}

注意：
- 这3个名字必须完全不同
- 每个名字都要体现个人特点和文化内涵
- 解释要简洁明了，突出名字的特色
""")
        
        # 组合完整提示词
        prompt = "\n".join(prompt_parts)
        
        # 调用通义千问API
        response = call_dashscope_api(prompt)
        
        print(f"API调用成功，开始解析响应...")
        
        # 解析API响应
        if not response:
            raise ValueError("API返回为空")
            
        if 'output' not in response:
            print(f"API完整响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
            raise ValueError("API返回数据格式错误：未找到output字段")
            
        print(f"API输出内容: {response['output']}")
        
        try:
            # 提取JSON内容 - 更健壮的方式处理markdown格式
            json_text = response['output']['text']
            # 找到JSON内容的起始和结束位置
            start = json_text.find('{')
            end = json_text.rfind('}') + 1
            if start == -1 or end == 0:
                raise ValueError("未找到有效的JSON内容")
            
            # 只提取JSON部分
            json_content = json_text[start:end]
            result = json.loads(json_content)
            print(f"解析后的结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        except json.JSONDecodeError as e:
            print(f"JSON解析失败，提取的内容: {json_content}")
            raise ValueError(f"API返回的JSON格式无效: {str(e)}")
            
        # 验证返回的数据结构
        if 'names' not in result or not isinstance(result['names'], list) or len(result['names']) != 3:
            raise ValueError("API返回数据格式错误：未找到names数组或数组长度不为3")
            
        # 验证每个名字的字段
        required_fields = ['chinese_name', 'pinyin', 'meaning', 'english_meaning']
        for i, name_data in enumerate(result['names']):
            missing_fields = [field for field in required_fields if field not in name_data]
            if missing_fields:
                raise ValueError(f"第{i+1}个名字缺少必要字段: {', '.join(missing_fields)}")
                
            # 验证名字长度
            if not 2 <= len(name_data['chinese_name']) <= 10:
                raise ValueError(f"第{i+1}个名字长度不符合要求: {name_data['chinese_name']}")
            
        return result['names']
        
    except Exception as e:
        error_msg = f"生成名字时发生错误: {str(e)}"
        print(f"错误详情: {error_msg}")
        raise Exception(error_msg)

def call_dashscope_api(prompt):
    """
    调用阿里云通义千问API
    """
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {Config.DASHSCOPE_API_KEY}",
        "Content-Type": "application/json",
        "X-DashScope-SSE": "disable"
    }
    
    data = {
        "model": "qwen-turbo",
        "parameters": {
            "temperature": 0.9,
            "seed": int.from_bytes(os.urandom(4), byteorder='big'),
            "result_format": "text"
        },
        "input": {
            "prompt": prompt
        }
    }
    
    try:
        print(f"正在调用API，请求数据: {json.dumps(data, ensure_ascii=False)}")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        # 打印原始响应内容
        print(f"API原始响应: {response.text}")
        
        # 检查响应状态码
        if response.status_code != 200:
            error_msg = f"API请求失败，状态码: {response.status_code}, 响应内容: {response.text}"
            print(error_msg)
            raise Exception(error_msg)
            
        # 尝试解析JSON响应
        try:
            response_json = response.json()
            print(f"API响应解析结果: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
            
            # 检查API错误信息
            if 'code' in response_json and response_json['code'] != "200":
                error_msg = f"API返回错误: {response_json.get('message', '未知错误')}"
                print(error_msg)
                raise Exception(error_msg)
                
            return response_json
            
        except json.JSONDecodeError as e:
            error_msg = f"API响应不是有效的JSON格式: {str(e)}\n响应内容: {response.text}"
            print(error_msg)
            raise ValueError(error_msg)
            
    except requests.exceptions.RequestException as e:
        error_msg = f"API请求异常: {str(e)}"
        if response := getattr(e, 'response', None):
            error_msg += f"\nAPI响应内容: {response.text}"
        print(error_msg)
        raise Exception(error_msg)
