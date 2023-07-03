import base64
import os.path
import random

import fs
import rsa

import config
import smc_sm_ram_data
from cryptography.fernet import Fernet
import sys
sys.path.insert(1, '../')


def init_system(web_app_public_key, contact_url, kk_session_key_nonce_enc):
    smc_sm_ram_data.kk_session_key_nonce_enc = kk_session_key_nonce_enc
    smc_sm_ram_data.contact_url = contact_url
    smc_sm_ram_data.web_app_public_key = rsa.PublicKey.load_pkcs1_openssl_der(base64.b64decode(web_app_public_key))


def init_session_key():
    smc_sm_ram_data.session_key = Fernet.generate_key()
    smc_sm_ram_data.nonce_1 = random.randbytes(32)
    enc_session_key = rsa.encrypt(smc_sm_ram_data.session_key, smc_sm_ram_data.web_app_public_key)
    enc_nonce_1 = rsa.encrypt(smc_sm_ram_data.nonce_1, smc_sm_ram_data.web_app_public_key)
    return enc_session_key, enc_nonce_1


# for testing purposes
def init_session_key_test():
    smc_sm_ram_data.session_key = b'AVT50EP4pIlFBuUtqYC2Qj5ly_dcurmxq40gVEM8Y60='
    smc_sm_ram_data.nonce_1 = random.randbytes(32)
    enc_session_key = rsa.encrypt(smc_sm_ram_data.session_key, smc_sm_ram_data.web_app_public_key)
    enc_nonce_1 = rsa.encrypt(smc_sm_ram_data.nonce_1, smc_sm_ram_data.web_app_public_key)
    return enc_session_key, enc_nonce_1


def decrypt_with_session_key(enc_svm_cert, enc_svm_private_key):
    session_key = smc_sm_ram_data.session_key
    cipher_suite = Fernet(session_key)
    enc_svm_cert_filepath = os.path.join(config.ROOT_DIRECTORY, os.path.join(config.CERT_DIRECTORY, enc_svm_cert.filename))
    enc_svm_private_key_filepath = os.path.join(config.ROOT_DIRECTORY, os.path.join(config.CERT_DIRECTORY, enc_svm_private_key.filename))
    enc_svm_cert.save(enc_svm_cert_filepath)
    enc_svm_private_key.save(enc_svm_private_key_filepath)
    with open(enc_svm_cert_filepath, "rb") as in_file:
        svm_cert = cipher_suite.decrypt(in_file.read()).decode("utf-8")
    with open(enc_svm_private_key_filepath, "rb") as in_file:
        svm_private_key = cipher_suite.decrypt(in_file.read()).decode("utf-8")
    return svm_cert, svm_private_key


def store_certificate_to_temp_memory(svm_cert, svm_private_key):
    temp_mem_root = "mem://"
    mem_fs = fs.open_fs(temp_mem_root)
    cert_directory = "cert"
    mem_fs.makedir(cert_directory)
    svm_cert_filepath = os.path.join(cert_directory, "svm_cert.pem")
    svm_private_key_filepath = os.path.join(cert_directory, "svm_private_key.pem")
    mem_fs.writetext(svm_cert_filepath, svm_cert)
    mem_fs.writetext(svm_private_key_filepath, svm_private_key)
    return os.path.join(temp_mem_root, svm_cert_filepath), os.path.join(temp_mem_root, svm_private_key_filepath)
