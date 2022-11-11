from json import loads as json_loads, dumps as json_dumps
from os import path
root_path = path.dirname(__file__)
__config_file_path = path.join(root_path, './config.json')


def get(key: str):
    __f = open(__config_file_path, 'r')
    __config = __f.read()
    __config = json_loads(__config)
    __f.close()
    if key in __config.keys():
        return __config[key]
    else:
        raise KeyError('配置里没有这个项')


def set(key: str, value: any):
    __f = open(__config_file_path, 'r')
    __config = __f.read()
    __f.close()
    try:
        __config = json_loads(__config)
        __config[key] = value
        __f = open(__config_file_path, 'w')
        __f.write(json_dumps(__config, ensure_ascii=False))
        __f.close()
        return True
    except BaseException:
        __f.close()
        raise ValueError('试图写入无法JSON序列化的值')
