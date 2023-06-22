from sqlalchemy import JSON, Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, create_engine, func, orm

# database_url = "mysql+pymysql://test_data:6pCb3GbMBZPRAd3C@192.168.30.125/test_data"
# database_url = "mysql+pymysql://media_database:tY5Xk3r3sf3z2dec@192.168.30.125/media_database"
database_url = "sqlite:///./boosteroffline.db"

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
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='用户id')
    #生成邮箱字段代码
    email = Column(String(50), comment='邮箱')
    

#生成订单表
class Order(Base):
    #用户订单表
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='订单id')
    #商品名称
    name = Column(String(50), comment='商品名称')
    #订单所属的用户id
    user_id = Column(Integer, ForeignKey('user.id'), comment='用户id')
    #订单状态
    status = Column(Enum('待支付', '已支付', '已取消'), comment='订单状态')
    #支付金额
    amount = Column(Integer, comment='支付金额')
    #支付时间
    pay_time = Column(DateTime, comment='支付时间')
    #商品类型及要求说明json
    product_type = Column(JSON, comment='商品类型及要求说明json')
    

metadata.create_all(engine)
'''
所有表的元数据字典
使用 tables['表名'] 即可获取到表的元数据
'''
tables = metadata.tables
