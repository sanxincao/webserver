from datetime import datetime
from json import dumps as json_dumps, loads as json_loads
from hashlib import sha1, sha256
from base64 import b64encode as base64_encode, b64decode as base64_decode
import os
import sys
from time import time
from fastapi import APIRouter, Body, Depends, File, UploadFile, Form, requests, responses
from common import add_salt, success, Error,generate_function_and_component_list
from pydantic import BaseModel
import config
import crud


router = APIRouter()
'Electron程序所使用的接口'


def check_token(token: str = Body(..., embed=True)):
    '检查token是否合法，若校验通过，返回token中携带的信息'
    token = token.split('.')
    if len(token) != 3:
        raise Error(21)
    signature_server = token[1]
    signature_client = token[2]
    if len(signature_server) != 64 or len(signature_client) != 64:
        raise Error(22)
    if signature_server != sha256(add_salt(token[0], 0).encode()).hexdigest():
        raise Error(23)
    try:
        token = json_loads(base64_decode(token[0]))
    except BaseException:
        raise Error(24)
    return token




@router.post('/')
def root():
    '根路由'
    return success()

@router.post('/register')
def register(email=Body(...)):
    '注册接口'
    res=crud.create_user(email)
    if res[0]==False:
        raise Error(10)
    if res[0]==True:
        return success({"message":res[1]})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    

@router.post('/login')
def login(email=Body(...), password=Body(...), device_id=Body(...)):
    '''
    登录系统，分发token
    需要满足：账户有效且存在，处于有效期内，密码输入正确，设备id属于已授权设备列表，或设备id不在已授权设备列表中但已授权设备总数未达上限（此时会自动添加）
    '''
    
    res = crud.get_user(email)
    if res is None:
        raise Error(11)
   
    token = {
        "email": email,
        "login_time": time(),
        "expire": res['expire_time'].timestamp()
    }
    token = base64_encode(json_dumps(token, ensure_ascii=False).encode()).decode()
    # 用于服务器校验
    signature_server = sha256(add_salt(token, 0).encode()).hexdigest()
    # 用于客户端校验
    signature_client = sha256((f'{token}{signature_server}').encode()).hexdigest()
    return success({
        'token': f'{token}.{signature_server}.{signature_client}'
    })

