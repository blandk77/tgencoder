#Feature Added By https//t.me/The_TGguy
# Telegram Guy!!™
# for support @Itsme123i In Telegram

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper.database import db
from helper.utils import CANT_CONFIG_GROUP_MSG
from script import Txt
from asyncio.exceptions import TimeoutError


@Client.on_message((filters.group | filters.private) & filters.command('set_caption'))
async def add_caption(client, message):

    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return

    if len(message.command) == 1:
        return await message.reply_text("**__Gɪᴠᴇ Tʜᴇ Cᴀᴩᴛɪᴏɴ__\n\nExᴀᴍᴩʟᴇ:- `/set_caption {filename}\n\n💾 Sɪᴢᴇ: {filesize}\n\n⏰ Dᴜʀᴀᴛɪᴏɴ: {duration}`**")

    SnowDev = await message.reply_text(text="**Please Wait...**", reply_to_message_id=message.id)
    caption = message.text.split(" ", 1)[1]
    await db.set_caption(message.from_user.id, caption=caption)
    await message.reply_text("__**✅ Cᴀᴩᴛɪᴏɴ Sᴀᴠᴇᴅ**__")


@Client.on_message((filters.group | filters.private) & filters.command('del_caption'))
async def delete_caption(client, message):

    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return


    SnowDev = await message.reply_text(text="**Please Wait...**", reply_to_message_id=message.id)
    caption = await db.get_caption(message.from_user.id)
    if not caption:
        return await SnowDev.edit("__**😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ**__")
    await db.set_caption(message.from_user.id, caption=None)
    await SnowDev.edit("__**❌️ Cᴀᴩᴛɪᴏɴ Dᴇʟᴇᴛᴇᴅ**__")


@Client.on_message((filters.group | filters.private) & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message):

    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return

    caption = await db.get_caption(message.from_user.id)
    if caption:
        await message.reply_text(f"**Yᴏᴜ'ʀᴇ Cᴀᴩᴛɪᴏɴ:-**\n\n`{caption}`")
    else:
        await message.reply_text("__**😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ**__")


@Client.on_message((filters.group | filters.private) & filters.command(['view_thumb', 'viewthumb']))
async def viewthumb(client, message):

    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return

    SnowDev = await message.reply_text(text="**Please Wait...**", reply_to_message_id=message.id)
    thumb = await db.get_thumbnail(message.from_user.id)
    if thumb:
        await SnowDev.delete()
        await client.send_photo(chat_id=message.chat.id, photo=thumb, reply_to_message_id=message.id)
    else:
        await SnowDev.edit("😔 __**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Tʜᴜᴍʙɴᴀɪʟ**__")


@Client.on_message((filters.group | filters.private) & filters.command(['del_thumb', 'delthumb']))
async def removethumb(client, message):

    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return

    SnowDev = await message.reply_text(text="**Please Wait...**", reply_to_message_id=message.id)
    await db.set_thumbnail(message.from_user.id, thumbnail=None)
    await SnowDev.edit("❌️ __**Tʜᴜᴍʙɴᴀɪʟ Dᴇʟᴇᴛᴇᴅ**__")


@Client.on_message((filters.group | filters.private) & filters.photo)
async def addthumbs(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return

    SnowDev = await message.reply_text(text="**Please Wait...**", reply_to_message_id=message.id)
    await db.set_thumbnail(message.from_user.id, message.photo.file_id)
    await SnowDev.edit("✅️ __**Tʜᴜᴍʙɴᴀɪʟ Sᴀᴠᴇᴅ**__")
    

@Client.on_message((filters.group | filters.private) & filters.command(['set_ffmpeg', 'setffmpeg']))
async def set_ffmpeg(client, message):

    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return
    try:
        ffmpeg = await client.ask(text=Txt.SEND_FFMPEG_CODE, chat_id=message.chat.id,
                            user_id=message.from_user.id, filters=filters.text, timeout=30, disable_web_page_preview=True)
    except TimeoutError:
        await message.reply_text("Error!!\n\nRequest timed out.\nRestart by using /set_ffmpeg", reply_to_message_id=message.id)
        return
        
    await db.set_ffmpegcode(message.from_user.id, ffmpeg.text)
    await message.reply_text("✅ __**Fғᴍᴘᴇɢ Cᴏᴅᴇ Sᴀᴠᴇᴅ**__", reply_to_message_id=message.id)


@Client.on_message((filters.group | filters.private) & filters.command(['see_ffmpeg', 'seeffmpeg']))
async def see_ffmpeg(client, message):

    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return

    SnowDev = await message.reply_text(text="**Please Wait...**", reply_to_message_id=message.id)

    ffmpeg = await db.get_ffmpegcode(message.from_user.id)
    
    if ffmpeg:
        await SnowDev.edit(f"✅ <b>Yᴏᴜʀ Cᴜʀʀᴇɴᴛ Fғᴍᴘᴇɢ Cᴏᴅᴇ ɪs :-</b>\n\n<code>{ffmpeg}</code>")
    else:
        await SnowDev.edit(f"😔 __**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Fғᴍᴘᴇɢ Cᴏᴅᴇ**__")


@Client.on_message((filters.group | filters.private) & filters.command(['del_ffmpeg', 'delffmpeg']))
async def del_ffmpeg(client, message):

    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return

    SnowDev = await message.reply_text(text="**Please Wait...**", reply_to_message_id=message.id)
    await db.set_ffmpegcode(message.from_user.id, None)
    await SnowDev.edit("❌ __**Fғᴍᴘᴇɢ Cᴏᴅᴇ Dᴇʟᴇᴛᴇᴅ**__")


@Client.on_message((filters.group | filters.private) & filters.command('set_metadata'))
async def set_metadata(client, message):
    
    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return
    
    try:
        metadata = await client.ask(text=Txt.SEND_METADATA, chat_id=message.chat.id, user_id=message.from_user.id, filters=filters.text, timeout=30)

    except TimeoutError:
        await message.reply_text("Error!!\n\nRequest timed out.\nRestart by using /set_ffmpeg", reply_to_message_id= metadata.id)
        return
    
    await db.set_metadata(message.from_user.id, metadata=metadata.text)
    await message.reply_text("✅ __**Mᴇᴛᴀᴅᴀᴛᴀ Cᴏᴅᴇ Sᴀᴠᴇᴅ**__", reply_to_message_id=message.id)
    
    
@Client.on_message((filters.group | filters.private) & filters.command('see_metadata'))
async def see_metadata(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return
    
    SnowDev = await message.reply_text(text="**Please Wait...**", reply_to_message_id=message.id)

    metadata = await db.get_metadata(message.from_user.id)
    
    if metadata:
        await SnowDev.edit(f"✅ <b>Yᴏᴜʀ Cᴜʀʀᴇɴᴛ Mᴇᴛᴀᴅᴀᴛᴀ Cᴏᴅᴇ ɪs :-</b>\n\n<code>{metadata}</code>")
    else:
        await SnowDev.edit(f"😔 __**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Mᴇᴛᴀᴅᴀᴛᴀ Cᴏᴅᴇ**__")


#Feature Added By https//t.me/The_TGguy
# Telegram Guy!!™
# for support @Itsme123i In Telegram

user_data = {}

# Position mappings (predefined positions in drawtext coordinates)
POSITION_MAP = {
    "top left": "x=10:y=10",
    "top center": "x=(w-tw)/2:y=10",
    "top right": "x=w-tw-10:y=10",
    "center left": "x=10:y=(h-th)/2",
    "center": "x=(w-tw)/2:y=(h-th)/2",
    "center right": "x=w-tw-10:y=(h-th)/2",
    "bottom left": "x=10:y=h-th-10",
    "bottom center": "x=(w-tw)/2:y=h-th-10",
    "bottom right": "x=w-tw-10:y=h-th-10"
}

# Inline keyboard for position selection
POSITION_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("Top Left", callback_data="pos:top left"),
     InlineKeyboardButton("Top Center", callback_data="pos:top center"),
     InlineKeyboardButton("Top Right", callback_data="pos:top right")],
    [InlineKeyboardButton("Center Left", callback_data="pos:center left"),
     InlineKeyboardButton("Center", callback_data="pos:center"),
     InlineKeyboardButton("Center Right", callback_data="pos:center right")],
    [InlineKeyboardButton("Bottom Left", callback_data="pos:bottom left"),
     InlineKeyboardButton("Bottom Center", callback_data="pos:bottom center"),
     InlineKeyboardButton("Bottom Right", callback_data="pos:bottom right")],
    [InlineKeyboardButton("Custom Position", callback_data="pos:custom")]
])

@Client.on_message((filters.group | filters.private) & filters.command('set_wm'))
async def set_wm(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return

    # Initialize user data
    user_data[message.from_user.id] = {}
    
    # Ask for watermark text
    await message.reply_text("Send me the text for the watermark (e.g., 'Waves')", reply_to_message_id=message.id)

@Client.on_message((filters.group | filters.private) & ~filters.command())
async def handle_wm_steps(client, message):
    user_id = message.from_user.id
    if user_id not in user_data:
        return  # Ignore if user hasn't started the process

    data = user_data[user_id]
    
    # Step 1: Capture watermark text
    if "text" not in data:
        data["text"] = message.text
        await message.delete()  # Delete user's input
        await message.reply_text(
            "Choose the position for the text:",
            reply_markup=POSITION_KEYBOARD
        )
    
    # Step 3: Custom position input
    elif "waiting_for_custom" in data:
        try:
            x, y = map(int, message.text.split())
            data["position"] = f"x={x}:y={y}"
            del data["waiting_for_custom"]
            await message.delete()
            await message.reply_text("Now send me the opacity to use in the video (e.g., 100, 70, 60, etc.)")
        except:
            await message.reply_text("Invalid format! Please send like: [10] [10]")
    
    # Step 4: Capture opacity
    elif "opacity" not in data:
        try:
            opacity = int(message.text)
            if 0 <= opacity <= 100:
                data["opacity"] = opacity / 100  # Convert to 0.0-1.0 range for drawtext
                await message.delete()
                await message.reply_text("Now send me the color for the text (e.g., white, red, blue)")
            else:
                await message.reply_text("Opacity must be between 0 and 100!")
        except:
            await message.reply_text("Please send a valid number (e.g., 100, 70)")

    # Step 5: Capture color
    elif "color" not in data:
        data["color"] = message.text.lower()
        await message.delete()
        await message.reply_text("Now send me the font size (e.g., 24, 36)")
    
    # Step 6: Capture font size and finalize
    elif "font_size" not in data:
        try:
            font_size = int(message.text)
            data["font_size"] = font_size
            await message.delete()
            
            # Construct the drawtext filter
            wm_code = (
                f'-vf "drawtext=text=\'{data["text"]}\':'
                f'fontcolor={data["color"]}:'
                f'fontsize={data["font_size"]}:'
                f'{data["position"]}:'
                f'alpha={data["opacity"]}"'
            )
            
            # Save to database
            await db.set_watermark(user_id, watermark=wm_code)
            
            # Clean up and notify user
            del user_data[user_id]
            await message.reply_text("✅ __**Watermark Code Saved**__")
        except:
            await message.reply_text("Please send a valid number (e.g., 24, 36)")

@Client.on_callback_query(filters.regex(r"^pos:"))
async def handle_position_selection(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in user_data:
        return

    pos_choice = callback_query.data.split(":")[1]
    
    if pos_choice == "custom":
        user_data[user_id]["waiting_for_custom"] = True
        await callback_query.message.edit_text("Send me the position, e.g., [10] [10]")
    else:
        user_data[user_id]["position"] = POSITION_MAP[pos_choice]
        await callback_query.message.edit_text("Now send me the opacity to use in the video (e.g., 100, 70, 60, etc.)")

# Existing view_wm and delete_wm remain unchanged
@Client.on_message((filters.group | filters.private) & filters.command('view_wm'))
async def view_wm(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return

    SnowDev = await message.reply_text(text="**Please Wait...**", reply_to_message_id=message.id)
    wm_code = await db.get_watermark(message.from_user.id)

    if wm_code:
        await SnowDev.edit(f"✅ <b>Your Current Watermark Code is :-</b>\n\n<code>{wm_code}</code>")
    else:
        await SnowDev.edit(f"😔 __**You Don’t Have Any Watermark**__")

@Client.on_message((filters.group | filters.private) & filters.command('delete_wm'))
async def delete_wm(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return

    SnowDev = await message.reply_text(text="**Please Wait...**", reply_to_message_id=message.id)
    await db.set_watermark(message.from_user.id, watermark=None)
    await SnowDev.edit("❌ __**Watermark Deleted**__")
