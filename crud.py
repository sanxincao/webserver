from datetime import datetime
from database import engine, tables
from sqlalchemy import select, insert, update, delete, func, Table
from sqlalchemy.exc import OperationalError

T_user: Table = tables['user']



def __check_user_exist(phone: str):
    '检查某用户是否存在'
    with engine.connect() as con:
        sql = select(T_user).where(T_user.c.phone == phone)
        res = con.execute(sql)
        return len(res.all()) > 0


def create_user(email: str) -> tuple[bool, str]:
    '''
    ### 创建一名用户，返回创建用户的结果
    * 此处不进行密码哈希
    '''
    with engine.connect() as con:
        sql = select(T_user).where(T_user.c.email == email)
        res = con.execute(sql)
        if len(res.all()) > 0:
            return False, '用户已存在'
        sql = insert(T_user).values(email=email)
        con.execute(sql)
        con.commit()
    with engine.connect() as conn:
        sql = select(T_user).where(T_user.c.email == email)
        res = conn.execute(sql)
        if len(res.all()) > 0:
            return True, 'ok'
        else:
            return False, '用户创建失败'
    
    


def get_user(email: str):
    '''
    ### 获取一名用户的信息，包括密码、设备、权限等
    * 若用户不存在会返回`False`
    '''
    with engine.connect() as con:
        sql = T_user.select().where(T_user.c.email == email)
        res = con.execute(sql)
        res = res.mappings().first()
    if res is not None:
        return dict(res)
    else:
        return False

