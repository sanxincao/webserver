import requests
import json
url="http://127.0.0.1:5000/api/v1.0/login"
data={
    'phone': 'Ec9C/XMDbtAnQrOMF51g4w==',
    'password': 'FZz3LAvSqBjRKk7RbJ2cAQ=='
}
requests.post(url,json=data)