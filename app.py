from flask import Flask, jsonify, request
import requests
from utils.aws_lambda_service_client import invoke_lambda
from utils.logger import LogType, log
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


TAG = "TrustFlow-Proto2"


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/verify", methods=['POST'])
def get_kyc_info():

    try:
        data = request.json

        user_photo = data.get('imgKey')
        user_aid = data.get('aadhaarCardNo')
        user_pan = data.get('panCardNo')

        data = {
            "user_aid": user_aid,
            "user_img_key": user_photo,
            "user_pid": user_pan
        }

        log(TAG, LogType.INFO, "Lambda invoked for: " + str(user_aid))
        response = invoke_lambda(function_name="TrustFlow-KYC-Verification", data=data, invocation_type="RequestResponse")
        return jsonify(response)
    except Exception as E:
        log(TAG, LogType.ERROR, "Error while invoking lambda: " + str(E))
        raise E


# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=4500)
