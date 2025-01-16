from datetime import datetime, timedelta
from app import db

class NameRecord(db.Model):
    __tablename__ = 'name_records'
    
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    preferences = db.Column(db.Text)
    generated_names = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def add_record(english_name, gender, preferences, generated_names, ip_address):
    record = NameRecord(
        english_name=english_name,
        gender=gender,
        preferences=preferences,
        generated_names=generated_names,
        ip_address=ip_address
    )
    db.session.add(record)
    db.session.commit()

def get_records():
    return NameRecord.query.order_by(NameRecord.created_at.desc()).all()

def get_stats():
    total_count = NameRecord.query.count()
    
    # 性别统计
    male_count = NameRecord.query.filter_by(gender='male').count()
    female_count = NameRecord.query.filter_by(gender='female').count()
    
    # 24小时内记录
    yesterday = datetime.utcnow() - timedelta(days=1)
    last_24h_count = NameRecord.query.filter(NameRecord.created_at >= yesterday).count()
    
    return {
        'total_count': total_count,
        'gender_stats': {
            'male': male_count,
            'female': female_count
        },
        'last_24h_count': last_24h_count
    } 