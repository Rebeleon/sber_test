from flask import Flask, request, jsonify
from pydantic import ValidationError
from decimal import *
from datetime import datetime
import json
from dateutil.relativedelta import relativedelta
from validator import DepositRequest


app = Flask(__name__)


@app.route('/calculate_deposit', methods=['POST'])
def calculate_deposit():
    try:
        deposit_request = DepositRequest.parse_obj(request.json)
    except ValidationError as e:
        error_dict = {e['loc'][0]: e['msg'] for e in e.errors()}
        return jsonify({'error': error_dict}), 400

    # Calculate the deposit
    result = {}
    deposit = Decimal(deposit_request.amount)
    for i in range(deposit_request.periods):
        t = datetime.strptime(deposit_request.date, "%d.%m.%Y") + relativedelta(months=i)
        t_str = t.strftime("%d.%m.%Y")
        deposit *= (1 + Decimal(deposit_request.rate) / 1200)
        result[t_str] = float(deposit.quantize(Decimal('.01')))
    json_obj = json.dumps(result, sort_keys=False)
    return json_obj, 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
