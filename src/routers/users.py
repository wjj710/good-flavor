"""
处理关于user的路由
"""
from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm

from src.utils import fetch_one
from ..user import UserIn, User,UserInDB, UserInfo, UserChange, UserReg
from ..exceptions import OperationFailed, AlreadyRegistered
from ..user_token import Token, authenticate_user, get_password_hash, create_access_token
from ..dependency import get_current_user, check_admin
from ..settings import Settings
from fastapi import APIRouter
from fastapi import Depends
from datetime import datetime, timedelta
import asyncpg

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(get_current_user)],
)
normal_router = APIRouter(
    tags=["user"],
)



@normal_router.post("/register")
async def register(user: UserReg):
    """注册用户
   
    Args:
        user (UserReg): 注册表单，JSON格式

    Raises:
        CreateFailed: 注册失败异常

    Returns:
        User: 注册成功的用户
    """
    #检查此用户是否已注册
    user1 = await fetch_one('SELECT * FROM myuser WHERE "username" = $1',user.username)
    if user1 is not None:
        raise AlreadyRegistered()
    user.password = get_password_hash(user.password)
    try:
        await fetch_one(\
        'INSERT INTO myuser ("username", "password","is_admin","name","id_type","id_number","phone_number","is_vip","description","city","reg_time","mod_time") VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12)'\
        ,user.username, user.password, user.is_admin, user.name, user.id_type, user.id_number\
        ,user.phone_number, user.is_vip, user.description, user.city, user.reg_time, user.mod_time)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return User(** await fetch_one('SELECT * FROM myuser WHERE "username"= $1',user.username))

@normal_router.post("/change")
async def change(user: UserChange):
    user.password = get_password_hash(user.password)
    try:
        await fetch_one(\
        'INSERT INTO myuser ("id","username", "password","is_admin","name","id_type","id_number","phone_number","is_vip","description","city","reg_time","mod_time") VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)'\
        ,user.id, user.username, user.password, user.is_admin, user.name, user.id_type, user.id_number\
        ,user.phone_number, user.is_vip, user.description, user.city, user.reg_time, user.mod_time)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return User(** await fetch_one('SELECT * FROM myuser WHERE "username"= $1',user.username))

@normal_router.post("/token", response_model=Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    """login代理接口，用于接入openapi，方便调试

    Args:
        form_data (OAuth2PasswordRequestForm, optional): _description_. Defaults to Depends().
    """
    return await login(UserIn(username=form_data.username, password=form_data.password))


@normal_router.post("/login")
async def login(data: UserIn):
    """登录

    Args:
        data (UserIn): 登录表单，JSON格式

    Raises:
        Unauthorization: 密码错误
        NoSuchUser: 没有这个用户
    Returns:
        Token: 令牌
    """
    # 验证用户密码
    user = await authenticate_user(data.username, data.password)
    # 签发token
    access_token_expires = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={Settings.PAYLOAD_NAME: user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer",**user.dict()}


@user_router.get("/me", response_model=UserInfo)
async def read_users_me(request: Request):
    """返回用户信息

    Returns:
        User: 除密码外的信息
    """
    return request.state.user




