from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper.database import db
from helper.utils import CANT_CONFIG_GROUP_MSG
from script import Txt
from asyncio.exceptions import TimeoutError


# Timeout durations
TEXT_TIMEOUT = 30
OTHER_TIMEOUT = 60

# Predefined positions with their respective x and y values
positions_map = {
    "top_left": {"x": "10", "y": "10"},
    "top_center": {"x": "(w-text_w)/2", "y": "10"},
    "top_right": {"x": "w-text_w-10", "y": "10"},
    "center_left": {"x": "10", "y": "(h-text_h)/2"},
    "center": {"x": "(w-text_w)/2", "y": "(h-text_h)/2"},
    "center_right": {"x": "w-text_w-10", "y": "(h-text_h)/2"},
    "bottom_left": {"x": "10", "y": "h-text_h-10"},
    "bottom_center": {"x": "(w-text_w)/2", "y": "h-text_h-10"},
    "bottom_right": {"x": "w-text_w-10", "y": "h-text_h-10"}
}

# Position buttons
position_buttons = [
    ["top_left", "top_center", "top_right"],
    ["center_left", "center", "center_right"],
    ["bottom_left", "bottom_center", "bottom_right"],
    ["custom_position"]
]

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


def generate_position_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(pos.replace("_", " "), callback_data=f"position:{pos}") for pos in row]
        for row in position_buttons
    ])

async def ask_user(client, message, question, timeout=OTHER_TIMEOUT):
    try:
        sent_message = await message.reply_text(question)
        response = await client.listen(message.chat.id, timeout=timeout)
        return response.text
    except TimeoutError:
        await message.reply_text("⏳ Timeout reached! Process canceled.")
        return None

@Client.on_message((filters.group | filters.private) & filters.command('set_wm'))
async def set_wm(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return

    # Step 1: Ask for watermark text
    text = await ask_user(client, message, "Send me the text for the watermark", timeout=TEXT_TIMEOUT)
    if not text:
        return

    # Step 2: Ask for position
    await message.reply_text("Choose the position for the text", reply_markup=generate_position_markup())

    # Save user state for position selection
    client.user_state[message.chat.id] = {"text": text}

@Client.on_callback_query()
async def handle_position_callback(client, callback_query):
    if not callback_query.data.startswith("position:"):
        return

    position = callback_query.data.split(":", 1)[1]
    chat_id = callback_query.message.chat.id

    # Retrieve user state
    user_state = client.user_state.get(chat_id)
    if not user_state:
        await callback_query.message.edit_text("❌ Process not started. Use /set_wm to begin.")
        return

    if position == "custom_position":
        # Handle custom position input
        custom_position = await ask_user(client, callback_query.message, "Send me the position in the format: x y (e.g., 10 10)")
        if not custom_position or len(custom_position.split()) != 2 or not all(i.isdigit() for i in custom_position.split()):
            await callback_query.message.reply_text("❌ Invalid position! Please restart the process.")
            return
        x, y = custom_position.split()
    else:
        # Predefined position
        pos_values = positions_map.get(position)
        x, y = pos_values["x"], pos_values["y"]

    await callback_query.message.edit_text(f"✅ Position chosen: {position.replace('_', ' ')}")

    user_state["x"] = x
    user_state["y"] = y

    # Step 3: Ask for opacity
    opacity = await ask_user(client, callback_query.message, "Now send me the opacity to use in the video. Eg: 100, 70, 60... Etc.")
    if not opacity or not opacity.isdigit():
        await callback_query.message.reply_text("❌ Invalid opacity! Please restart the process.")
        return

    user_state["opacity"] = opacity

    # Step 4: Ask for color
    color = await ask_user(client, callback_query.message, "Send me the color for the text. Eg: white, black, red... Etc.")
    if not color:
        await callback_query.message.reply_text("❌ Invalid color! Please restart the process.")
        return

    user_state["color"] = color

    # Step 5: Ask for font size
    font_size = await ask_user(client, callback_query.message, "Send me the font size for the text. Eg: 24, 30... Etc.")
    if not font_size or not font_size.isdigit():
        await callback_query.message.reply_text("❌ Invalid font size! Please restart the process.")
        return

    user_state["font_size"] = font_size

    # Step 6: Generate drawtext command
    drawtext_command = f"drawtext=text='{user_state['text']}':fontcolor={user_state['color']}:fontsize={user_state['font_size']}:x={user_state['x']}:y={user_state['y']}:opacity={user_state['opacity']}"

    # Save to database
    await db.set_watermark(chat_id, watermark=drawtext_command)
    await callback_query.message.reply_text(f"✅ Watermark set successfully!\n\n<code>{drawtext_command}</code>")        


@Client.on_message((filters.group | filters.private) & filters.command('view_wm'))
async def view_wm(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return

    SnowDev = await message.reply_text(text="**Please Wait...**", reply_to_message_id=message.id)

    wm_code = await db.get_watermark(message.from_user.id)

    if wm_code:
        await SnowDev.edit(f"✅ <b>Yᴏᴜʀ Cᴜʀʀᴇɴᴛ Wᴀᴛᴇʀᴍᴀʀᴋ Cᴏᴅᴇ ɪs :-</b>\n\n<code>{wm_code}</code>")
    else:
        await SnowDev.edit(f"😔 __**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Wᴀᴛᴇʀᴍᴀʀᴋ**__")


@Client.on_message((filters.group | filters.private) & filters.command('delete_wm'))
async def delete_wm(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await CANT_CONFIG_GROUP_MSG(client, message)
        return

    SnowDev = await message.reply_text(text="**Please Wait...**", reply_to_message_id=message.id)
    await db.set_watermark(message.from_user.id, watermark=None)
    await SnowDev.edit("❌ __**Wᴀᴛᴇʀᴍᴀʀᴋ Dᴇʟᴇᴛᴇᴅ**__")
    
