from flask_restful import Api,Resource,reqparse,abort
from flask_httpauth import HTTPBasicAuth,HTTPTokenAuth
from ..models import User,AnonymousUser
from flask import g, jsonify,request
import time
from . import api_bp


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
  #if password==''
  user=User.query.filter_by(phone=phone).first()
  if not user:
    return False
  g.current_user=user
  g.token_used=False
  return user.verify_password(password)
@token_auth.verify_token
def verify_token(token):
  g.current_user=User.verify_auth_token(token)
  g.token_used=True
  return g.current_user is not None


class userlogin(Resource):
  def get(self):
    return {'test':'test'}
  def post(self):
      new_x = request.get_json()
      #new_y=request.data()
      #thedata=request.get_data()
      #print(thedata)
      #print(new_y)
      print(new_x)
      phone=new_x['phone']
      password=new_x['password']
      islogin=verify_password(phone,password)
      now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

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

api.add_resource(userlogin, '/login')
