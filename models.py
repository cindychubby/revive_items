from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Item(db.Model):
    """
    物品模型：
    - id: 自增主键
    - name: 物品名（非空）
    - description: 物品描述（可空）
    - contact: 联系方式（可空）
    - created_at: 创建时间
    """
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    contact = db.Column(db.String(200), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "contact": self.contact,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<Item id={self.id} name={self.name!r}>"
