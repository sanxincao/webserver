from flask import Flask,request
#import parser
from flask_restful import Api,Resource,reqparse,abort
import time
#this file write api route
app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()


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
        args = parser.parse_args()
        print(args)
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

#api.add_resource(severnode, '/')
api.add_resource(severnode,'/servernode')
#USER_LOGIN_API login data
"""

"""
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
              'token':'123456'
          }

      }
api.add_resource(userlogin, '/login')

class DES_KEY(Resource):
    def get(self):
        return [ 0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF ]

class getstatus(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        parser.add_argument('device')
        args = parser.parse_args()
        print(args)
    def post(self):
        return {
            "code":"200"
        }
api.add_resource(getstatus, '/')
if __name__ == '__main__':
    app.run(debug=True)