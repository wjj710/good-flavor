import datetime
from gettext import translation
from http.client import HTTPException
from fastapi import APIRouter
from typing import Any, Optional, List
import fastapi
from ..exceptions import OperationFailed
import pydantic
from ..user import UserInfo
from src.utils import fetch_all, fetch_one, fetch_one_then_wrap_model, get_connection
import asyncpg


admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@admin_router.get("/user", response_model=List[UserInfo])
async def get_users():
    """获取所有用户，需要管理员权限

    Returns:
        List[User]: 所有用户的信息
    """
    users = await fetch_all('SELECT * FROM myuser')
    return [UserInfo(**user) for user in users]


@admin_router.post("/administrator/{userid}")
async def grant_user_as_admin(userid: int):
    """授予用户管理员权限，需要管理员权限
    即使用户不存在也不会报错

    Args:
        userid (int): 用户id
    """
    await fetch_one('UPDATE myuser SET is_admin = true WHERE id = $1', userid)
    return "ok"


@admin_router.delete("/administrator/{userid}")
async def revoke_user_as_admin(userid: int):
    """撤销用户管理员权限，需要管理员权限
    即使用户不存在也不会报错

    Args:
        userid (int): 用户id
    """
    await fetch_one('UPDATE myuser SET is_admin = false WHERE id = $1', userid)
    return "ok"

@admin_router.get("/all_search_query")
async def all_search_query(flavor_type: str="", req_name: str=""):
    if flavor_type!="" and req_name!="":
        command=f"""
        SELECT * FROM search WHERE "flavor_type"='{flavor_type}' and "req_name" like '%{req_name}%'
        """
    elif flavor_type!="":
        command=f"""
        SELECT * FROM search WHERE "flavor_type"='{flavor_type}'
        """
    elif req_name!="":
        command=f"""
        SELECT * FROM search WHERE "req_name" like '%{req_name}%'
        """
    else:
        command=f"""
        SELECT * FROM search'
        """
    try:
        result=await fetch_all(command)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return result

@admin_router.get("/all_taste_query")
async def all_taste_query():
    command=f"""
    SELECT * FROM taste
    """
    try:
        result=await fetch_all(command)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return result

@admin_router.get("/benefits_query")
async def benefits_query(flavor_type: str = "", city: str = "beijing",
                         start_time: datetime.date = datetime.date(1999, 1, 1),
                         stop_time: datetime.date = datetime.date.today(), flag: int = 0):
    if start_time.year == 1999:
        if stop_time.month > 3:
            start_time = datetime.date(stop_time.year, stop_time.month - 3, stop_time.day)
        else:
            start_time = datetime.date(stop_time.year - 1, stop_time.month + 8, stop_time.day)

    if flavor_type == '':
        command = f"""
        SELECT "finish_time","flavor_type","city","req_id","user1_id","user2_id","fee1","fee2"  
        FROM success INNER JOIN search ON success.req_id = search.id 
        INNER JOIN myuser ON success.user1_id = myuser.id
        WHERE "finish_time"<='{stop_time}' AND "finish_time">='{start_time}'
        AND "city"='{city}'
        """
    else:
        command = f"""
        SELECT "finish_time","flavor_type","city","req_id","user1_id","user2_id","fee1","fee2"  
        FROM success INNER JOIN search ON success.req_id = search.id 
        INNER JOIN myuser ON success.user1_id = myuser.id
        WHERE "finish_time"<='{stop_time}' AND "finish_time">='{start_time}'
        AND "city"='{city}' AND "flavor_type"='{flavor_type}'
        """
    if flag == 1:
        command += '/nORDER BY "finish_time" DESC'
    elif flag == 2:
        command += '/nORDER BY "fee1" DESC'

    try:
        result = await fetch_all(command)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return result
