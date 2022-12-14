from ..model import search, searchInDB, taste, tasteInDB,success
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
        'INSERT INTO search ("user_id", "flavor_type","req_name","req_description","price","end_time","photo","crea_time","mod_time","state") VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)'\
        ,s.user_id, s.flavor_type, s.req_name, s.req_description, s.price, s.end_time\
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
        'INSERT INTO search ("id", "user_id", "flavor_type","req_name","req_description","price","end_time","photo","crea_time","mod_time","state") VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)'\
        ,s.id, s.user_id, s.flavor_type, s.req_name, s.req_description, s.price, s.end_time\
        ,s.photo, s.crea_time, s.mod_time, s.state)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return "ok"

@data_router.post("/search/update_state")
async def update_state1(id: int, s: int):
    """用于更新“寻味道”表中的state字段
    """
    try:
        await fetch_one('UPDATE search SET state = $1 WHERE id = $2',s,id)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return "ok"

@data_router.get("/search/query1")
async def search_query1(user_id: int):
    """用于查询某一用户发布的所有“寻味道”
    """
    command=f"""
    SELECT * FROM search WHERE "user_id"={user_id}
    """
    try:
        result=await fetch_all(command)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return result

@data_router.get("/search/query2")
async def search_query2(city: str):
    """用于查询同地区的“寻味道”信息
    """
    command=f"""
    SELECT search.* FROM search JOIN myuser ON search."user_id"=myuser."id"
    WHERE myuser."city"='{city}'
    """
    try:
        result=await fetch_all(command)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return result

@data_router.post("/taste/add")
async def taste_add(s: taste):
    try:
        await fetch_one(\
        'INSERT INTO taste ("req_id", "user_id","description","crea_time","mod_time","state") VALUES ($1,$2,$3,$4,$5,$6)'\
        ,s.req_id, s.user_id, s.description, s.crea_time, s.mod_time, s.state)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return "ok"

@data_router.post("/taste/delete")
async def taste_delete(id: int):
    try:
        await fetch_one('DELETE FROM taste WHERE "id"=$1',id)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return "ok"

@data_router.post("/taste/change")
async def taste_change(s: tasteInDB):
    try:
        await fetch_one(\
        'INSERT INTO taste ("id", "req_id", "user_id","description","crea_time","mod_time","state") VALUES ($1,$2,$3,$4,$5,$6,$7)'\
        ,s.id, s.req_id, s.user_id, s.description, s.crea_time, s.mod_time, s.state)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return "ok"

@data_router.post("/taste/update_state")
async def update_state2(id: int, s: int):
    """用于更新“请品鉴”表中的state字段
    """
    try:
        await fetch_one('UPDATE taste SET state = $1 WHERE id = $2',s,id)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return "ok"

@data_router.get("/taste/query1")
async def taste_query1(user_id: int):
    """用于查询某一用户发布的“请品鉴”
    """
    command=f"""
    SELECT * FROM taste WHERE "user_id"={user_id}
    """
    try:
        result=await fetch_all(command)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return result

@data_router.get("/taste/query2")
async def taste_query2(user_id: int):
    """用于查询某一用户收到的“请品鉴”
    """
    command=f"""
    SELECT taste.* FROM search JOIN taste ON search."id"=taste."req_id"
    WHERE search."user_id"={user_id}
    """
    try:
        result=await fetch_all(command)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    return result

@data_router.post("/success_add")
async def success_add(s: success):
    """用于增加一条成功记录并更改统计表信息
    """
    try:
        await fetch_one(\
        'INSERT INTO success ("req_id", "user1_id","user2_id","finish_time","fee1","fee2") VALUES ($1,$2,$3,$4,$5,$6)'\
        ,s.req_id, s.user1_id, s.user2_id, s.finish_time, s.fee1, s.fee2)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()

    year=s.finish_time.year
    month=s.finish_time.month
    t=str(year).zfill(4)+str(month).zfill(2)

    command1=f"""
        SELECT * FROM myuser WHERE "id"={s.user1_id}
    """
    result1=await fetch_one(command1)
    city=result1[10]

    command2=f"""
        SELECT * FROM search WHERE "id"={s.req_id}
    """
    result2=await fetch_one(command2)
    type=result2[2]

    command3=f"""
        SELECT * FROM income WHERE "month"='{t}' and "city"='{city}' and "type"='{type}'
    """
    result3=await fetch_all(command3)

    num=1
    fee=s.fee1+s.fee2
    if len(result3)!=0:
        num=result3[0][3]+1
        fee=result3[0][4]+s.fee1+s.fee2
    
    try:
        await fetch_one(\
        'INSERT INTO income ("month", "city", "type","number","money") VALUES ($1,$2,$3,$4,$5)'\
        ,t, city, type, num, fee)
    except asyncpg.PostgresError as e:
        print(e)
        raise OperationFailed()
    
    return "ok"

