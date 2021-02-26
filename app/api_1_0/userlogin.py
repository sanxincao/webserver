from flask_restful import Api,Resource,reqparse,abort
from flask_httpauth import HTTPBasicAuth
from . import api_bp


parser = reqparse.RequestParser()

auth=HTTPBasicAuth

api=Api(api_bp)
@auth.verify_password
def verify_password(phone,password)

class userlogin(Resource):
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
