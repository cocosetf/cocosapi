import os

import config
from smc_sm_ram_data import data_keys, users, result_keys, code_keys

from werkzeug.utils import secure_filename


def save_code_file(file):
    file.save(os.path.join(config.CODE_DIRECTORY, config.ENC_CODE_FILENAME))


def add_data_file(file, filename):
    file.save(os.path.join(config.DATA_DIRECTORY, filename))


def add_code(username, file, key):
    code_keys.update({config.ENC_CODE_FILENAME: key})
    save_code_file(file)
    users[username].set_code_submitted()


def add_data(username, file, key):
    input_filename = secure_filename(file.filename)
    filename = username.join(input_filename)
    data_keys.update({filename: key})
    add_data_file(file, filename)
    users[username].set_data_submitted()


def add_result_key(username, key):
    result_keys.update({username: key})
    users[username].set_result_key_submitted()
