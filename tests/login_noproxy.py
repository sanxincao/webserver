import requests
postdata={
  'phone':'13840702430',
  'password':'password'
}
res=requests.post('http://127.0.0.1:5000/api/v1.0/login',json=postdata)
print(res.json())