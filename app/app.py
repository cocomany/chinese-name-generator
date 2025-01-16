from flask import Flask, render_template, request, jsonify, session
from services.name_generator import generate_names
from services.tts_service import generate_audio
from models.record import init_db, add_record, get_records, get_stats
import os
from config import Config  # 添加这行

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 用于session加密
# 从环境变量获取管理密码，如果未设置则使用默认值
ADMIN_PASSWORD = Config.ADMIN_PASSWORD

# 确保数据库和表存在
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    english_name = data.get('english_name', '')
    gender = data.get('gender', 'male')
    preferences = data.get('preferences', '')
    
    # 生成名字
    names = generate_names(english_name, gender, preferences)
    
    # 记录访问信息
    ip_address = request.remote_addr
    generated_names = ', '.join([f"{name['chinese']}({name['pinyin']})" for name in names])
    add_record(english_name, gender, preferences, generated_names, ip_address)
    
    return jsonify({'names': names})

@app.route('/audio/<name>')
def audio(name):
    audio_data = generate_audio(name)
    return audio_data

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['authenticated'] = True
        else:
            return '密码错误', 401
    
    authenticated = session.get('authenticated', False)
    if not authenticated:
        return render_template('admin.html', authenticated=False)
    
    stats = get_stats()
    records = get_records()
    return render_template('admin.html', 
                         authenticated=True,
                         stats=stats,
                         records=records)

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True) 