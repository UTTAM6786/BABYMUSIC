from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.types import Message
from strings import get_string, helpers
from PURVIMUSIC import app
from pyrogram.types import InputMediaVideo
from PURVIMUSIC.misc import SUDOERS
from PURVIMUSIC.utils.database import add_sudo, remove_sudo
from PURVIMUSIC.utils.decorators.language import language
from PURVIMUSIC.utils.extraction import extract_user
from PURVIMUSIC.utils.inline import close_markup
from config import BANNED_USERS, OWNER_ID



@app.on_message(filters.command(["addsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id in SUDOERS:
        return await message.reply_text(_["sudo_1"].format(user.mention))
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(_["sudo_2"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])


@app.on_message(filters.command(["delsudo", "rmsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id not in SUDOERS:
        return await message.reply_text(_["sudo_3"].format(user.mention))
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(_["sudo_4"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])



@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & ~BANNED_USERS)
async def sudoers_list(client, message: Message):
    keyboard = [[InlineKeyboardButton("๏ ᴠɪᴇᴡ sᴜᴅᴏʟɪsᴛ ๏", callback_data="check_sudo_list")]]
    reply_markups = InlineKeyboardMarkup(keyboard)
  
    #await message.reply_photo(photo="https://telegra.ph/file/2fae241ce04a9009d4a0c.mp4", caption="**» ƈԋҽαƙ ʂυԃσ ʅιʂƚ Ⴆყ ɠιʋҽɳ Ⴆҽʅσɯ Ⴆυƚƚσɳ.**\n\n**» ɴᴏᴛᴇ:**  σɳʅყ ʂυԃσ υʂҽɾʂ ƈαɳ ʋιҽɯ. ", reply_markup=reply_markups)
    await message.reply_video(video="https://telegra.ph/file/2fae241ce04a9009d4a0c.mp4", caption="**» ƈԋҽαƙ ʂυԃσ ʅιʂƚ Ⴆყ ɠιʋҽɳ Ⴆҽʅσɯ Ⴆυƚƚσɳ.**\n\n**» ɴᴏᴛᴇ:**  σɳʅყ ʂυԃσ υʂҽɾʂ ƈαɳ ʋιҽɯ. ", reply_markup=reply_markups)
    

@app.on_callback_query(filters.regex("^check_sudo_list$"))
async def check_sudo_list(client, callback_query: CallbackQuery):
    keyboard = []
    if callback_query.from_user.id not in SUDOERS:
        return await callback_query.answer("𝐒𝐔𝐃𝐎 𝐋𝐈𝐒𝐓 𝐊 𝐁𝐀𝐃𝐋𝐄 𝐔𝐓𝐓𝐀𝐌 𝐊𝐄 𝐋𝐔𝐍𝐃 𝐋𝐄 𝐋𝐄🖕😎😂", show_alert=True)
    else:
        user = await app.get_users(OWNER_ID)

        user_mention = (user.first_name if not user.mention else user.mention)
        caption = f"**ʅιʂƚ σϝ ɱσԃҽɾαƚσɾ**\n\n**🌹σɯɳҽɾ** ➥ {user_mention}\n\n"

        keyboard.append([InlineKeyboardButton("๏ ʋιҽɯ σɯɳҽɾ ๏", url=f"tg://openmessage?user_id={OWNER_ID}")])
        
        count = 1
        for user_id in SUDOERS:
            if user_id != OWNER_ID:
                try:
                    user = await app.get_users(user_id)
                    user_mention = user.mention if user else f"**🎁 Sᴜᴅᴏ {count} ɪᴅ:** {user_id}"
                    caption += f"**🎁 ʂυԃσ** {count} **»** {user_mention}\n"
                    button_text = f"๏ ʋιҽɯ ʂυԃσ {count} ๏ "
                    keyboard.append([InlineKeyboardButton(button_text, url=f"tg://openmessage?user_id={user_id}")]
                    )
                    count += 1
                except:
                    continue

        # Add a "Back" button at the end
        keyboard.append([InlineKeyboardButton("๏ Ⴆαƈƙ ๏", callback_data="back_to_main_menu")])

        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            await callback_query.message.edit_caption(caption=caption, reply_markup=reply_markup)

@app.on_callback_query(filters.regex("^back_to_main_menu$"))
async def back_to_main_menu(client, callback_query: CallbackQuery):
    keyboard = [[InlineKeyboardButton("๏ ᴠɪᴇᴡ sᴜᴅᴏʟɪsᴛ ๏", callback_data="check_sudo_list")]]
    reply_markupes = InlineKeyboardMarkup(keyboard)
    await callback_query.message.edit_caption(caption="**» ƈԋҽαƙ ʂυԃσ ʅιʂƚ Ⴆყ ɠιʋҽɳ Ⴆҽʅσɯ Ⴆυƚƚσɳ.**\n\n**» ɴᴏᴛᴇ:**  σɳʅყ ʂυԃσ υʂҽɾʂ ƈαɳ ʋιҽɯ. ", reply_markup=reply_markupes)




@app.on_message(filters.command(["delallsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
@language
async def del_all_sudo(client, message: Message, _):
    count = len(SUDOERS) - 1  # Exclude the admin from the count
    for user_id in SUDOERS.copy():
        if user_id != OWNER_ID:
            removed = await remove_sudo(user_id)
            if removed:
                SUDOERS.remove(user_id)
                count -= 1
    await message.reply_text(f"Removed {count} users from the sudo list.")
