from urllib.parse import quote
from time import time
from fastapi import APIRouter, Path, Response
from common import Error, add_salt
from base64 import b64decode as base64_decode
from hashlib import sha256
from json import loads as json_loads
import config
router = APIRouter()


@router.get('/file/{ticket}')
def file(ticket: str = Path(...)):
    ticket = ticket.split('_')
    if len(ticket) != 2:
        raise Error(5)
    try:
        detail = json_loads(base64_decode(ticket[0].encode()))
    except BaseException:
        raise Error(5)
    signature = sha256(add_salt(ticket[0], 1).encode()).hexdigest()
    if ticket[1] != signature:
        raise Error(5)
    if detail['expire_time'] < time():
        raise Error(5)
    try:
        f = open(f'{config.root_path}//record_files/{detail["record_id"]}/{detail["file_name"]}', 'rb')
        binary = f.read()
        f.close()
        return Response(binary, headers={"Content-Disposition": f"attachment; filename={quote(detail['file_name'])}"})
    except BaseException:
        raise Error(5)


@router.get('/installation/{ticket}')
def file(ticket: str = Path(...)):
    ticket = ticket.split('_')
    if len(ticket) != 2:
        raise Error(5)
    try:
        detail = json_loads(base64_decode(ticket[0].encode()))
    except BaseException:
        raise Error(5)
    signature = sha256(add_salt(ticket[0], 1).encode()).hexdigest()
    if ticket[1] != signature:
        raise Error(5)
    if detail['expire_time'] < time():
        raise Error(5)
    try:
        f = open(f'{config.root_path}//record_files/{detail["record_id"]}/{detail["file_name"]}', 'rb')
        binary = f.read()
        f.close()
        return Response(binary, headers={"Content-Disposition": f"attachment; filename={quote(detail['file_name'])}"})
    except BaseException:
        raise Error(5)
