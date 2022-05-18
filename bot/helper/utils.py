import os
from bot import data, download_dir, app
import asyncio
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified
from .ffmpeg_utils import encode, get_thumbnail, get_duration, get_width_height 

async def on_task_complete():
    del data[0]
    if len(data) > 0:
      await add_task(data[0])

async def add_task(message: Message):
    try:  
      msg = await message.reply_text("⬇️ **Downloading Video** ⬇️", quote=True)
      filepath = await message.download(file_name=download_dir)
      abc = await msg.edit(f"**Encoding The File**")
      reply_id = message.id
      og = await encode(filepath, abc)
      if og:
        await msg.edit("**⬆️ Starting To Upload**")
        thumb = await get_thumbnail(og)
        width, height = await get_width_height(filepath)
        duration2 = await get_duration(og)
        await msg.edit("**⬆️ Uploading Video ⬆️**")
        await app.send_video(video=og, chat_id=message.chat.id, supports_streaming=True, file_name=og, thumb=thumb, duration=duration2, width=width, height=height, caption=og, reply_to_message_id=reply_id)
        os.remove(filepath)
        os.remove(thumb)
        await msg.edit("**File Encoded**")
        await msg.delete()
      else:
        await msg.edit("**Error Contact @NIRUSAKIMARVALE**")
        os.remove(filepath)
        os.remove(og)
    except MessageNotModified:
      pass
    except Exception as e:
      await msg.edit(f"```{e}```")
    await on_task_complete()
