document.addEventListener('DOMContentLoaded', function() {
    const nameForm = document.getElementById('nameForm');
    const generateBtn = document.getElementById('generateBtn');
    const resultCard = document.getElementById('resultCard');

    nameForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // 显示加载状态
        generateBtn.querySelector('.normal-text').classList.add('d-none');
        generateBtn.querySelector('.loading-text').classList.remove('d-none');
        generateBtn.disabled = true;

        try {
            // 获取表单数据
            const englishName = document.getElementById('englishName').value;
            const gender = document.querySelector('input[name="gender"]:checked').value;
            const preferences = document.getElementById('preferences').value;

            // 发送请求
            const response = await fetch('/api/generate_name', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    english_name: englishName,
                    gender: gender,
                    preferences: preferences
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // 显示结果
            resultCard.classList.remove('d-none');
            
            // 更新三个名字选项
            data.names.forEach((name, index) => {
                const num = index + 1;
                document.getElementById(`chineseName${num}`).textContent = name.chinese_name;
                document.getElementById(`pinyinName${num}`).textContent = name.pinyin;
                document.getElementById(`meaning${num}`).textContent = name.meaning;
                document.getElementById(`englishMeaning${num}`).textContent = name.english_meaning;
            });

            // 滚动到结果区域
            resultCard.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error('Error:', error);
            alert('生成名字时出错，请重试。');
        } finally {
            // 恢复按钮状态
            generateBtn.querySelector('.normal-text').classList.remove('d-none');
            generateBtn.querySelector('.loading-text').classList.add('d-none');
            generateBtn.disabled = false;
        }
    });
});

// 音频缓存Map
const audioCache = new Map();

// 播放音频
async function playAudio(index) {
    const playBtn = document.querySelector(`#chineseName${index}`).closest('.name-option').querySelector('.btn-outline-primary');
    const originalText = playBtn.innerHTML;
    
    try {
        // 显示加载状态
        playBtn.disabled = true;
        playBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 加载中...';
        
        const chineseName = document.getElementById(`chineseName${index}`).textContent;
        const gender = document.querySelector('input[name="gender"]:checked').value;
        const cacheKey = `${chineseName}-${gender}`;
        
        let audioPath;
        
        // 检查缓存
        if (audioCache.has(cacheKey)) {
            console.log('使用缓存的音频路径:', cacheKey);
            audioPath = audioCache.get(cacheKey);
        } else {
            // 缓存中没有，从服务器获取
            console.log('从服务器获取音频:', cacheKey);
            const response = await fetch(`/audio/${encodeURIComponent(chineseName)}?gender=${gender}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            audioPath = await response.text();
            // 存入缓存
            audioCache.set(cacheKey, audioPath);
        }
        
        const audio = new Audio(audioPath);
        
        // 播放完成后恢复按钮状态
        audio.onended = () => {
            playBtn.disabled = false;
            playBtn.innerHTML = originalText;
        };
        
        // 播放出错时恢复按钮状态
        audio.onerror = () => {
            playBtn.disabled = false;
            playBtn.innerHTML = originalText;
            alert('播放音频时出错，请重试。');
        };
        
        await audio.play();
    } catch (error) {
        console.error('Error playing audio:', error);
        alert('播放音频时出错，请重试。');
        // 恢复按钮状态
        playBtn.disabled = false;
        playBtn.innerHTML = originalText;
    }
} 