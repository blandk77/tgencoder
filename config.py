import os, time, re

id_pattern = re.compile(r'^.\d+$') 


class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "26728872")  # ⚠️ Required
    API_HASH  = os.environ.get("API_HASH", "96985c2aaea6c75408528909b7e18879") # ⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7898251858:AAEH62w1B0wWw5M7Fq8J62tebzTH30zXuM4") # ⚠️ Required
    FORCE_SUB = os.environ.get('FORCE_SUB', 'The_TGguy') # ⚠️ Required
    AUTH_CHANNEL = int(FORCE_SUB) if FORCE_SUB and id_pattern.search(
    FORCE_SUB) else None
   
    # database config
    DB_URL  = os.environ.get("DB_URL", "mongodb+srv://Telegram_Guy:I6AfG9KKBJ5397xF@botstore.t3cuf.mongodb.net/?retryWrites=true&w=majority&appName=Botstore")  # ⚠️ Required
    DB_NAME  = os.environ.get("DB_NAME","sjjabakjzkpajanx") 

    # Other Configs 
    ADMIN = int(os.environ.get("ADMIN", "7465574522")) # ⚠️ Required
    LOG_CHANNEL = int(os.environ.get('LOG_CHANNEL', '-1002288135729')) # ⚠️ Required
    BOT_UPTIME = BOT_UPTIME  = time.time()
    START_PIC = os.environ.get("START_PIC", "https://graph.org/file/ef699b1666a548a9b8417-36129fecd7753dbca0.jpg")

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))


    caption = """
{0}
"""    
