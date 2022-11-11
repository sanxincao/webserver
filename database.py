from sqlalchemy import JSON, Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, create_engine, func, orm

# database_url = "mysql+pymysql://test_data:6pCb3GbMBZPRAd3C@192.168.30.125/test_data"
# database_url = "mysql+pymysql://media_database:tY5Xk3r3sf3z2dec@192.168.30.125/media_database"
database_url = "sqlite:///../offline.db"

# 数据库引擎
engine = create_engine(database_url, echo=False, future=True)
# ORM注册器
registry = orm.registry()
# ORM元数据
metadata = registry.metadata
# 数据模型基类
Base = registry.generate_base()


class User(Base):
    '用户表'
    __tablename__ = 'user'
    # 字段
    phone = Column(String(20), primary_key=True, comment='电话号码')
    password = Column(String(40), comment='密码(sha1)')
    authorized_device_list = Column(JSON, default=[], comment='已授权的设备')
    max_authorized_device_count = Column(Integer, server_default='3', comment='最大授权设备数量')
    disabled = Column(Boolean, server_default='0', comment='禁用标记')
    expire_time = Column(DateTime, server_default=func.now(), comment='用户过期时间')
    create_time = Column(DateTime, server_default=func.now(), comment='记录创建时间')
    update_time = Column(DateTime, onupdate=func.now(), server_default=func.now(), comment='记录更新时间')

class serverlist(Base):
    "服务器表"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='服务器id')
    linkstring = Column(String(100), comment='服务器链接')
    type = Column(String(100), comment='服务器类型')
    expire_time = Column(DateTime, server_default=func.now(), comment='服务器过期时间')
    
    

metadata.create_all(engine)
'''
所有表的元数据字典
使用 tables['表名'] 即可获取到表的元数据
'''
tables = metadata.tables
