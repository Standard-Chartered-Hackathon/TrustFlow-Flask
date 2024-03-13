from flask import Flask, jsonify
import requests
from utils.aws_lambda_service_client import invoke_lambda


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/verify", methods=['GET'])
def get_kyc_info():
    api_endpoint = ""

    try:
        response = requests.get(api_endpoint)
        data = response.json()

        user_photo = data.get('imgUrl')
        user_aid = data.get('aadhaarCardNo')
        user_pan = data.get('panCardNo')

        data = {
            "user_aid": user_aid,
            "user_img_url": user_photo,
            "user_pid": user_pan
        }

        response = invoke_lambda(function_name="TrustFlow-KYC-Verification", data=data, invocation_type="RequestResponse")
        return jsonify(response)
    except Exception as E:
        raise E


if __name__ == '__main__':
    app.run(debug=True)
