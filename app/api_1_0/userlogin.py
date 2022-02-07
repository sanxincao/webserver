from flask_restful import Api,Resource,reqparse,abort
from flask_httpauth import HTTPBasicAuth,HTTPTokenAuth
from ..models import User,AnonymousUser,Server
from flask import g, jsonify,request
from flask_login import login_user, logout_user, login_required, \
    current_user
import time
from . import api_bp
from .. import DES

des=DES()
parser = reqparse.RequestParser()

auth=HTTPBasicAuth()
token_auth=HTTPTokenAuth()
api=Api(api_bp)

@auth.verify_password
def verify_password(phone,password):
  #实际上用不到，客户端会检查是否填写
  if phone=='':
    g.current_user==AnonymousUser()
    return True
  #user=User.query.filter_by(phone='Ec9C/XMDbtAnQrOMF51g4w=='.encode("utf-8")).first()

  else:
    return False
  #login_user(user)
  #g.current_user=user
  #g.token_used=False

@token_auth.verify_token
def verify_token(token):
  g.current_user=User.verify_auth_token(token)
  g.token_used=True
  return g.current_user is not None


class userlogin(Resource):

  def post(self):
      new_x = request.get_json()
      phone=new_x['phone']
      password=new_x['password']
      print(phone)
      print(password)
      if phone=='':
        g.current_user==AnonymousUser()

      user=User.query.filter_by(phone=phone).first()
      if not user:
        print(user)
        print('not user')
      islogin=user.verify_password(password)
      print(islogin)
      now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
      if islogin == True:
        g.current_user=user
        g.token_used=False
        login_user(user)
        print('login')
        return {
          'code':'200',

          'content':
          {
              'avatar':'null',
              'serviceexpiredate':now,

              'password':'null',
              'phone':'null',
              'type':'1',
              'token':g.current_user.generate_auth_token(expiration=3600)
          }
        }
      else :
        print('failed')
        logout_user()
        return {
          'code':'400'
        }


api.add_resource(userlogin, '/login')

class test(Resource):
  def get(self):
    return {'test':'test'}


api.add_resource(test, '/test')
# todo servernode logout api get sources from datebase and update

#the server node
"""private int id;
        http://localhost/
        private string name;
        private string icon;s
        private string remark;
        private int linkcount;
        private bool selected;
        private string host;
        private string port;
        private string method;
        private string password;"""
class severnode(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        #TODO yanzheng token 后返回server
        args = parser.parse_args()
        print(args['token'])
        istoken=verify_token(args)

        print(istoken)
        return {
        'code':'200',
        'content':[
        {
        'id': '1',
        'name':'test',
        'icon':'white.loge',
        'remark':'null',
        'linkcount':'1',
        'selected':True,
        'host':'144.34.148.204',
        'port':'443',
        'method':'aes-256-gcm',
        'password':'password'
        },
        {
        'id': '2',
        'name':'test',
        'icon':'white.loge',
        'remark':'null',
        'linkcount':'1',
        'selected':True,
        'host':'144.34.148.204',
        'port':'443',
        'method':'aes-256-gcm',
        'password':'password'
        }

        ]
        }

api.add_resource(severnode,'/servernode')

class logout(Resource):
  def post(self):
    logout_user()

#TODO
api.add_resource(logout,'/logout')