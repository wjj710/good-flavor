import datetime
from typing import Optional
import pydantic

class search(pydantic.BaseModel):
	username:str
	flavor_type:str
	req_name:str
	req_description:Optional[str]
	price:float
	end_time:datetime.date
	photo:Optional[bytes]
	crea_time:datetime.datetime
	mod_time:datetime.datetime
	state:int
	
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