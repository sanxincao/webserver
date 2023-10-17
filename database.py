from sqlalchemy import JSON, Boolean, Column, DateTime, Text, Enum, ForeignKey, Integer, String, BigInteger,create_engine, func, orm

# database_url = "mysql+pymysql://test_data:6pCb3GbMBZPRAd3C@192.168.30.125/test_data"
# database_url = "mysql+pymysql://media_database:tY5Xk3r3sf3z2dec@192.168.30.125/media_database"
database_url = "sqlite:///./offline.db"

# 数据库引擎
engine = create_engine(database_url, echo=False, future=True)
# ORM注册器
registry = orm.registry()
# ORM元数据
metadata = registry.metadata
# 数据模型基类
Base = registry.generate_base()


class User(Base):
    '技术用户表'
    __tablename__ = 'user'
    # 字段
    usrid = Column(BigInteger(unsigned=True), primary_key=True, comment='用户id')
    email = Column(String(40), comment='邮箱')
    name = Column(String(20),  server_default='小皮皮',comment='用户名')
    password = Column(String(40), comment='密码(sha1)')
    skill_tree = Column(JSON, default=[], comment='用户技能树')   
    # max_authorized_device_count = Column(Integer, server_default='3', comment='最大授权设备数量')
    disabled = Column(Boolean, server_default='0', comment='禁用标记')
    online_state = Column(Boolean, server_default='0', comment='在线状态')
    #优先权重
    priority = Column(Integer, server_default='100', comment='优先权重')
    create_time = Column(DateTime, server_default=func.now(), comment='记录创建时间')
    update_time = Column(DateTime, onupdate=func.now(), server_default=func.now(), comment='记录更新时间')
    #payment_method 
    Column(Enum('alipay', 'wechat', 'bankcard', 'usdt', name='payment_method'), comment='支付方式')

class Customer(Base):
    '客户表'
    __tablename__ = 'customer'
    # 字段
    customer_id = Column(BigInteger(unsigned=True), primary_key=True, comment='客户ID')
    email = Column(String(40), comment='邮箱')
    password = Column(String(40), comment='密码(sha1)')
    customer_name = Column(String(20), comment='客户名称')
    create_time = Column(DateTime, server_default=func.now(), comment='记录创建时间')
    update_time = Column(DateTime, onupdate=func.now(), server_default=func.now(), comment='记录更新时间')


class UserFeedback(Base):
    "用户评价表"
    __tablename__ = 'user_feedback'
    #id
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    #以user表的id作为外键
    usrid = Column(BigInteger(unsigned=True), ForeignKey('user.usrid'), comment='用户ID')
    #反馈内容 富文本
    content = Column(Text, comment='反馈内容')

class CustomerFeedback(Base):
    '客户反馈表'
    __tablename__ = 'customer_feedback'
    #id
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    #以customer表的id作为外键
    customer_id = Column(BigInteger(unsigned=True), ForeignKey('customer.customer_id'), comment='客户ID')
    user_id = Column(BigInteger(unsigned=True), ForeignKey('user.usrid'), comment='用户ID')    
    #反馈内容 富文本
    content = Column(Text, comment='反馈内容')

class Order(Base):
    '撮合交易表'
    __tablename__ = 'order'
    #id
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    #以customer表的id作为外键
    customer_id = Column(String(20), ForeignKey('customer.customer_id'), comment='客户ID')
    #交易对方
    counterparty = Column(BigInteger(unsigned=True), ForeignKey('user.usrid'),comment='交易对方')
    #交易类型
    order_type = Column(String(20), comment='交易类型')
    #price
    price = Column(String(20), comment='价格')
    #start_time
    start_time = Column(DateTime, server_default=func.now(), comment='开始时间')
    #end_time
    end_time = Column(DateTime, onupdate=func.now(), server_default=func.now(), comment='结束时间')
    #verify_video_url
    verify_video_url = Column(String(20), comment='验证视频url')
    #close
    close = Column(Boolean, server_default='0', comment='是否关闭')


metadata.create_all(engine)
'''
所有表的元数据字典
使用 tables['表名'] 即可获取到表的元数据
'''
tables = metadata.tables
