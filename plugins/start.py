import asyncio
import shutil
import humanize
from time import sleep
from config import Config
from script import Txt
from helper.database import db
from pyrogram.errors import FloodWait
from pyrogram import Client, filters, enums
from .check_user_status import handle_user_status
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message((filters.private | filters.group))
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)

@Client.on_message((filters.private | filters.group) & filters.command('start'))
async def Handle_StartMsg(bot:Client, msg:Message):

    Snowdev = await msg.reply_text(text= '**Please Wait...**', reply_to_message_id=msg.id)

    if msg.chat.type == enums.ChatType.SUPERGROUP and not await db.is_user_exist(msg.from_user.id):
        botusername = await bot.get_me()
        btn = [
            [InlineKeyboardButton(text='⚡ BOT PM', url=f'https://t.me/{botusername.username}')],
            [InlineKeyboardButton(text='📢 Uᴘᴅᴀᴛᴇs', url='https://t.me/The_TGguy')]
        ]

        await Snowdev.edit(text=Txt.GROUP_START_MSG.format(msg.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))
    
    else:
        btn = [
            [InlineKeyboardButton(text='❗ Hᴇʟᴘ', callback_data='help'), InlineKeyboardButton(text='🌨️ Aʙᴏᴜᴛ', callback_data='about')],
            [InlineKeyboardButton(text='📢 Uᴘᴅᴀᴛᴇs', url='https://t.me/The_TGguy'), InlineKeyboardButton(text='💻 Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/TGguy_Ownerobot')]
        ]

        if Config.START_PIC:
            await Snowdev.delete()
            await msg.reply_photo(photo=Config.START_PIC, caption=Txt.PRIVATE_START_MSG.format(msg.from_user.mention), reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)
        else:
            await Snowdev.delete()
            await msg.reply_text(text=Txt.PRIVATE_START_MSG.format(msg.from_user.mention), reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)
            
    

@Client.on_message((filters.private | filters.group) & (filters.document | filters.audio | filters.video))
async def Files_Option(bot:Client, message:Message):
    
    SnowDev = await message.reply_text(text='**Please Wait**', reply_to_message_id=message.id)

    if message.chat.type == enums.ChatType.SUPERGROUP and not await db.is_user_exist(message.from_user.id):
        botusername = await bot.get_me()
        btn = [
            [InlineKeyboardButton(text='⚡ BOT PM', url=f'https://t.me/{botusername.username}')],
            [InlineKeyboardButton(text='💻 Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/TGguy_Ownerobot')]
        ]

        return await SnowDev.edit(text=Txt.GROUP_START_MSG.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))
        
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)


    try:
        text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""

        buttons = [[InlineKeyboardButton("Rᴇɴᴀᴍᴇ 📝", callback_data=f"rename-{message.from_user.id}")],
                   [InlineKeyboardButton("Cᴏᴍᴘʀᴇss 🗜️", callback_data=f"compress-{message.from_user.id}")]]
        await SnowDev.edit(text=text, reply_markup=InlineKeyboardMarkup(buttons))
        
    except FloodWait as e:
        
        floodmsg = await message.reply_text(f"**😥 Pʟᴇᴀsᴇ Wᴀɪᴛ ᴅᴏɴ'ᴛ ᴅᴏ ғʟᴏᴏᴅɪɴɢ ᴡᴀɪᴛ ғᴏʀ {e.value} Sᴇᴄᴄᴏɴᴅs**", reply_to_message_id=message.id)
        await sleep(e.value)
        await floodmsg.delete()

        text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
        buttons = [[InlineKeyboardButton("Rᴇɴᴀᴍᴇ 📝", callback_data=f"rename-{message.from_user.id}")],
                   [InlineKeyboardButton("Cᴏᴍᴘʀᴇss 🗜️", callback_data=f"compress-{message.from_user.id}")]]
        await SnowDev.edit(text=text, reply_markup=InlineKeyboardMarkup(buttons))

    except Exception as e:
        print(e)

@Client.on_message(filters.command("rqueue") & filters.private)
async def handle_rqueue(client: Client, message: Message):
    """Handles the /rqueue command to remove a file from the queue."""
    try:
        queue_position = message.command[1]  # Get queue position from command
        await cancelqueue(client, message, queue_position)
    except IndexError:
        await message.reply_text("Please specify the queue position to remove (e.g., /rqueue 2)")
    except Exception as e:
        print(f"Error in rqueue handler: {e}")
        await message.reply_text(f"An error occurred: {e}")


@Client.on_message(filters.command("vqueue") & filters.private)
async def handle_vqueue(client: Client, message: Message):
    """Handles the /vqueue command to list files in the queue."""
    queue_list = "<b>Queue:</b>\n"
    temp_list = []
    count = 1
    
    # Get current user id
    user_id = message.from_user.id
    
    # Iterate all queue
    while not QUEUE.empty():
      item = await QUEUE.get()
      bot, query, ffmpegcode, c_thumb, ms = item
      temp_list.append(item)
      user_name = query.from_user.first_name or query.from_user.username
      file = query.message.reply_to_message
      file_name = getattr(file , file.media.value).file_name
      queue_list += f"{count}. {file_name} - {user_name} ({user_id})\n"
      count += 1
      
    # Put items in queue
    for item in temp_list:
      await QUEUE.put(item)
    
    if count == 1: # Queue is empty
      queue_list = "Queue is empty"

    await message.reply_text(queue_list, parse_mode=enums.ParseMode.HTML)


@Client.on_message(filters.command("hwn") & filters.private)
async def handle_hwn(client: Client, message: Message):
    """Handles the /hwn command to display help text."""
    await message.reply_text(Txt.help_wm, parse_mode=enums.ParseMode.HTML)
    
@Client.on_message((filters.private | filters.group) & filters.command('cancel'))
async def cancel_process(bot:Client, message:Message):
    
    try:
        shutil.rmtree(f"encode/{message.from_user.id}")
        shutil.rmtree(f"ffmpeg/{message.from_user.id}")
        shutil.rmtree(f"Renames/{message.from_user.id}")
        shutil.rmtree(f"Metadata/{message.from_user.id}")
        shutil.rmtree(f"Screenshot_Generation/{message.from_user.id}")
        
        return await message.reply_text(text="**Canceled All On Going Processes ✅**")
    except BaseException:
        pass
