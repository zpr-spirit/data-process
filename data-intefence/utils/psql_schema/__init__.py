from app import db

class TransDetail(db.Model):
    __tablename__ = 'trans'  # 表名
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, age={self.age})>"