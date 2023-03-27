from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router

app: FastAPI = FastAPI(title="Curso API - Segurança")
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', port=8000, host='127.0.0.1', reload=True)

'''
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNlc3NfdG9rZW4iLCJleHAiOjE2ODAxMTU2NDUsImlhdCI6MTY3OTUxMDg0NSwic3ViIjoiNyJ9.vdyfGZkSU2jrEwe3yFUG61TyizgwVxivl9Q481QaBUI
tipo: bearer
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNlc3NfdG9rZW4iLCJleHAiOjE2ODAxMTczNDksImlhdCI6MTY3OTUxMjU0OSwic3ViIjoiNSJ9.MwEiBhULyrWhjxz2vtanBKyK_lWAPmzT8sZr8SoNEAM
'''