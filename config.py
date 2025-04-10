import os, time, re

id_pattern = re.compile(r'^.\d+$') 


class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "")  # ⚠️ Fuck you
    API_HASH  = os.environ.get("API_HASH", "") # ⚠️ Stealer
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "") # ⚠️ You are such a failure 😂 
    FORCE_SUB = os.environ.get('FORCE_SUB', 'The_TGguy') # ⚠️ Required
    AUTH_CHANNEL = int(FORCE_SUB) if FORCE_SUB and id_pattern.search(
    FORCE_SUB) else None
   
    # database config
    DB_URL  = os.environ.get("DB_URL", "")  # ⚠️ Required
    DB_NAME  = os.environ.get("DB_NAME","sjjabaosnwkzjanx") 

    # Other Configs 
    ADMIN = int(os.environ.get("ADMIN", "1705634892")) # ⚠️ Required
    LOG_CHANNEL = int(os.environ.get('LOG_CHANNEL', '-1002288135729')) # ⚠️ Required
    BOT_UPTIME = BOT_UPTIME  = time.time()
    START_PIC = os.environ.get("START_PIC", "https://graph.org/file/ef699b1666a548a9b8417-36129fecd7753dbca0.jpg")

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))


    caption = """
{0}
"""
