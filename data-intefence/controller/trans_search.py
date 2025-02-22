from flask import Blueprint,jsonify
from datetime import datetime
from http import HTTPStatus
from webargs.flaskparser import use_args
from app.utils import TransDetailSchema, TransSumSchema
from app.models import Transaction
import logging

logging.basicConfig(level=logging.DEBUG)

router_trans = Blueprint('transaction', __name__)

@router_trans.route('/inteface/trans/detail', methods=['POST'])
@use_args(TransDetailSchema(), location="json")
def search_trans_detail(data):
    user_id = data.get('user_id', "")
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    result = [transaction.to_dict() for transaction in transactions]
    logging.info(f"user_id is : {user_id}, search transaction detail success.")
    return jsonify({'trans_detail': result,'timestamp':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'err_msg':''}), HTTPStatus.OK

@router_trans.route('/inteface/trans/summary', methods=['POST'])
@use_args(TransSumSchema(), location="json")
def search_trans_summary(data):
    user_ids = data.get("user_ids", [])
    result = Transaction.get_amount_sum_by_user(user_ids)
    return jsonify({'answer':result,'timestamp':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'err_msg':''}), HTTPStatus.OK