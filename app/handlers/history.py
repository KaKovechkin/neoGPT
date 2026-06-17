from aiogram.filters import Command, callback_data
from aiogram.types import Message, CallbackQuery
from aiogram import Router, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.db import get_connection, get_list_usernames, get_update_message
from app.callbacks import UserID

router = Router()


@router.message(Command('history'))
async def cmd_history(message:Message):
    owner_id = message.from_user.id 
    connection = await get_connection(owner_id)
    if connection is None:
        await message.answer('У вас нет активного бизнес-соеденения.')
    else:
        users = await get_list_usernames(connection[0])
        builder = InlineKeyboardBuilder()
        for user in users:
            username, user_id, first_name = user
            name = f'@{username}' if username else f'{first_name} {user_id}'
            builder.button(
            text=f'{name}',
            callback_data=UserID(user_id=user_id).pack()
)
        builder.adjust(1)
        markup = builder.as_markup()
        await message.answer(text = "Выберете пользователя:" , reply_markup=markup)
        

@router.callback_query(UserID.filter())
async def on_user_selected(callback: CallbackQuery, callback_data: UserID, bot:Bot):
    user_id = callback_data.user_id
    owner_id = callback.from_user.id
    business_connection_id = await get_connection(owner_id=owner_id)
    business_connection_id = business_connection_id[0]
    messages = await get_update_message(business_connection_id=business_connection_id, from_user_id=user_id)
    if not messages:
        print(messages, 'Eror')
        await callback.answer('Нет сообщений от пользователя.')
    else:
        await callback.message.answer(text=f'Сообщения от пользователя:')
        for message in messages:
            type_message = message[5]
            file_id = message[4]
            type_message_update = "Изменено" if message[1] == 1 and message[2] == 0 else "Удалено"  if message[1] == 0 and message[2] == 1 else "Изменено и удалено."
            print(type_message_update, message)
            if type_message == 'text':
                await callback.message.answer(f'дата: {message[3]}. Текст:{message[0]}. Тип {type_message_update}.')
            elif type_message == 'photo':
                await bot.send_photo(chat_id=owner_id, photo=file_id, caption=f'Дата: {message[3]}. Тип: {type_message_update}.')
            elif type_message == 'video':
                await bot.send_video(owner_id, file_id, caption=f'Дата: {message[3]}. Тип: {type_message_update}.')
            elif type_message == 'sticker':
                await bot.send_sticker(owner_id, file_id)
                await bot.send_message(owner_id, text = f'Дата: {message[3]}. Тип: {type_message_update}.')
            elif type_message == 'video_note':
                await bot.send_video_note(owner_id, file_id)
                await bot.send_message(owner_id, text=f'Дата: {message[3]}. Тип: {type_message_update}.')
            elif type_message == 'voice':
                await bot.send_voice(owner_id, file_id)
                await bot.send_message(owner_id, text=f'Дата: {message[3]}. Тип: {type_message_update}.')
            elif type_message == 'document':
                await bot.send_document(owner_id, file_id, caption=f'Дата: {message[3]}. Тип: {type_message_update}.')
            else:
                print(type_message)
                await bot.send_message(owner_id, text='Неизвестное сообщение.')
            
    
    
    
            