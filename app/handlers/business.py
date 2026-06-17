from aiogram.types import Message, BusinessMessagesDeleted
from aiogram import Router, Bot
from aiogram.exceptions import TelegramAPIError


from app.database.db import save_message, message_update, mark_deleted, get_message, save_connection


router = Router()


@router.business_message()
async def handle_business_message(message:Message):
    chat_id = message.chat.id
    business_connection_id = message.business_connection_id
    message_id = message.message_id
    from_user_id = message.from_user.id
    text = message.text or message.caption
    date = message.date
    first_name = message.from_user.first_name
    username = message.from_user.username
    if message.photo:
        type_message = 'photo'
        file_id = message.photo[-1].file_id
    elif message.video:
        type_message = 'video'
        file_id = message.video.file_id
    elif message.sticker:
        type_message = 'sticker'
        file_id = message.sticker.file_id
    elif message.video_note:
        type_message = 'video_note'
        file_id = message.video_note.file_id
    elif message.voice:
        type_message = 'voice'
        file_id = message.voice.file_id
    elif message.document:
        type_message = 'document'
        file_id = message.document.file_id
    elif message.text:
        type_message = 'text'
        file_id = None
    else:
        print(type(message))
        type_message = 'other_type'
        file_id = None
    await save_message(chat_id, business_connection_id, message_id,file_id, type_message, from_user_id, text, date, first_name, username)
    
    
@router.edited_business_message()
async def handle_business_message_update(message: Message, bot: Bot):
    owner_id = None
    try:
        connection = await bot.get_business_connection(message.business_connection_id)
        owner_id = connection.user.id
        await save_connection(owner_id, message.business_connection_id)
        old_message = await get_message(chat_id=message.chat.id, message_id=message.message_id)
        if old_message is None:
            await bot.send_message(chat_id=owner_id, text='Сообщение не найдено в базе')
            return
        type_message = old_message[3]
        file_id = old_message[2]
        username = old_message[1] or "Без username"
        edit_text = f'Пользователь @{username} изменил(а) сообщение.'
        if type_message == 'text':
            await bot.send_message(
                chat_id=owner_id,
                text=f'Пользователь @{username} изменил(а) сообщение с текстом: {old_message[0]}'
            )
        elif type_message == 'photo':
            await bot.send_photo(chat_id=owner_id, photo=file_id, caption=edit_text)
        elif type_message == 'video':
            await bot.send_video(chat_id=owner_id, video=file_id, caption=edit_text)
        elif type_message == 'sticker':
            await bot.send_sticker(chat_id=owner_id, sticker=file_id)
            await bot.send_message(chat_id=owner_id, text=edit_text)
        elif type_message == 'video_note':
            await bot.send_video_note(chat_id=owner_id, video_note=file_id)
            await bot.send_message(chat_id=owner_id, text=edit_text)
        elif type_message == 'voice':
            await bot.send_voice(chat_id=owner_id, voice=file_id)
            await bot.send_message(chat_id=owner_id, text=edit_text)
        elif type_message == 'document':
            await bot.send_document(chat_id=owner_id, document=file_id, caption=edit_text)
        else:
            print(f'Неизвестный тип сообщения: {type_message}')
            await bot.send_message(chat_id=owner_id, text='Неизвестный тип сообщения.')
        await message_update(
            message.text or message.caption,
            chat_id=message.chat.id,
            message_id=message.message_id,
            is_edited=1
        )
    except TelegramAPIError as e:
        print(f'Ошибка Telegram API: {e}')
        if owner_id:
            await bot.send_message(chat_id=owner_id, text=f'Ошибка при обработке сообщения: {e}')
    except Exception as e:
        print(f'Неизвестная ошибка: {e}')
        
        
@router.deleted_business_messages()
async def handle_deleted(event: BusinessMessagesDeleted, bot: Bot):
    try:
        connection = await bot.get_business_connection(event.business_connection_id)
        owner_id = connection.user.id
        await save_connection(owner_id, event.business_connection_id)
    except Exception as e:
        print(f'Ошибка: {e}')
        return
    for message_id in event.message_ids:
        await mark_deleted(message_id=message_id , chat_id=event.chat.id)
        row= await get_message(event.chat.id ,message_id)
        if row is None:
            print('row is None')
            continue
        type_message = row[3]
        file_id = row[2]
        if type_message == 'text':
            await bot.send_message(chat_id=owner_id, text = f'Пользователь @{row[1] or "Без username"} удалил(а) сообщение с текстом: {row[0]}')
        elif type_message == 'photo':
            await bot.send_photo(chat_id=owner_id, photo=file_id, caption=f'Пользователь @{row[1] or "Без username"} удалил(а) сообщение.')
        elif type_message == 'video':
            await bot.send_video(chat_id=owner_id, video=file_id, caption=f'Пользователь @{row[1] or "Без username"} удалил(а) сообщение.')
        elif type_message == 'sticker':
            await bot.send_sticker(chat_id=owner_id, sticker=file_id)
            await bot.send_message(chat_id=owner_id, text=f'Пользователь @{row[1] or "Без username"} удалил(а) сообщение.')
        elif type_message == 'video_note':
            await bot.send_video_note(chat_id=owner_id, video_note=file_id)
            await bot.send_message(chat_id=owner_id, text=f'Пользователь @{row[1] or "Без username"} удалил(а) сообщение.')
        elif type_message == 'voice':
            await bot.send_voice(chat_id=owner_id, voice=file_id)
            await bot.send_message(chat_id=owner_id, text=f'Пользователь @{row[1] or "Без username"} удалил(а) сообщение.')
        elif type_message == 'document':
            await bot.send_document(chat_id=owner_id, document=file_id, caption=f'Пользователь @{row[1] or "Без username"} удалил(а) сообщение.')
        else:
            print(f'Неизвестный тип сообщения: {type_message}')
            await bot.send_message(chat_id=owner_id, text='Неизвестный тип сообщения.')



   



    
    