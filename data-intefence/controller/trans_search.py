from flask import Blueprint,jsonify
from datetime import datetime
from http import HTTPStatus
from webargs.flaskparser import use_args
from utils.request_schema import TransDetailSchema, TransSumSchema
from utils.psql_schema import TransDetail

router_trans = Blueprint('llm_qa', __name__)

@router_trans.route('/inteface/trans/detail', methods=['POST'])
@use_args(TransDetailSchema(), location="json")
def llm_qa(data):
    user = data.get('user', "")
    result = dict()
    trans_detail = TransDetail.query.all()
    return jsonify({'trans_detail': trans_detail,'timestamp':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'err_msg':''}), HTTPStatus.OK

@router_trans.route('/inteface/trans/summary', methods=['POST'])
@use_args(TransSumSchema(), location="json")
def llm_qa(data):
    users = data.get('users', [])
    result = dict()
    return jsonify({'answer':result,'timestamp':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'err_msg':''}), HTTPStatus.OK