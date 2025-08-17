from dotenv import load_dotenv
from  os import getenv

load_dotenv() 

user_id=getenv("user_id")
Redirect=getenv("Redirect")
Client=getenv("Client")
Client_Secret=getenv("Client_Secret")

skills=getenv("skills")
personal=getenv("personal")
promt=getenv("promt")

description=""
#URL
global_url=getenv("global_url")
auth_url=getenv("auth_url")
token_url=getenv("token_url")
another_account=getenv("another_account")
response=getenv("response")
url_auth_cookie=getenv("url_auth_cookie")
password=getenv("password")