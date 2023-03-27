from pydantic import BaseModel, HttpUrl


class ArtigoSchema(BaseModel):
    id: int|None = None
    titulo: str
    descricao: str
    url_fonte: HttpUrl
    usuario_id: int|None

    class Config:
        orm_mode = True