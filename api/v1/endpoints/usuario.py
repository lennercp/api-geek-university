from typing import List, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaArtigos, UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUpdate

from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

router = APIRouter()

# GET LOGADO
@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado

# POST / SIGNUP
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha= gerar_hash_senha(usuario.senha),
        eh_admin=usuario.eh_admin,
    )
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()

            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Já existe um usuario com este email cadastradado")

# GET Usuarios
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
        
        return usuarios

# GET USUARIO         
@router.get('/{usuario_id}', status_code=status.HTTP_200_OK, response_model=UsuarioSchemaArtigos)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaBase = result.scalar()

        if usuario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado")

        return usuario

# PUT USUARIO
@router.put('/{usuario_id}', status_code=status.HTTP_202_ACCEPTED, response_model=UsuarioSchemaBase)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalar()

        if usuario_up is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado")

        if usuario.nome:
            usuario_up.nome = usuario.nome
        if usuario.sobrenome:
            usuario_up.sobrenome = usuario.sobrenome
        if usuario.email:
            usuario_up.email = usuario.email
        if usuario.senha:
            usuario_up.senha = gerar_hash_senha(usuario.senha)
        if usuario.eh_admin:
            usuario_up.eh_admin = usuario.eh_admin

        await session.commit()

        return usuario_up

# DELETE USUARIO
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_delete: UsuarioSchemaBase = result.scalar()

        if usuario_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado")

        await session.delete(usuario_delete)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

# POST LOGIN
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if usuario is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dados de acesso incorretos')

    return JSONResponse(content={
        "acess_token": criar_token_acesso(sub=usuario.id),
        "token_type": "bearer",
    }, status_code=status.HTTP_200_OK)
