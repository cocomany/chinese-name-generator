import unittest
import os
import json
from unittest.mock import patch, MagicMock
from app.services.tts_service import synthesize_speech, ensure_audio_folder_exists
from config import Config

class TestTTSService(unittest.TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.test_text = "测试文本"
        self.test_audio_file = os.path.join(Config.AUDIO_FOLDER, 'test_speech.wav')
        
        # 确保测试目录存在
        ensure_audio_folder_exists()
        
        # 清理可能存在的测试文件
        if os.path.exists(self.test_audio_file):
            os.remove(self.test_audio_file)
    
    def tearDown(self):
        """测试后的清理工作"""
        if os.path.exists(self.test_audio_file):
            os.remove(self.test_audio_file)
    
    def test_ensure_audio_folder_exists(self):
        """测试音频文件夹创建功能"""
        # 确保文件夹存在
        ensure_audio_folder_exists()
        self.assertTrue(os.path.exists(Config.AUDIO_FOLDER))
        self.assertTrue(os.path.isdir(Config.AUDIO_FOLDER))
    
    @patch('dashscope.audio.tts.SpeechSynthesizer.call')
    def test_synthesize_speech_success(self, mock_call):
        """测试成功合成语音"""
        # 模拟成功响应
        mock_result = MagicMock()
        mock_result.get_audio_data.return_value = b'fake_audio_data'
        mock_call.return_value = mock_result
        
        # 调用合成函数
        output_file = synthesize_speech(self.test_text)
        
        # 验证调用参数
        mock_call.assert_called_once_with(
            model='sambert-zhichu-v1',
            text=self.test_text,
            sample_rate=48000
        )
        
        # 验证结果
        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(os.path.getsize(output_file) > 0)
    
    @patch('dashscope.audio.tts.SpeechSynthesizer.call')
    def test_synthesize_speech_no_audio_data(self, mock_call):
        """测试无音频数据的情况"""
        # 模拟响应但没有音频数据
        mock_result = MagicMock()
        mock_result.get_audio_data.return_value = None
        mock_call.return_value = mock_result
        
        # 验证错误处理
        with self.assertRaises(Exception) as context:
            synthesize_speech(self.test_text)
        
        self.assertIn("未获取到音频数据", str(context.exception))

if __name__ == '__main__':
    unittest.main() 