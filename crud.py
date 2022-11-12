from datetime import datetime
from database import engine, tables
from sqlalchemy import select, insert, update, delete, func, Table
from sqlalchemy.exc import OperationalError

T_user: Table = tables['user']



def __check_user_exist(username: str):
    '检查某用户是否存在'
    with engine.connect() as con:
        sql = select(T_user).where(T_user.c.username == username)
        res = con.execute(sql)
        return len(res.all()) > 0


def create_user(phone: str, password: str) -> tuple[bool, str]:
    '''
    ### 创建一名用户，返回创建用户的结果
    * 此处不进行密码哈希
    '''
    with engine.connect() as con:
        sql = select(T_user).where(T_user.c.phone == phone)
        res = con.execute(sql)
        if len(res.all()) > 0:
            return False, '用户已存在'
        sql = insert(T_user).values(phone=phone, password=password)
        con.execute(sql)
        con.commit()
        sql = select(T_user).where(T_user.c.phone == phone)
        res = con.execute(sql)
    if len(res.all()) > 0:
        return True, 'ok'
    else:
        return False, '用户创建失败'


def get_user(username: str):
    '''
    ### 获取一名用户的信息，包括密码、设备、权限等
    * 若用户不存在会返回`False`
    '''
    with engine.connect() as con:
        sql = T_user.select().where(T_user.c.username == username)
        res = con.execute(sql)
        res = res.mappings().first()
    if res is not None:
        return dict(res)
    else:
        return False


def change_user_information(username: str, password: str, nickname: str, function_type: str, function_list: list[str], authorized_device_list: list[str], max_authorized_device_count: int, disabled: bool, expire_time: datetime) -> tuple[bool, str]:
    '''
    ### 修改一名用户的信息
    - - -

    `nickname` : 用户的昵称
    `function_type` : 判断该用户可使用功能的类型，可选值：`white`/`black`/`total`
    `function_list` : 与function_type对应，代表功能的黑/白名单
    `authorized_device_list` : 已授权的设备列表
    `max_authorized_device_count` : 最大授权设备数量
    `disabled` : 账号是否禁用
    `expire_time` : 账号过期时间
    '''
    if __check_user_exist(username) == False:
        return False, '用户不存在'
    information = {
        'password': password,
        'function_type': function_type,
        'function_list': function_list,
        'authorized_device_list': authorized_device_list,
        'max_authorized_device_count': max_authorized_device_count,
        'disabled': disabled,
        'expire_time': expire_time,
    }
    with engine.connect() as con:
        sql = update(T_user).where(T_user.c.username == username).values(**information)
        res = con.execute(sql)
        con.commit()
    if res.rowcount > 0:
        return True, 'ok'
    else:
        return False, '修改失败'
