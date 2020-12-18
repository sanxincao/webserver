from flask import Flask
#import parser
from flask_restful import Api,Resource,reqparse,abort
import time
#this file write api route
app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('task', type=str)
class root(Resource):
    def get():
        return {
            'token':'13840702430'
        }

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
        return {'id': '1',
        'name':'test',
        'icon':'white.loge',
        'remark':'null',
        'linkcount':'1',
        'selected':True,
        'host':'144.34.148.204',
        'method':'aes-156-gcm',
        'port':'443',
        'password':'password'
        }

api.add_resource(severnode, '/servernode')
#USER_LOGIN_API login data
"""

"""
class userlogin(Resource):
    def post(self):
        args = parser.parse_args()
        now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(args)
        return {
            'code':'200',
            'content':
            {
                'avatar':'null',
                'serviceexpiredate':now,
                'password':'null',
                'phone':'null',
                'type':'null'
            }
            
        }
api.add_resource(userlogin, '/login')

class DES_KEY(Resource):
    def get(self):
        return [ 0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF ]


if __name__ == '__main__':
    app.run(debug=True)