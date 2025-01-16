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
        prompt_parts = ["""请你作为一个专业的中文起名专家，为一个外国人起一个独特的中文名字。

要求：
1. 名字发音与英文名相近, 要响亮、寓意好、易记
2. 要考虑中国传统文化内涵
3. 名字长度2-5个字
4. 名字要通俗易懂，不要过于深奥，不需要文采。避免生僻字
7. 特别有中国特色，包括但不限于中国的古语，地名，诗词，物件，历史人物，传说故事等"""]
        
        # 添加可选信息
        if english_name:
            prompt_parts.append(f"他/她的英文名是：{english_name}")
        if gender != '':
            prompt_parts.append(f"性别：{gender_text}")
        if preferences:
            prompt_parts.append(f"个人喜好和特点：{preferences}")
            
        # 添加生成要求
        prompt_parts.append("""
请按照以下JSON格式返回结果，不要返回其他内容：
{
    "chinese_name": "中文名",
    "pinyin": "拼音",
    "meaning": "名字的中文含义解释（100字以内）",
    "english_meaning": "名字的英文含义解释（200字以内）"
}

注意：
- 每次生成的名字必须独特且不同
- 名字要体现个人特点和文化内涵
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
            # 去掉API响应中的```json```标记
            json_text = response['output']['text'].replace('```json', '').replace('```', '').strip()
            result = json.loads(json_text)
            print(f"解析后的结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        except json.JSONDecodeError as e:
            print(f"JSON解析失败，原始内容: {response['output']['text']}")
            raise ValueError(f"API返回的JSON格式无效: {str(e)}")
            
        # 验证所需字段是否存在
        required_fields = ['chinese_name', 'pinyin', 'meaning', 'english_meaning']
        missing_fields = [field for field in required_fields if field not in result]
        if missing_fields:
            raise ValueError(f"API返回数据缺少必要字段: {', '.join(missing_fields)}")
            
        # 验证名字长度
        if not 2 <= len(result['chinese_name']) <= 5:
            raise ValueError(f"生成的名字长度不符合要求: {result['chinese_name']}")
            
        return result
        
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
            "temperature": 0.8,
            "top_p": 0.9,
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
