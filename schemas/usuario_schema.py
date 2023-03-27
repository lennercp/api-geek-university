from typing import List
from pydantic import BaseModel, EmailStr

from schemas.artigo_schema import ArtigoSchema


class UsuarioSchemaBase(BaseModel):
    id: int| None = None
    nome: str
    sobrenome: str
    email: EmailStr
    eh_admin: bool = False

    class Config:
        orm_mode = True

class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str

class UsuarioSchemaArtigos(UsuarioSchemaBase):
    artigos: List[ArtigoSchema] | None

class UsuarioSchemaUpdate(UsuarioSchemaBase):
    nome: str | None
    sobrenome: str | None
    email: EmailStr | None
    senha: str | None
    eh_admin: bool | None