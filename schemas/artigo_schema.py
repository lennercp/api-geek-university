from pydantic import BaseModel, HttpUrl
from typing import Optional

class ArtigoSchema(BaseModel):
    id: Optional[int] = None
    titulo: str
    descricao: str
    url_fonte: HttpUrl
    usuario_id: Optional[int] = None

    class Config:
        orm_mode = True