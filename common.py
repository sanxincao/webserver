from fastapi import HTTPException
import config


__message_map = {
    0: 'ok',
    1: '用户不存在',
    2: '用户被禁用',
    3: '该账号已过期',
    4: '该设备未授权',
    5: '找不到对应资源',
    6: '服务器逻辑执行异常',
    7: '服务器文件IO异常',
    8: '传入的数据格式异常',
    9: '数据库操作异常',
    10: '用户已存在',
    11: '登录失败，用户不存在',
    12: '登录失败，密码不正确',
    13: '登录失败，该账号已禁用',
    14: '登录失败，该账号有效授权期已过',
    15: '登录失败，该账号已绑定设备数量达到上限',
    21: '口令校验失败，段落数异常',
    22: '口令校验失败，签名长度异常',
    23: '口令校验失败，签名错误',
    24: '口令校验失败，无法解码',
    31: '受试者不存在',
    32: '评测记录不存在',
    33: '组件不存在',
    34: '评测项不存在',
    35: '文件不存在',
    36: '文件块不存在',
    41: '非法操作，无权获取该受试者',
    42: '非法操作，无权获取该评测记录',
    43: '非法操作，无权获取该组件详情',
    44: '非法操作，无权获取该评测项详情',
    99: '非法操作'
}


class Error(HTTPException):
    '''
    0: 'ok',
    1: '用户不存在',
    2: '用户被禁用',
    3: '该账号已过期',
    4: '该设备未授权',
    5: '找不到对应资源',
    6: '服务器逻辑执行异常',
    7: '服务器文件IO异常',
    8: '传入的数据格式异常',
    9: '数据库操作异常',
    10: '用户已存在',
    11: '登录失败，用户不存在',
    12: '登录失败，密码不正确',
    13: '登录失败，该账号已禁用',
    14: '登录失败，该账号有效授权期已过',
    15: '登录失败，该账号已绑定设备数量达到上限',
    21: '口令校验失败，段落数异常',
    22: '口令校验失败，签名长度异常',
    23: '口令校验失败，签名错误',
    24: '口令校验失败，无法解码',
    31: '受试者不存在',
    32: '评测记录不存在',
    33: '组件不存在',
    34: '评测项不存在',
    35: '文件不存在',
    36: '文件块不存在',
    41: '非法操作，无权获取该受试者',
    42: '非法操作，无权获取该评测记录',
    43: '非法操作，无权获取该组件详情',
    44: '非法操作，无权获取该评测项详情',
    99: '非法操作'
    '''

    def __init__(self, code: int = 0):
        self.status_code = 200
        self.code = code


def success(data: dict = {}):
    return {
        **data,
        'code': 0,
        'message': 'ok'
    }


def fail(code: int, data: dict = {}):
    return {
        **data,
        'code': code,
        'message': __message_map[code],
    }


def add_salt(string: str, type: int = 0):
    if type == 1:
        return f'😂左加一个嘎嘎盐😂{string}😊右加一个嘟嘟盐😊'
    else:
        return f'🤭左加一个嘻嘻盐🤭{string}😄右加一个哈哈盐😄'
    
    
def generate_function_and_component_list(function_type, function_list) -> dict:
    '通过`function_type`(total/white/black) 生成相应的功能列表与组件列表'
    total_function_list = config.get('function_list')
    user_function_list = []
    if function_type == 'total':
        user_function_list = [item['id'] for item in total_function_list]
    elif function_type == 'white':
        user_function_list = [item['id'] for item in total_function_list if item['id'] in function_list]
    elif function_type == 'black':
        user_function_list = [item['id'] for item in total_function_list if item['id'] not in function_list]
    user_component_list = ['backend']
    for function_id in user_function_list:
        for function in total_function_list:
            if function_id == function['id']:
                user_component_list += function['component']
    user_component_list = list(set(user_component_list))
    return {
        'function_list': user_function_list,
        'component_list': user_component_list
    }



