# -*- coding: utf-8 -*-
# @Time    : 2018/5/23 09:44
# @Author  : Yulong Liu
# @File    : open_sdk.py

import requests
import time
import random
import string
from hashlib import md5
from Crypto.Cipher import AES


class OpenAuth(object):
    """处理开放平台的签名和加密"""
    def __init__(self, auth_key, auth_secret):
        """
        :param auth_secret: must be either 16, 24, 32 bytes long
        """
        self._auth_key = auth_key
        self._auth_secret = auth_secret

    def encode(self, text):
        """AES encrypt"""
        cryptor = AES.new(self._auth_secret, AES.MODE_ECB, AES.block_size * '\0')
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        return cryptor.encrypt(pad(text)).encode('hex')

    def get_headers(self, method, url, portal_name, params):
        """add common params and sign to headers"""
        method = method.upper()
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        timestamp = int(time.time())

        headers = {
            'PortalName': portal_name,
            'Salt': salt,
            'TimeStamp': str(timestamp),
            'AuthKey': self._auth_key,
        }
        sign_params = {k: v for k, v in params.iteritems()}
        sign_params.update(headers)
        headers['Sign'] = self._make_sign(method, url, sign_params)

        return headers

    def _make_sign(self, method, url, params):
        """make sign with params"""
        params_str = ''
        params_name = params.keys()
        params_name.sort()
        for k in params_name:
            params_str += str(k) + '=' + str(params[k])
        sign_str = ':'.join((method, url, params_str, self._auth_secret))
        return md5(sign_str).hexdigest()


def demo_request(host):
    auth_key = 'AuthKeyTest'
    auth_secret = 'AuthSecretTest01'
    portal_name = 'topsports'
    auth = OpenAuth(auth_key, auth_secret)

    params = {
        'int_test': 100,
        'float_test': 3.14,
        'str_test': 'something',
        'chinese_test': '中文',
        'bool_test': True,
        'encode_test': auth.encode('中文+english'),
    }
    url = host + '/api/open_external_service/demo/demo'

    headers = auth.get_headers(
        'get', '/api/open_external_service/demo/demo', portal_name, params)

    res = requests.get(url, params=params, headers=headers)
    print res.text

if __name__ == '__main__':
    # host = 'https://openapi.hillinsight.com'
    host = 'http://0.0.0.0:4488'
    demo_request(host)
