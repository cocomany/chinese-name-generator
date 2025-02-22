import os
import time
import json
import glob
import dashscope
from dashscope.audio.tts import SpeechSynthesizer
from config import Config
from flask import current_app

def ensure_audio_folder_exists():
    """确保音频文件夹存在"""
    # 使用app/static/audio路径
    audio_folder = os.path.join('app', 'static', 'audio')
    os.makedirs(audio_folder, exist_ok=True)
    return audio_folder

def cleanup_old_audio_files(hours=1):
    """清理指定小时数之前的音频文件"""
    try:
        current_time = time.time()
        audio_folder = ensure_audio_folder_exists()
        # 获取所有wav文件
        pattern = os.path.join(audio_folder, 'speech_*.wav')
        for file_path in glob.glob(pattern):
            try:
                # 获取文件修改时间
                file_mtime = os.path.getmtime(file_path)
                # 如果文件超过指定时间
                if current_time - file_mtime > hours * 3600:
                    os.remove(file_path)
                    print(f"已删除旧音频文件: {file_path}")
            except Exception as e:
                print(f"删除文件 {file_path} 时出错: {str(e)}")
    except Exception as e:
        print(f"清理音频文件时出错: {str(e)}")

# 确保音频文件夹存在
AUDIO_FOLDER = ensure_audio_folder_exists()

# 设置API Key
dashscope.api_key = Config.DASHSCOPE_API_KEY

# 定义音色配置
VOICE_CONFIG = {
    'female': {
        'model': 'sambert-zhiqi-v1',   # 温柔女声
        'sample_rate': 48000
    },
    'male': {
        'model': 'sambert-zhixiang-v1', # 磁性男声
        'sample_rate': 48000
    }
}

def synthesize_speech(text, gender=''):
    """
    使用阿里云通义千问语音合成服务生成语音
    """
    try:
        # 先清理旧文件
        cleanup_old_audio_files()
        
        # 根据性别选择音色
        voice_config = VOICE_CONFIG['female'] if gender == 'female' else VOICE_CONFIG['male']
        
        # 生成唯一的音频文件名
        timestamp = int(time.time())
        audio_file = os.path.join(AUDIO_FOLDER, f'speech_{timestamp}.wav')
        
        # 调用语音合成
        result = SpeechSynthesizer.call(
            model=voice_config['model'],
            text=text,
            sample_rate=voice_config['sample_rate']
        )
        
        # 检查音频数据
        audio_data = result.get_audio_data()
        if audio_data is not None:
            # 保存音频文件
            with open(audio_file, 'wb') as f:
                f.write(audio_data)
            # 返回相对于static文件夹的路径
            return 'static/audio/speech_{}.wav'.format(timestamp)
        else:
            raise Exception("语音合成失败：未获取到音频数据")
        
    except Exception as e:
        error_msg = str(e)
        if not error_msg.startswith("语音合成失败"):
            error_msg = f"语音合成失败: {error_msg}"
        print(f"TTS API error: {error_msg}")
        raise Exception(error_msg)

def generate_audio(text, gender=''):
    """
    生成音频文件并返回文件路径
    """
    try:
        audio_path = synthesize_speech(text, gender)
        return audio_path
    except Exception as e:
        print(f"生成音频失败: {str(e)}")
        return None