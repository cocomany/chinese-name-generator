from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, send_file
from app import db
from app.models.record import NameRecord, add_record, get_records, get_stats
from app.services.name_generator import generate_chinese_name
from app.services.tts_service import generate_audio
from config import Config

main = Blueprint('main', __name__)

# 从配置中获取管理密码
ADMIN_PASSWORD = Config.ADMIN_PASSWORD

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/generate_name', methods=['POST'])
def generate_name():
    try:
        data = request.get_json()
        english_name = data.get('english_name', '')
        gender = data.get('gender', '')
        preferences = data.get('preferences', '')
        
        # 调用名字生成服务，一次性生成3个名字
        names = generate_chinese_name(
            gender=gender,
            preferences=preferences,
            english_name=english_name
        )
        
        # 记录访问信息
        ip_address = request.remote_addr
        generated_names = ', '.join([f"{name['chinese_name']}({name['pinyin']})" for name in names])
        add_record(english_name, gender, preferences, generated_names, ip_address)
        
        # 返回生成的名字
        return jsonify({'names': names})
    
    except Exception as e:
        print(f"生成名字时出错: {str(e)}")  # 添加错误日志
        return jsonify({'error': str(e)}), 500

@main.route('/audio/<name>')
def audio(name):
    try:
        # 从查询参数中获取性别
        gender = request.args.get('gender', '')
        audio_path = generate_audio(name, gender)
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
