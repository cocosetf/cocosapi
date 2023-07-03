import threading

from flask import Flask,  request
from flask_restful import Api, Resource

import smc_sm_initialization
from smc_sm_ws import smc_sm_web_service as web_app

app = Flask(__name__)
api = Api(app)


class InitSystem(Resource):
    def post(self):
        if request.is_json:
            web_app_public_key = request.json['web_app_public_key']
            contact_url = request.json['contact_url']
            kk_session_key_nonce_enc = request.json['kk_session_key_nonce_enc']
            smc_sm_initialization.init_system(web_app_public_key, contact_url, kk_session_key_nonce_enc)
            enc_session_key, enc_nonce_1 = smc_sm_initialization.init_session_key()
            return {'enc_session_key': str(enc_session_key), 'enc_nonce_1': str(enc_nonce_1)}, 201
        else:
            return {'error': 'Request must be JSON'}, 400


class InitCrypto(Resource):
    def post(self):
        enc_svm_cert = request.files['enc_svm_cert']
        enc_svm_private_key = request.files['enc_svm_private_key']
        svm_cert, svm_private_key = smc_sm_initialization.decrypt_with_session_key(enc_svm_cert, enc_svm_private_key)
        svm_cert_filepath, svm_private_key_filepath = smc_sm_initialization.store_certificate_to_temp_memory(svm_cert, svm_private_key)
        threading.Thread(target=lambda: web_app.init_app(svm_cert_filepath, svm_private_key_filepath)).start()
        return {'success': True}, 201


api.add_resource(InitSystem, '/init-system')
api.add_resource(InitCrypto, '/init-crypto')
app.run(port=5050, debug=True, use_reloader=False)
