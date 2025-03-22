
import asyncio
import math, time
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

# Dictionary to store queues for each user
USER_QUEUES = {}
USER_STATUS = {}  # Track user's processing status

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
    ms = await message.reply_text(text="Sᴏʀʀʏ Yᴏᴜ Cᴀɴ'ᴛ Cᴏɴғɪɢ Yᴏᴜʀ Sᴇᴛᴛɪɴɢs\n\nFɪʀsᴛ sᴛᴀʀᴛ ᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍʏ ғᴇᴀᴛᴜʀs ɪɴ ɢʀᴏᴜᴘ", reply_to_message_id = message.id, reply_markup=InlineKeyboardMarkup(btn))

    await asyncio.sleep(10)
    await ms.delete()


async def Compress_Stats(e, userid):


    if int(userid) not in [e.from_user.id, 0]:
        return await e.answer(f"⚠️ Hᴇʏ {e.from_user.first_name}\nYᴏᴜ ᴄᴀɴ'ᴛ sᴇᴇ sᴛᴀᴛᴜs ᴀs ᴛʜɪs ɪs ɴᴏᴛ ʏᴏᴜʀ ғɪʟᴇ", show_alert=True)
    
    inp = f"ffmpeg/{e.from_user.id}/{os.listdir(f'ffmpeg/{e.from_user.id}')[0]}"
    outp = f"encode/{e.from_user.id}/{os.listdir(f'encode/{e.from_user.id}')[0]}"
    try:
        ot = humanbytes(int((Path(outp).stat().st_size)))
        ov = humanbytes(int(Path(inp).stat().st_size))
        processing_file_name = inp.replace(f"ffmpeg/{userid}/", "").replace(f"_", " ")
        ans = f"Processing Media: {processing_file_name}\n\nDownloaded: {ov}\n\nCompressed: {ot}"
        await e.answer(ans, cache_time=0, show_alert=True)
    except Exception as er:
        print(er)
        await e.answer(
            "Someting Went Wrong.\nSend Media Again.", cache_time=0, alert=True
        )

async def skip(e, userid):

    if int(userid) not in [e.from_user.id, 0]:
        return await e.answer(f"⚠️ Hᴇʏ {e.from_user.first_name}\nYᴏᴜ ᴄᴀɴ'ᴛ ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴇss ᴀs ʏᴏᴜ ᴅɪᴅɴ'ᴛ sᴛᴀʀᴛ ɪᴛ", show_alert=True)
    try:
        await e.message.delete()
        os.system(f"rm -rf ffmpeg/{userid}*")
        os.system(f"rm -rf encode/{userid}*")
        for proc in psutil.process_iter():
            processName = proc.name()
            processID = proc.pid
            print(processName , ' - ', processID)
            if(processName == "ffmpeg"):
             os.kill(processID,signal.SIGKILL)
    except Exception as e:
        pass
    try:
        shutil.rmtree(f'ffmpeg' + '/' + str(userid))
        shutil.rmtree(f'encode' + '/' + str(userid))
    except Exception as e:
        pass
    
    return

async def CompressVideo(bot, query, ffmpegcode, c_thumb):
    UID = query.from_user.id
    ms = await query.message.edit('Pʟᴇᴀsᴇ Wᴀɪᴛ...\n\n**Fᴇᴛᴄʜɪɴɢ Qᴜᴇᴜᴇ 👥**')

    # Create user queue if it doesn't exist
    if UID not in USER_QUEUES:
        USER_QUEUES[UID] = []

    if UID not in USER_STATUS:
        USER_STATUS[UID] = False  # Initially, no processing is going on


    #Gather video details for the queue
    media = query.message.reply_to_message
    file = getattr(media , media.media.value)
    filename = Filename(filename=str(file.file_name), mime_type=str(file.mime_type))
    Download_DIR = f"ffmpeg/{UID}"
    Output_DIR = f"encode/{UID}"
    File_Path = f"ffmpeg/{UID}/{filename}"
    Output_Path = f"encode/{UID}/{filename}"

    video_data = {
        'bot': bot,
        'query': query,
        'ffmpegcode': ffmpegcode,
        'c_thumb': c_thumb,
        'filename': filename,
        'Download_DIR': Download_DIR,
        'Output_DIR': Output_DIR,
        'File_Path': File_Path,
        'Output_Path': Output_Path,
        'ms': ms  # Store the message object for updates
    }


    # Check if a process is already running for this user
    #if os.path.isdir(f'ffmpeg/{UID}') and os.path.isdir(f'encode/{UID}'): # This condition not good for Status check
    if USER_STATUS[UID]: #Correct one to check status
        # Add the video to the queue
        USER_QUEUES[UID].append(video_data)
        await ms.edit("Added to queue.  You'll be notified when processing starts.")
    else:
        #Start processing immediately
        USER_STATUS[UID] = True  # Set status to processing
        await process_video(video_data)


#This is a dummy function for sending message to user.
async def send_message(chat_id, text, reply_markup=None):
    try:
        await bot.send_message(chat_id, text, reply_markup=reply_markup)
    except Exception as e:
        print(f"Failed to send message: {e}")

async def process_video(video_data):
    bot = video_data['bot']
    query = video_data['query']
    ffmpegcode = video_data['ffmpegcode']
    c_thumb = video_data['c_thumb']
    filename = video_data['filename']
    Download_DIR = video_data['Download_DIR']
    Output_DIR = video_data['Output_DIR']
    File_Path = video_data['File_Path']
    Output_Path = video_data['Output_Path']
    UID = query.from_user.id
    ms = video_data['ms']

    try:
        await ms.edit('⚠️__**Please wait...**__\n**Tʀyɪɴɢ Tᴏ Dᴏᴡɴʟᴏᴀᴅɪɴɢ....**')
        s = dt.now()
        try:
            if not os.path.isdir(Download_DIR) and not os.path.isdir(Output_DIR):
                os.makedirs(Download_DIR)
                os.makedirs(Output_DIR)

                dl = await bot.download_media(
                    message=query.message.reply_to_message, #Used video_data['query'] before
                    file_name=File_Path,
                    progress=progress_for_pyrogram,
                    progress_args=("\n⚠️__**Please wait...**__\n\n☃️ **Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
                )
        except Exception as e:
            return await ms.edit(str(e))
        
        es = dt.now()
        dtime = ts(int((es - s).seconds) * 1000)

        await ms.edit(
            "**🗜 Compressing...**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Sᴛᴀᴛs', callback_data=f'stats-{UID}')],
                [InlineKeyboardButton(text='Cᴀɴᴄᴇʟ', callback_data=f'skip-{UID}')]
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
                await ms.edit(str(er) + "\n\n**Error**")
                shutil.rmtree(f"ffmpeg/{UID}")
                shutil.rmtree(f"encode/{UID}")
                return
        except BaseException:
            pass
        

        # Clean up resources
        # Now Uploading to the User
        ees = dt.now()
        
        if (query.message.reply_to_message.thumbs or c_thumb): #Used video_data['query'] before
            if c_thumb:
                ph_path = await bot.download_media(c_thumb)
            else:
                ph_path = await bot.download_media(query.message.reply_to_message.thumbs[0].file_id) #Used video_data['query'] before

        org = int(Path(File_Path).stat().st_size)
        com = int((Path(Output_Path).stat().st_size))
        pe = 100 - ((com / org) * 100)
        per = str(f"{pe:.2f}")  + "%"
        eees = dt.now()
        x = dtime
        xx = ts(int((ees - es).seconds) * 1000)
        xxx = ts(int((eees - ees).seconds) * 1000)
        await ms.edit("⚠️__**Please wait...**__\n**Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅɪɴɢ....**")
        await bot.send_document(
                UID,
                document=Output_Path,
                thumb=ph_path,
                caption=Config.caption.format(filename, humanbytes(org), humanbytes(com) , per, x, xx, xxx),
                progress=progress_for_pyrogram,
                progress_args=("⚠️__**Please wait...**__\n🌨️ **Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time()))
        
        if query.message.chat.type == enums.ChatType.SUPERGROUP: #Used video_data['query'] before
            botusername = await bot.get_me()
            await ms.edit(f"Hey {query.from_user.mention},\n\nI Have Send Compressed File To Your Pm", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Bᴏᴛ Pᴍ", url=f'https://t.me/{botusername.username}')]]))
            
        else:
            await ms.delete()

        #await cleanup_resources(UID, ph_path) # Use await Removed here

    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    finally: #Important to Process Next In Queue after success/failure
        await cleanup_resources(UID, ph_path)
        USER_STATUS[UID] = False  # Reset processing status
        await process_next_in_queue(UID)


#3. Add the `process_next_in_queue` function and `cleanup_resources` function
async def process_next_in_queue(user_id):
    if user_id in USER_QUEUES and USER_QUEUES[user_id]:
        # Get the next video from the queue
        next_video = USER_QUEUES[user_id].pop(0)  # Remove the first item
        USER_STATUS[user_id] = True # Important to enable processing
        await process_video(next_video)
    else:
        # No more videos in the queue, cleanup directories
        #await cleanup_resources(user_id) # Removed Here for better
        pass

async def cleanup_resources(user_id, ph_path=None):
    try:
        shutil.rmtree(f"ffmpeg/{user_id}")
        shutil.rmtree(f"encode/{user_id}")
        if ph_path:
            os.remove(ph_path)
    except Exception as e:
        print(f"Error cleaning up resources: {e}")
