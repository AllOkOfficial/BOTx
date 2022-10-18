import asyncio
import ast
from asyncio.log import logger
import re

from os import environ
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

def redirected_env(value):
    value = str(value)
    if value.lower() in ['chat', 'group', 'channel', 'supergroup', 'true']:
        return 'Chat'
    elif value.lower() in ['user', '0', 'pm', 'personal', 'bot', 'bot pm', 'false']:
        return 'PM'
    else:
        return 'Chat'

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))
PICS = (environ.get('PICS', 'https://telegra.ph/file/47ec05e89d83789067f66.jpg https://telegra.ph/file/470687bf8a302c64e75c1.jpg https://telegra.ph/file/78f2e55cb4cff909cfe40.jpg https://telegra.ph/file/a176b5927783e6603a5bb.jpg https://telegra.ph/file/c699a79616886d90c2a01.jpg https://telegra.ph/file/3f4c0d562aa66a9856c6b.jpg https://telegra.ph/file/918ab60116c57c11ffec8.jpg https://telegra.ph/file/90ab448fbb72d99d93bf6.jpg https://telegra.ph/file/4974a6c5c63bcc371a086.jpg https://telegra.ph/file/f35f36aa266acd1d0c5d2.jpg https://telegra.ph/file/e92f87cd1fc2fd828028f.jpg https://telegra.ph/file/d7e6dd46dfc6fb8e9f62c.jpg https://telegra.ph/file/a6ff7413ee1ea06257084.jpg https://telegra.ph/file/59044a16947232e39a876.jpg https://telegra.ph/file/e88d4a781e23a7efea9cd.jpg https://telegra.ph/file/f613c75db7d77b1a31d50.jpg')).split()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '1906155412').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Rajappan")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# Others
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'HombaleCinemas')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "False")), False)
IMDB = is_enabled((environ.get('IMDB', "True")), True)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "📝 File Name : <code>[HombaleCinemas] {file_name}</code>\n🧲 File Size :<i>{file_size}</i>, InlineKeyboardButton('➕️ 𝖠𝖽𝖽 𝖬𝖾 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 ➕️', url =f'http://t.me/TeleMoviesRobot?startgroup=true')")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>IMDb Data:\n\n🏷</b><b>Title:</b> <a href={url}>{title}</a>\n<code>{aka}</code>\n📆 <b>Year:</b> <a href={url}/releaseinfo>{year}</a>\n🌟 <b>Rating:</b> <a href={url}/ratings>{rating}</a> / 10\n\n🎭 <b>Genres : {genres}</b>\n\n📑 <b>Story Line :</b><code>{plot}</code>\n\n<b>Directors:{Directors}</b>\n<b>Writers :{Writers}</b>\n\n<b>JOIN & SUPPORT | {message.chat.title}</b>")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)

DELETE_TIME = int(environ.get('DELETE_TIME', 300))
START_IMAGE_URL = environ.get('START_IMAGE_URL', "")
UNAUTHORIZED_CALLBACK_TEXT = (environ.get('UNAUTHORIZED_CALLBACK_TEXT', "𝙏𝙃𝙄𝙎 𝙄𝙎 𝙉𝙊𝙏 𝙂𝙐𝘿 𝘿𝙐𝘿𝙀"))[:200]
REDIRECT_TO = (environ.get('REDIRECT_TO', 'true'))

LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your current IMDB template is {IMDB_TEMPLATE}"
