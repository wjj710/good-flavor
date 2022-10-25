"""
用户
"""
# import aiosqlite
from .exceptions import ValidateError
from pydantic import BaseModel, validator
import re
from typing import Any, Optional, Dict
from .settings import Settings
import datetime


class UserIn(BaseModel):
    """用于登录的用户信息
    """
    username: str
    password: str

    @validator('username')
    def validate_name(cls, v: str):
        if len(v) < Settings.USERNAME_MIN_LENGTH or len(v) > Settings.USERNAME_MAX_LENGTH:
            print("用户名")
            raise ValidateError("用户名不合法")
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < Settings.PASSWORD_MIN_LENGTH or len(v) > Settings.PASSWORD_MAX_LENGTH or Settings.PASSWORD_RULE.match(v) is None:
            print("密码")
            raise ValidateError("密码不合法")
        return v


class User(BaseModel):
    """用户基本信息，不包含id和password
    """
    username: str
    is_admin: bool = False
    name: str
    id_type: str
    id_number: str
    phone_number: str
    is_vip: bool = False
    description: Optional[str]
    city: str
    reg_time: datetime.datetime
    mod_time: datetime.datetime

class UserInfo(User):
    """用于返回用户信息，此处返回的id用于之后的修改操作
    """
    id: int

class UserInDB(UserInfo):
    """存储在数据库中的
    """
    password: str

class UserReg(User):
    """用于注册
    """
    password: str

    @validator('username')
    def validate_name(cls, v: str):
        if len(v) < Settings.USERNAME_MIN_LENGTH or len(v) > Settings.USERNAME_MAX_LENGTH:
            raise ValidateError("用户名不合法")
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < Settings.PASSWORD_MIN_LENGTH or len(v) > Settings.PASSWORD_MAX_LENGTH or Settings.PASSWORD_RULE.match(v) is None:
            raise ValidateError("密码不合法")
        return v
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        if len(v)!=11 or Settings.NUMBER_RULE.match(v) is None:
            raise ValidateError("号码格式不正确")
        return v

class UserChange(UserInDB):
    """用于更改的用户信息
    """
    id: int