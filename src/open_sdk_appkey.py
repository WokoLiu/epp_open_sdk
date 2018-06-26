# -*- coding: utf-8 -*-
# @Time    : 2018/5/31 17:59
# @Author  : Yulong Liu
# @File    : open_sdk_appkey.py

import requests
import time
import random
import string
from hashlib import md5
from Crypto.Cipher import AES


class OpenAuth(object):
    """处理开放平台的签名和加密"""
    def __init__(self, app_key, app_secret):
        """
        :param app_secret: must be either 16, 24, 32 bytes long
        """
        self._app_key = app_key
        self._app_secret = app_secret

    def encode(self, text):
        """AES encrypt"""
        cryptor = AES.new(self._app_secret, AES.MODE_ECB, AES.block_size*'\0')
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        return cryptor.encrypt(pad(text)).encode('hex')

    def decode(self, text):
        """AES decrypt"""
        cryptor = AES.new(self._app_secret, AES.MODE_ECB, AES.block_size*'\0')
        res = cryptor.decrypt(text.decode('hex'))
        unpad = lambda s: s[0:-ord(s[-1])]
        return unpad(res)

    def get_headers(self, method, url, portal_name, params):
        """add common params and sign to headers"""
        method = method.upper()
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        timestamp = int(time.time())

        headers = {
            'PortalName': portal_name,
            'Salt': salt,
            'TimeStamp': str(timestamp),
            'AppKey': self._app_key,
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
        sign_str = ':'.join((method, url, params_str, self._app_secret))
        return md5(sign_str).hexdigest()


def demo_request(host):
    app_key = 'app_key_tttttttttttttttttttttttt'
    app_secret = 'app_secret_ttttttttttttttttttttt'
    portal_name = 'skyfield'
    api = '/api/open_external_service/demo/demo'
    auth = OpenAuth(app_key, app_secret)

    params = {
        'int_test': 100,
        'float_test': 3.14,
        'str_test': 'something',
        'chinese_test': '中文',
        'bool_test': True,
        'encode_test': auth.encode('加密测试').upper(),
        'decode_test': '解密测试',
    }

    # print auth.encode('加密测试')

    headers = auth.get_headers('post', api, portal_name, params)

    res = requests.post(host+api, params=params, headers=headers)
    print res.text
    data = res.json()
    decode_test = data.get('result', {}).get('decode_test', '')
    if decode_test:
        print auth.decode(decode_test)

if __name__ == '__main__':
    host = 'https://openapi.hillinsight.com:59687'
    demo_request(host)
