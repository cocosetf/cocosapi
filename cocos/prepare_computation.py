import os.path

from cryptography.fernet import Fernet

import smc_sm_ram_data
from computation import Computation
import config
import marshal


def get_python_code_from_bytes():
    f = Fernet(smc_sm_ram_data.code_keys[config.ENC_CODE_FILENAME])
    with open(os.path.join(config.CODE_DIRECTORY, config.ENC_CODE_FILENAME), "rb") as file:
        encrypted_data = file.read()
    bytes = f.decrypt(encrypted_data)
    code = marshal.loads(bytes)
    return code


def start_compute():
    comp = Computation.get_computation()
    comp.update_status()
    code = get_python_code_from_bytes()
    exec(code, {"data_keys": smc_sm_ram_data.data_keys, "result_keys": smc_sm_ram_data.result_keys, "RESULT_PATH": config.RESULT_PATH, "CODE_DIRECTORY": config.CODE_DIRECTORY, "DATA_DIRECTORY": config.DATA_DIRECTORY})
    comp.update_status()


def check_computation(username):
    for user in smc_sm_ram_data.users:
        u = smc_sm_ram_data.users[user]
        if not u.ready():
            return False
    smc_sm_ram_data.users[username].set_started_computation()
    return True
