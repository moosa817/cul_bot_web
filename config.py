import os 
user = os.getenv("user", default=None)
pwd = os.getenv("pwd", default=None)
admin = os.getenv("admin", default=None)
admin_pwd = os.getenv("admin_pwd", default=None)
mongo_str = os.getenv("mongo_str",default=None)