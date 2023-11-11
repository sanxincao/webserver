import hashlib
from time import time
from json import loads as json_loads, dumps as json_dumps
import shutil
import os
from fastapi import APIRouter, Body, Depends, File, Form, UploadFile
from zipfile import ZipFile, is_zipfile
import crud
from base64 import b64encode as base64_encode, b64decode as base64_decode
from common import Error, success, fail, add_salt
from hashlib import sha1, sha256
from datetime import datetime
import config


def check_token(token: str = Body(...)):
    if token == 'tcmx':
        return True
    else:
        raise Error(99)


router = APIRouter(dependencies=[Depends(check_token)])
'负责管理后台相关的接口'


@router.post('/uploadComponent')
def upload_component(compoment_id: str = Body(...), update_information: str = Body(...), package_file: UploadFile = File(...)):
    '上传组件'
    def fail(message):
        shutil.rmtree(item_path)
        return {'result': False, 'message': message}

    def parse_detail(path):
        with open(path, 'r') as f:
            return json_loads(f.read())

    def save_detail(path, detail):
        with open(path, 'w') as f:
            return f.write(json_dumps(detail, ensure_ascii=False))

    component_detail_list = config.get('component_detail_list')
    if compoment_id not in list(map(lambda x: x['id'], component_detail_list)):
        return {'result': False, 'message': '不存在该组件'}
    # 定义相关文件路径
    compoment_path = f'{config.root_path}/components/{compoment_id}'
    item_path = f'{compoment_path}/{len(os.listdir(compoment_path))+1}'
    old_detail_path = f'{compoment_path}/{len(os.listdir(compoment_path))}/detail.json'
    detail_path = f'{item_path}/detail.json'
    package_path = f'{item_path}/package.zip'
    unzip_path = f'{item_path}/unzip'
    # 创建文件夹
    os.mkdir(item_path)
    os.mkdir(unzip_path)
    # 判断新上传文件是否重复
    zip_data = package_file.file.read()
    zip_file_md5 = hashlib.md5(zip_data).hexdigest()
    if len(os.listdir(compoment_path)) > 1:
        old_detail = parse_detail(old_detail_path)
        if zip_file_md5 == old_detail['zip_file_md5']:
            return fail('本次上传的组件包与上版本哈希值相同')
    # 保存压缩文件
    with open(package_path, 'wb') as f:
        f.write(zip_data)
    # 判断压缩文件是否满足需求
    if is_zipfile(package_path) == False:
        return fail('上传的组件包非压缩文件')
    # 读取压缩文件，并进行解压缩处理，生成文件(夹)项目列表
    try:
        zip = ZipFile(package_path)
        file_tree_item_list = [{'id': './', 'name': 'root_path', 'type': 'folder'}]
        for name in zip.namelist():
            target_path = f'{unzip_path}/{name}'
            if target_path.endswith('/'):
                os.mkdir(target_path)
                node = {'id': './' + name, 'parent': (f'./{"/".join(name.split("/")[:-2])}/').replace('.//', './'), 'name': name.split('/')[-2], 'type': 'folder'}
            else:
                file_data = zip.read(name)
                with open(target_path, 'wb') as f:
                    f.write(file_data)
                node = {'id': './' + name, 'parent': (f'./{"/".join(name.split("/")[:-1])}/').replace('.//', './'), 'name': name.split('/')[-1], 'type': 'file'}
            file_tree_item_list.append(node)
    except BaseException:
        return fail('压缩包读取异常')
    # 生成文件树
    file_tree = []
    folder_children_mapping = {}
    folder_list = list(filter(lambda x: x['type'] == 'folder', file_tree_item_list))
    while len(folder_list) > 0:
        folder_children_mapping[folder_list[0]['id']] = []
        if 'parent' in folder_list[0].keys():
            if folder_list[0]['parent'] in folder_children_mapping.keys():
                folder_children_mapping[folder_list[0]['parent']].append({
                    'id': folder_list[0]['id'],
                    'name': folder_list[0]['name'],
                    'children': folder_children_mapping[folder_list[0]['id']]
                })
                folder_list.pop(0)
            else:
                folder_list.append(folder_list.pop(0))
        else:
            file_tree.append({
                'id': folder_list[0]['id'],
                'name': folder_list[0]['name'],
                'children': folder_children_mapping[folder_list[0]['id']]
            })
            folder_list.pop(0)
    file_list = list(filter(lambda x: x['type'] == 'file', file_tree_item_list))
    for file in file_list:
        folder_children_mapping[file['parent']].append({
            'id': file['id'],
            'name': file['name']
        })
    # 保存此次组件包的详情
    detail = {
        'zip_file_md5': zip_file_md5,
        'information': update_information,
        'file_tree': file_tree[0]['children'],
        'timestamp': time()
    }
    save_detail(detail_path, detail)
    # 默认需要哈希的文件，这里为全部
    hash_file_list = [item['id'] for item in file_tree_item_list if item['type'] == 'file']
    # 计算这些文件的哈希总和
    hash_result_list = []
    for file_path in hash_file_list:
        f = open(f'{unzip_path}/{file_path}', 'rb')
        hash_result_list.append(hashlib.md5(f.read()).hexdigest())
        f.close()
    hash_result_list.sort()
    hash_result = hashlib.md5(''.join(hash_result_list).encode()).hexdigest()
    # 对配置文件进行读取和写入
    component_detail_list = config.get('component_detail_list')
    for item in component_detail_list:
        if item['id'] == compoment_id:
            item['hash_file_list'] = hash_file_list
            item['hash_result'] = hash_result
            item['version'] = len(os.listdir(compoment_path))
    config.set('component_detail_list', component_detail_list)
    return success({'result': True})


@router.post('/changeUserInformation')
def change_user_information(username: str = Body(...), password: str = Body(...), nickname: str = Body(...)):
    try:
        password_hash = sha1(add_salt(password, 1).encode()).hexdigest()
        crud.change_user_information(username, password_hash,'white', [], [], 3, False, datetime(2023, 1, 1))
        return success()
    except BaseException:
        return fail()



@router.post('/uploadProgramInstallation')
def upload_program_installation(version: str = Body(..., example='v0.1.0'), program_installation: UploadFile = File(...)):
    config.set('client_version', version)
    f = open('./client.exe', 'wb')
    f.write(program_installation.file.read())
    f.close()
    return success()
