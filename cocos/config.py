import os.path

ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(ROOT_DIRECTORY, 'static', 'uploads')
DATA_DIRECTORY = os.path.join(UPLOAD_FOLDER, 'data')
CODE_DIRECTORY = os.path.join(UPLOAD_FOLDER, 'code')
ENC_CODE_FILENAME = 'enc_code'
CERT_DIRECTORY = os.path.join(UPLOAD_FOLDER, 'cert')

OUTPUT_DIRECTORY = 'output'
RESULT_PATH = os.path.join(OUTPUT_DIRECTORY, 'result')
