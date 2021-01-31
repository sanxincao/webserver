import requests
import json
url="http://127.0.0.1:5000/login"
data={
    "www":"rewq",
    "rrr":"wwww"
}
requests.post(url,json=data)