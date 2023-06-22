import hashlib
from time import time
from json import loads as json_loads, dumps as json_dumps
import shutil
import os
from fastapi import APIRouter, Body, Depends, File, Form, UploadFile
from zipfile import ZipFile, is_zipfile
import crud
from base64 import b64encode as base64_encode, b64decode as base64_decode
from common import Error, success, fail, add_salt
from hashlib import sha1, sha256
from datetime import datetime
import config


def check_token(token: str = Body(...)):
    if token == 'booster':
        return True
    else:
        raise Error(99)


router = APIRouter(dependencies=[Depends(check_token)])
'负责管理后台相关的接口'

