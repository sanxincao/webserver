from flask import Flask
from flask_restful import Api,Resource
#this file write api route
app = Flask(__name__)
api = Api(app)
#the server node
"""private int id;
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
        'host':
        'port:8080'
        }

api.add_resource(HelloWorld, '/')

class DES_KEY(Resource):
    def get(self):
        return [ 0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF ]

class
if __name__ == '__main__':
    app.run(debug=True)