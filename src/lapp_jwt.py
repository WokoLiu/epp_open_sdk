# -*- coding: utf-8 -*-
# @Time    : 2018/11/14 14:31
# @Author  : Yulong Liu
# @File    : lapp_jwt.py

import jwt

public_key = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArDv5MYYa3kl5ymaPLCZm
LhR+b9O673mlvLj5WWd6WKD2FTT74u+u2T2UI8Uy0YHhFa8IxSXlZ7lT/GCOhZsI
mLGN9YuVsFLsInhmz89xcHWIRItNYHGP13m7bV2JotsW5necFnbX+fph4FHBXRIm
o+JG507WP4rk306uDX3Ag9xy3AI8TIYtVazlKz34bkkw3dLq6aBsKezkg5NkJqec
V/m/YMhTOUL+7bAVgljrPDRi+DdIl/Yh5h6SE43GotrfEu8WduTQWx1jknve4c+4
Vosx/1bGaDrPhHn3kc2ANWkL2CR3ekwPTyXy1gbGwWorMkiuOrZJ02wb/DO9hVzU
dQIDAQAB
-----END PUBLIC KEY-----'''

jwt_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NSwicmVmX2V4cCI6MTYxNzMxMzg3NSwiYXVkIjoiSU9ESkZJT0ozOEozMlBPQ0QwOUNKS0xXRTlMS0dNM1AiLCJhcHBuYW1lIjoic2t5ZmllbGQiLCJpc3MiOiJlcHAiLCJuYW1lX2NuIjoiXHU1ZjIwXHU0ZTA5IiwiYXZhdGFyIjoiaHR0cDovL2F2YXRhci5leGFtcGxlLmNvbS9hLmpwZyIsImV4cCI6MTYxNzIyNzQ3NSwiaWF0IjoxNTE3MTQxMDc1LCJuYW1lIjoic2FueiIsImVtcF9ubyI6IjE4MTMxMjM0NSJ9.VYbBds9_JepNviOUYSXqZ3qq-gvjaSKmg4YRb482l8skKT_eWZ7HNbNt9h66Etymg-41o1OZVBRxQGWHrvRBdYjbsH62ZTBuSY8iOYR8G3p_DSTD-BAm4XheUo4qtDx_JLR3bQ44IcBtBYDJcRVgTHH8ePcn70Sbipp3p05yORbL3TGfV-0aktuKNUkWPZtYde4oeBg886teKeZwqwVB6hSSAsWGe5rjg6nqk9b_TvfhEjOWOPv0CR1DUqgiExle2DSg2AG8ZfjD7VxEBOJgDRTOSXJTSS3OVA7ZLD7R4e2yuQCBiYHPuqQKYY43S7sdueBDN5nrG8Hn9UGQpjUSzA'

app_key = 'IODJFIOJ38J32POCD09CJKLWE9LKGM3P'

try:
    res = jwt.decode(jwt_token, public_key, audience=app_key)
except jwt.ExpiredSignatureError:
    print 'jwt过期'
except jwt.InvalidAudienceError:
    print 'app_key错误'
except jwt.InvalidSignatureError:
    print '公钥错误'
except jwt.DecodeError:
    print '其他错误'
else:
    print '成功'
    print res
