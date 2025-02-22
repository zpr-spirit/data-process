from . import db
from sqlalchemy import func

class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    signup_date = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'signup_date': self.signup_date,
            'amount': float(self.amount),  
            'timestamp': self.timestamp.isoformat()
        }
    
    @staticmethod
    def get_amount_sum_by_user(user_ids=[]):
        query = db.session.query(
            Transaction.user_id,
            func.sum(Transaction.amount).label('total_amount')
        )

        if user_ids:
            query = query.filter(Transaction.user_id.in_(user_ids))
        result = query.group_by(Transaction.user_id).order_by('user_id').all()

        return [{
            'user_id': row.user_id,
            'total_amount': float(row.total_amount) 
        } for row in result]