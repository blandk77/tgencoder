import asyncio
import math, time
import string
import random
from . import *
from datetime import datetime as dt
import sys
import shutil
import signal
import os
from pathlib import Path
from datetime import datetime
import psutil
from pytz import timezone
from config import Config
from script import Txt
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from pymongo import MongoClient

# MongoDB setup
MONGO_URI = Config.DB_URL
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['encoding_bot']
queue_collection = db['queue']


ENCODING_LOCK = asyncio.Lock()

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:        
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "{0}{1}".format(
            ''.join(["⬢" for i in range(math.floor(percentage / 5))]),
            ''.join(["⬡" for i in range(20 - math.floor(percentage / 5))])
        )            
        tmp = progress + Txt.PROGRESS_BAR.format( 
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),            
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text=f"{ud_type}\n\n{tmp}",               
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data=f"close-{message.from_user.id}")]])                                               
            )
        except:
            pass

def humanbytes(size):    
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "ᴅ, ") if days else "") + \
        ((str(hours) + "ʜ, ") if hours else "") + \
        ((str(minutes) + "ᴍ, ") if minutes else "") + \
        ((str(seconds) + "ꜱ, ") if seconds else "") + \
        ((str(milliseconds) + "ᴍꜱ, ") if milliseconds else "")
    return tmp[:-2] 

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def ts(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ms, ") if milliseconds else "")
    )
    return tmp[:-2]

async def send_log(b, u):
    if Config.LOG_CHANNEL is not None:
        botusername = await b.get_me()
        curr = datetime.now(timezone("Asia/Kolkata"))
        date = curr.strftime('%d %B, %Y')
        time = curr.strftime('%I:%M:%S %p')
        await b.send_message(
            Config.LOG_CHANNEL,
            f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\nUꜱᴇʀ: {u.mention}\nIᴅ: `{u.id}`\nUɴ: @{u.username}\n\nDᴀᴛᴇ: {date}\nTɪᴍᴇ: {time}\n\nBy: @{botusername.username}"
        )

def Filename(filename, mime_type):
    if filename.split('.')[-1] in ['mkv', 'mp4', 'mp3', 'mov']:
        return filename
    else:
        if mime_type.split('/')[1] in ['pdf', 'mkv', 'mp4', 'mp3']:
            return f"{filename}.{mime_type.split('/')[1]}"
        elif mime_type.split('/')[0] == "audio":
            return f"{filename}.mp3"
        else:
            return f"{filename}.mkv"

async def CANT_CONFIG_GROUP_MSG(client, message):
    botusername = await client.get_me()
    btn = [
        [InlineKeyboardButton(text='Bᴏᴛ Pᴍ', url=f'https://t.me/{botusername.username}')]
    ]
    ms = await message.reply_text(text="Sᴏʀʀʏ Yᴏᴜ Cᴀɴ'ᴛ Cᴏɴғɪɢ Yᴏᴜʀ Sᴇᴛᴛɪɴɢs\n\nFɪʀsᴛ sᴛᴀʀᴛ ᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍʏ ғᴇᴀᴛᴜʀᴇs ɪɴ ɢʀᴏᴜᴘ", reply_to_message_id = message.id, reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(10)
    await ms.delete()

async def Compress_Stats(e, task_id):
    task = queue_collection.find_one({"task_id": task_id})
    if not task:
        return await e.answer("Task not found.", show_alert=True)
    
    if int(task["user_id"]) != e.from_user.id:
        return await e.answer(f"⚠️ Hᴇʏ {e.from_user.first_name}\nYᴏᴜ ᴄᴀɴ'ᴛ sᴇᴇ sᴛᴀᴛᴜs ᴀs ᴛʜɪs ɪs ɴᴏᴛ ʏᴏᴜʀ ғɪʟᴇ", show_alert=True)
    
    inp = f"ffmpeg/{task['user_id']}/{task['filename']}"
    outp = f"encode/{task['user_id']}/{task['filename']}"
    try:
        ot = humanbytes(int((Path(outp).stat().st_size)))
        ov = humanbytes(int(Path(inp).stat().st_size))
        ans = f"Processing Media: {task['filename']}\n\nDownloaded: {ov}\n\nCompressed: {ot}"
        await e.answer(ans, cache_time=0, show_alert=True)
    except Exception as er:
        print(er)
        await e.answer("Something Went Wrong.\nSend Media Again.", cache_time=0, alert=True)

async def skip(e, task_id):
    task = queue_collection.find_one({"task_id": task_id})
    if not task:
        return await e.answer("Task not found.", show_alert=True)
    
    if int(task["user_id"]) != e.from_user.id:
        return await e.answer(f"⚠️ Hᴇʏ {e.from_user.first_name}\nYᴏᴜ ᴄᴀɴ'ᴛ ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴇss ᴀs ʏᴏᴜ ᴅɪᴅɴ'ᴛ sᴛᴀʀᴛ ɪᴛ", show_alert=True)
    
    try:
        await e.message.delete()
        os.system(f"rm -rf ffmpeg/{task['user_id']}/*")
        os.system(f"rm -rf encode/{task['user_id']}/*")
        for proc in psutil.process_iter():
            processName = proc.name()
            processID = proc.pid
            if processName == "ffmpeg":
                os.kill(processID, signal.SIGKILL)
    except Exception as e:
        pass
    try:
        shutil.rmtree(f'ffmpeg/{task["user_id"]}')
        shutil.rmtree(f'encode/{task["user_id"]}')
        queue_collection.delete_one({"task_id": task_id})
    except Exception as e:
        pass
    return

def generate_task_id():
    return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*:", k=5))

async def add_to_queue(bot, query, ffmpegcode, c_thumb):
    media = query.message.reply_to_message
    if not media or not media.media:
        return await query.message.edit("Please reply to a media file.")
    
    file = getattr(media, media.media.value)
    filename = Filename(filename=str(file.file_name), mime_type=str(file.mime_type))
    user_id = query.from_user.id
    username = query.from_user.username or query.from_user.first_name
    
    task_id = generate_task_id()
    while queue_collection.find_one({"task_id": task_id}):
        task_id = generate_task_id()
    
    task = {
        "task_id": task_id,
        "user_id": user_id,
        "username": username,
        "filename": filename,
        "file_size": file.file_size,
        "ffmpegcode": ffmpegcode,
        "c_thumb": c_thumb,
        "status": "in_queue",
        "message_id": query.message.id,
        "chat_id": query.message.chat.id,
        "added_at": datetime.now()
    }
    queue_collection.insert_one(task)
    await query.message.edit(f"Task added to queue with Task ID: `{task_id}`\nUse /queue to view the queue.")
    
    # Start processing if queue was empty
    if queue_collection.count_documents({"status": "encoding"}) == 0:
        await process_queue(bot)

async def process_queue(bot):
    async with ENCODING_LOCK:
        while True:
            task = queue_collection.find_one_and_update(
                {"status": "in_queue"},
                {"$set": {"status": "encoding"}},
                sort=[("added_at", 1)]
            )
            if not task:
                break
            
            try:
                await process_task(bot, task)
            except Exception as e:
                print(f"Error processing task {task['task_id']}: {e}")
                queue_collection.delete_one({"task_id": task["task_id"]})
                try:
                    shutil.rmtree(f"ffmpeg/{task['user_id']}")
                    shutil.rmtree(f"encode/{task['user_id']}")
                except:
                    pass
            finally:
                queue_collection.delete_one({"task_id": task["task_id"]})

async def process_task(bot, task):
    UID = task["user_id"]
    filename = task["filename"]
    ffmpegcode = task["ffmpegcode"]
    c_thumb = task["c_thumb"]
    task_id = task["task_id"]
    message = await bot.get_messages(task["chat_id"], task["message_id"])
    
    Download_DIR = f"ffmpeg/{UID}"
    Output_DIR = f"encode/{UID}"
    File_Path = f"ffmpeg/{UID}/{filename}"
    Output_Path = f"encode/{UID}/{filename}"
    
    await message.edit('⚠️__**Please wait...**__\n**Tʀyɪɴɢ Tᴏ Dᴏᴡɴʟᴏᴀᴅɪɴɢ....**')
    s = dt.now()
    try:
        if not os.path.isdir(Download_DIR) and not os.path.isdir(Output_DIR):
            os.makedirs(Download_DIR)
            os.makedirs(Output_DIR)
        
        media = message.reply_to_message
        file = getattr(media, media.media.value)
        dl = await bot.download_media(
            message=file,
            file_name=File_Path,
            progress=progress_for_pyrogram,
            progress_args=("\n⚠️__**Please wait...**__\n☃️ **Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**", message, time.time())
        )
    except Exception as e:
        await message.edit(str(e))
        raise e
    
    es = dt.now()
    dtime = ts(int((es - s).seconds) * 1000)
    
    await message.edit(
        "**🗜 Compressing...**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Sᴛᴀᴛs', callback_data=f'stats-{task_id}')],
            [InlineKeyboardButton(text='Cᴀɴᴄᴇʟ', callback_data=f'skip-{task_id}')]
        ])
    )
    
    cmd = f"""ffmpeg -i "{dl}" {ffmpegcode} "{Output_Path}" -y"""
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    er = stderr.decode()
    
    try:
        if er:
            await message.edit(str(er) + "\n\n**Error**")
            raise Exception(er)
    except BaseException:
        pass
    
    ees = dt.now()
    
    if (file.thumbs or c_thumb):
        if c_thumb:
            ph_path = await bot.download_media(c_thumb)
        else:
            ph_path = await bot.download_media(file.thumbs[0].file_id)
    
    org = int(Path(File_Path).stat().st_size)
    com = int((Path(Output_Path).stat().st_size))
    pe = 100 - ((com / org) * 100)
    per = str(f"{pe:.2f}") + "%"
    eees = dt.now()
    x = dtime
    xx = ts(int((ees - es).seconds) * 1000)
    xxx = ts(int((eees - ees).seconds) * 1000)
    await message.edit("⚠️__**Please wait...**__\n**Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅɪɴɢ....**")
    await bot.send_document(
        UID,
        document=Output_Path,
        thumb=ph_path,
        caption=Config.caption.format(filename, humanbytes(org), humanbytes(com), per, x, xx, xxx),
        progress=progress_for_pyrogram,
        progress_args=("⚠️__**Please wait...**__\n🌨️ **Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....**", message, time.time())
    )
    
    if message.chat.type == enums.ChatType.SUPERGROUP:
        botusername = await bot.get_me()
        await message.edit(f"Hey {message.reply_to_message.from_user.mention},\n\nI Have Sent Compressed File To Your PM", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Bᴏᴛ Pᴍ", url=f'https://t.me/{botusername.username}')]]))
    else:
        await message.delete()
    
    try:
        shutil.rmtree(f"ffmpeg/{UID}")
        shutil.rmtree(f"encode/{UID}")
        os.remove(ph_path)
    except:
        pass

async def CompressVideo(bot, query, ffmpegcode, c_thumb):
    async with ENCODING_LOCK:
        if queue_collection.count_documents({"status": "encoding"}) > 0:
            await add_to_queue(bot, query, ffmpegcode, c_thumb)
        else:
            await add_to_queue(bot, query, ffmpegcode, c_thumb)
