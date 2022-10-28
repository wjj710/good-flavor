from ..model import search, searchInDB
from src.utils import fetch_one, fetch_all
from ..exceptions import OperationFailed
import asyncpg
from fastapi import APIRouter
from ..settings import Settings


data_router = APIRouter(
    prefix=f"{Settings.DATA_ROUTER_PREFIX}",
    tags=["data"],
)

@data_router.post("/search/add")
async def search_add(s: search):
    try:
        await fetch_one(\
        'INSERT INTO search ("username", "flavor_type","req_name","req_description","price","end_time","photo","crea_time","mod_time","state") VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)'\
        ,s.username, s.flavor_type, s.req_name, s.req_description, s.price, s.end_time\
        ,s.photo, s.crea_time, s.mod_time, s.state)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return "ok"

@data_router.post("/search/delete")
async def search_delete(id: int):
    try:
        await fetch_one('DELETE FROM search WHERE "id"=$1',id)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return "ok"

@data_router.post("/search/change")
async def search_change(s: searchInDB):
    try:
        await fetch_one(\
        'INSERT INTO search ("id", "username", "flavor_type","req_name","req_description","price","end_time","photo","crea_time","mod_time","state") VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)'\
        ,s.id, s.username, s.flavor_type, s.req_name, s.req_description, s.price, s.end_time\
        ,s.photo, s.crea_time, s.mod_time, s.state)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return "ok"

@data_router.get("/search/query")
async def search_query(username: str, flavor_type: str="", req_name: str=""):
    if flavor_type!="" and req_name!="":
        command=f"""
        SELECT * FROM search WHERE "username"='{username}' and "flavor_type"='{flavor_type}' and "req_name" like '%{req_name}%'
        """
    elif flavor_type!="":
        command=f"""
        SELECT * FROM search WHERE "username"='{username}' and "flavor_type"='{flavor_type}'
        """
    elif req_name!="":
        command=f"""
        SELECT * FROM search WHERE "username"='{username}' and "req_name" like '%{req_name}%'
        """
    else:
        command=f"""
        SELECT * FROM search WHERE "username"='{username}'
        """
    try:
        result=await fetch_all(command)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return result
