# coding=utf-8

import dashscope
from dashscope.audio.tts import SpeechSynthesizer

dashscope.api_key='sk-4cc8d187b0a34b65aeb8c37e1a90ed77'

result = SpeechSynthesizer.call(model='sambert-zhichu-v1',
                                text='今天天气怎么样',
                                sample_rate=48000)
if result.get_audio_data() is not None:
    with open('output.wav', 'wb') as f:
        f.write(result.get_audio_data())