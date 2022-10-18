from pyrogram import filters
from aiohttp import ClientSession
from pyrogram import Client as bot
from plugins.function import make_carbon
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
aiohttpsession = ClientSession()

C = "Successfully Created Your Carbon"
F = InlineKeyboardMarkup(
[[
     InlineKeyboardButton("ʜᴏᴍʙᴀʟᴇ ᴄɪɴᴇᴍᴀs", url="https://t.me/HombaleCinemas")
]]
)




@bot.on_message(filters.command("carbon"))
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "reply to a text message to make carbon."
        )
    if not message.reply_to_message.text:
        return await message.reply_text(
            "reply to a text message to make carbon."
        )
    user_id = message.from_user.id
    m = await message.reply_text("processing...")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("uploading..")
    await message.reply_photo(
        photo=carbon,
        caption=C,
        reply_markup=F)
    await m.delete()
    carbon.close()
