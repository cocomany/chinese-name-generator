from datetime import datetime
from app import db

class NameRecord(db.Model):
    __tablename__ = 'name_records'
    
    id = db.Column(db.Integer, primary_key=True)
    chinese_name = db.Column(db.String(10), nullable=False)
    pinyin = db.Column(db.String(50), nullable=False)
    meaning = db.Column(db.Text, nullable=False)
    english_meaning = db.Column(db.Text, nullable=False)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'chinese_name': self.chinese_name,
            'pinyin': self.pinyin,
            'meaning': self.meaning,
            'english_meaning': self.english_meaning,
            'gender': self.gender,
            'created_at': self.created_at.isoformat()
        } 