from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, send_file
from app.services.name_generator import generate_chinese_name
from app.services.tts_service import generate_audio
from app.models.record import add_record, get_records, get_stats

main = Blueprint('main', __name__)

ADMIN_PASSWORD = 'hao123'  # 管理页面密码

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/generate', methods=['POST'])
def generate():
    data = request.json
    english_name = data.get('english_name', '')
    gender = data.get('gender', 'male')
    preferences = data.get('preferences', '')
    
    # 生成名字
    names = [generate_chinese_name(gender, preferences, english_name) for _ in range(3)]
    
    # 记录访问信息
    ip_address = request.remote_addr
    generated_names = ', '.join([f"{name['chinese_name']}({name['pinyin']})" for name in names])
    add_record(english_name, gender, preferences, generated_names, ip_address)
    
    return jsonify({'names': names})

@main.route('/audio/<name>')
def audio(name):
    try:
        audio_path = generate_audio(name)
        if audio_path:
            return '/' + audio_path  # 返回相对路径
        return 'Error generating audio', 500
    except Exception as e:
        return str(e), 500

@main.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('main.admin'))
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

@main.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('main.admin'))
