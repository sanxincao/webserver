from datetime import datetime
from json import dumps as json_dumps, loads as json_loads
from hashlib import sha1, sha256
from base64 import b64encode as base64_encode, b64decode as base64_decode
import os
import sys
from time import time
from fastapi import APIRouter, Body, Depends, File, UploadFile, Form, Request, responses
from common import add_salt, success, Error,generate_function_and_component_list
from pydantic import BaseModel
import requests as requestslib
from urllib.parse import urlparse, parse_qs

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


def check_everything(user: dict, device_id: str):
    '检查各种事项，若出现问题直接抛出Error，这里用的user是crud.get_user()的返回结果'
    # 检查用户是否存在
    if user == False:
        raise Error(1)
    # 检查用户是否被禁用
    if user['disabled'] == 1:
        raise Error(2)
    # 检查账号是否在有效期内
    if (datetime.now() - user['expire_time']).total_seconds() > 0:
        raise Error(3)
    # 检查设备是否已授权
    if device_id not in user['authorized_device_list']:
        raise Error(4)


@router.post('/')
def root():
    '根路由'
    return success()

@router.post('/register')
def register(phone=Body(...), password=Body(...)):
    '注册接口'
    res=crud.create_user(phone,password)
    if res[0]==False:
        raise Error(10)
    if res[0]==True:
        return success({"message":res[1]})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        


@router.post('/login')
def login(phone=Body(...), password=Body(...), device_id=Body(...)):
    '''
    登录系统，分发token
    需要满足：账户有效且存在，处于有效期内，密码输入正确，设备id属于已授权设备列表，或设备id不在已授权设备列表中但已授权设备总数未达上限（此时会自动添加）
    '''
    
    res = crud.get_user(phone)
    if res is None:
        raise Error(11) 
    # if sha1(add_salt(password, 1).encode()).hexdigest() != res['password']:
    if  password != res['password']:
        print(sha1(password.encode()).hexdigest())
        print(res['password'])
        raise Error(12)
    if res['disabled']:
        raise Error(13)
    # if (datetime.now() - res['expire_time']).total_seconds() > 0:# 检查用户是否过期
    #     raise Error(14)# 暂时越过检查
    # if device_id not in res['authorized_device_list']:
    #     if len(res['authorized_device_list']) >= res['max_authorized_device_count']:
    #         raise Error(15)
    #     else:
    #         user = dict(res)
    #         user['authorized_device_list'].append(device_id)
    #         del user['create_time'], user['update_time']
    #         crud.change_user_information(**user)
    token = {
        "phone": phone,
        "device_id": device_id,
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

@router.get('/steamlogin')
def steamlogin(request: Request):
    url ='https://steamcommunity.com/openid/login'
    query_params = dict(request.query_params)
   
    print(query_params)
    # 构造请求参数
    if len(query_params['openid.assoc_handle'])>0:
        data = {
            'openid.assoc_handle': query_params['openid.assoc_handle'][0],
            'openid.signed': query_params['openid.signed'][0],
            'openid.sig': query_params['openid.sig'][0],
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.mode': 'check_authentication'
        }
        # 发送请求
        response = requestslib.post(url, data=data)
        if response.status_code == 200:   
            # 解析响应
            result = response.json()
            print(result)
            if result['is_valid'][0] == 'true':
                # 验证通过，可以使用openid.identity参数来标识用户的身份
                identity = result['openid.identity'][0]
                print(f'User identity: {identity}')
            else:
                # 验证失败
                Error(6)
                print('Authentication failed')
    else:
        Error(6)
@router.post('/getUserInfo')
def get_user_info(token_detail=Depends(check_token)):
    user = crud.get_user(token_detail['phone'])
    check_everything(user, token_detail['device_id'])
    return success({
        'expire_time': user['expire_time'].strftime('%Y-%m-%d %H:%M:%S'),

    })



@router.post('/downloadComponent')
def download_component(token_detail=Depends(check_token), component_id: str = Body(...)):
    user = crud.get_user(token_detail['username'])
    check_everything(user, token_detail['device_id'])
    generate_result = generate_function_and_component_list(user['function_type'], user['function_list'])
    if component_id not in generate_result["component_list"]:
        raise Error(43)
    component_detail_list = config.get('component_detail_list')
    for component in component_detail_list:
        if component['id'] == component_id:
            package_path = f"{config.root_path}/components/{component_id}/{component['version']}/package.zip"
            if os.path.exists(package_path):
                return responses.FileResponse(package_path)
            else:
                raise Error(7)
    return Error(6)


@router.post('/downloadProgram')
def download_program(token_detail=Depends(check_token)):
    user = crud.get_user(token_detail['username'])
    check_everything(user, token_detail['device_id'])
    program_path = f"{config.root_path}/client.exe"
    if os.path.exists(program_path):
        return responses.FileResponse(program_path)
    else:
        raise Error(7)


@router.post('/getProgramVersion')
def get_program_version(token_detail=Depends(check_token)):
    user = crud.get_user(token_detail['username'])
    check_everything(user, token_detail['device_id'])
    return success({
        "version": config.get("client_version")
    })
