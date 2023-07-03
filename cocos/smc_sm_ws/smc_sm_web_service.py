from flask import Flask,  request
from flask_restful import Resource, Api

from smc_sm import smc_sm_initialization
from user import User
import dashboard
import prepare_computation
import smc_sm_ram_data


class UserReader(Resource):
    def post(self):
        if request.is_json:
            for user in request.json['users']:
                new_user = User(username=user['username'],
                                provides_code=user['provides_code'],
                                provides_data=user['provides_data'],
                                uses_results=user['uses_results'],
                                is_supervisor=user['is_supervisor'])
                smc_sm_ram_data.users.update({new_user.username: new_user})
            return {'success': 'Attributes are successfully read'}, 201
        else:
            return {'error': 'Request must be JSON'}, 400


class AddCode(Resource):
    def post(self):
        username = request.form['username']
        code_file = request.files['code_file']
        code_key = request.form['code_key']
        dashboard.add_code(username, code_file, code_key)
        return {'success': True}, 201


class AddData(Resource):
    def post(self):
        username = request.form['username']
        file = request.files['data_file']
        key = request.form['data_key']
        dashboard.add_data(username, file, key)
        return {'success': True}, 201


class AddResultKey(Resource):
    def post(self):
        username = request.form['username']
        key = request.form['result_key']
        dashboard.add_result_key(username, key)
        return {'success': True}, 201


class CheckComputation(Resource):
    def post(self):
        if request.is_json:
            username = request.json['username']
            if prepare_computation.check_computation(username):
                return {'computation_status': True}, 201
            else:
                return {'computation_status': False}, 404
        else:
            return {'error': 'Request must be JSON'}, 400


class StartComputation(Resource):
    def get(self):
        prepare_computation.start_compute()
        return {'computation_done': True}, 201


def init_app(svm_cert_filepath, svm_private_key_filepath):
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(UserReader, '/read-users')
    api.add_resource(AddCode, '/add-code')
    api.add_resource(AddData, '/add-data')
    api.add_resource(AddResultKey, '/add-result-key')
    api.add_resource(CheckComputation, '/check-computation')
    api.add_resource(StartComputation, '/start-computation')

    app.run(port=5051, debug=True, use_reloader=False, ssl_context=(svm_cert_filepath, svm_private_key_filepath))
