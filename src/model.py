import datetime
from typing import Optional
import pydantic

class search(pydantic.BaseModel):
	user_id:int
	flavor_type:str
	req_name:str
	req_description:Optional[str]
	price:float
	end_time:datetime.date
	photo:Optional[bytes]
	crea_time:datetime.datetime
	mod_time:datetime.datetime
	state:int

	@pydantic.validator("user_id", pre=True)
	def parse_userid(cls, value):
		try:
			value = int(value)
		except Exception:
			return None
		return value
	@pydantic.validator("price", pre=True)
	def parse_price(cls, value):
		try:
			value = float(value)
		except Exception:
			return None
		return value
	@pydantic.validator("state", pre=True)
	def parse_state(cls, value):
		try:
			value = int(value)
		except Exception:
			return None
		return value

class searchInDB(search):
	id:int

class taste(pydantic.BaseModel):
	req_id:int
	user_id:int
	description:Optional[str]
	crea_time:datetime.datetime
	mod_time:datetime.datetime
	state:int
	
	@pydantic.validator("req_id", pre=True)
	def parse_reqid(cls, value):
		try:
			value = int(value)
		except Exception:
			return None
		return value
	@pydantic.validator("user_id", pre=True)
	def parse_userid(cls, value):
		try:
			value = int(value)
		except Exception:
			return None
		return value
	@pydantic.validator("state", pre=True)
	def parse_state(cls, value):
		try:
			value = int(value)
		except Exception:
			return None
		return value

class tasteInDB(taste):
	id:int

class success(pydantic.BaseModel):
	req_id:int
	user1_id:int
	user2_id:int
	finish_time:datetime.date
	fee1:float
	fee2:float
	
	@pydantic.validator("req_id", pre=True)
	def parse_reqid(cls, value):
		try:
			value = int(value)
		except Exception:
			return None
		return value
	@pydantic.validator("user1_id", pre=True)
	def parse_user1id(cls, value):
		try:
			value = int(value)
		except Exception:
			return None
		return value
	@pydantic.validator("user2_id", pre=True)
	def parse_user2id(cls, value):
		try:
			value = int(value)
		except Exception:
			return None
		return value
	@pydantic.validator("fee1", pre=True)
	def parse_fee1(cls, value):
		try:
			value = float(value)
		except Exception:
			return None
		return value
	@pydantic.validator("fee2", pre=True)
	def parse_fee2(cls, value):
		try:
			value = float(value)
		except Exception:
			return None
		return value