from fastapi import FastAPI, responses
from common import Error, success, fail


app = FastAPI()

from routers.admin import router as admin
from routers.client import router as client

app.include_router(admin, tags=['admin'], prefix='/admin')
app.include_router(client, tags=['client'], prefix='/client')

@app.exception_handler(Error)
def exception_handler(request, exception: Error):
    return responses.JSONResponse(fail(exception.code))


@app.post('/')
@app.get('/')
def root():
    return success()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', port=8002, host='0.0.0.0', reload=True)
