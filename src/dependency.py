
from fastapi import Request, Depends
from .user_token import oauth2_scheme, TokenData
from .settings import Settings
from .user import UserInDB
from .exceptions import InactiveUser, Unauthorization, PermissionDenied, NoSuchUser
from jose import JWTError, jwt
from typing import List
import asyncpg
from src.utils import fetch_all, fetch_one

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> UserInDB:
    """获取访问url的用户，中间件

    Args:
            request (Request): _description_
            token (str, optional): token字符串

    Raises:
            NoSuchUser: 没有这个用户
            Unauthorization: 验证失败

    Returns:
            UserInDB: 用户对象
    """
    try:
        # 校验jwt
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        username: str = payload.get(Settings.PAYLOAD_NAME)
        if username is None:
            raise NoSuchUser()
        # 查询用户数据
        token_data = TokenData(username=username)
        #con = await asyncpg.connect(user='postgres', database="tb")
        user = await fetch_one('SELECT * FROM myuser WHERE "username"= $1', token_data.username)
        #await con.close()
    except JWTError:
        raise Unauthorization()
    if user is None:
        raise NoSuchUser()
    user: UserInDB = UserInDB(**user)
    # 保存到request的上下文
    request.state.user = user
    return user


async def check_admin(user: UserInDB = Depends(get_current_user)):
    """判断当前用户是否是管理员

    Args:
            user (UserInDB, optional): 用户对象

    Raises:
            PermissionDenied: 权限不足
    """
    if not user.is_admin:
        raise PermissionDenied()
