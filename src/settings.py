import datetime
from enum import Enum
import re
import json
import platform
from statistics import mode

from src import model


class Settings:
    """
    Databse
    """
    DATABASE_USER = "postgres"
    DATABASE_PASSWORD = "password"
    DEFAULT_DATABASE = "tb"

    """
	User Rule
	"""
    USERNAME_MAX_LENGTH = 32
    USERNAME_MIN_LENGTH = 1
    PASSWORD_MAX_LENGTH = 32
    PASSWORD_MIN_LENGTH = 6
    #这里使用正则表达式中的前视断言，密码由字母和数字组成，必须包含两个数字，不能都为大写或小写
    PASSWORD_RULE = re.compile("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9].*[0-9])[A-Za-z0-9]*$") 
    NUMBER_RULE = re.compile("^[0-9]*$")

    """
	User Token
	"""
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 720  # 12小时
    PAYLOAD_NAME = "bupt"

    """
	Router
	"""
    DATA_ROUTER_PREFIX = "/data"

    MAX_ROW_PER_FILE = 50000
    TEMPDIR = ".tb"

str2Model = {
    str.lower(key):value for key,value in vars(model).items() if key.startswith("tb")
}


try:
    _config = json.load(open("config.json"))
except FileNotFoundError:
    print("缺少数据库配置文件，默认按照user=postgres连接")
    Settings.DATABASE_USER = "postgres"
    Settings.DATABASE_PASSWORD = None
else:
    Settings.DATABASE_USER = _config.get("username", "postgres")
    Settings.DATABASE_PASSWORD = _config.get("password", None)

import os

if(platform.system() == 'Windows'):
    Settings.TEMPDIR = os.path.join(os.getcwd(),Settings.TEMPDIR)
else:
    Settings.TEMPDIR = os.path.join("/tmp",Settings.TEMPDIR)
