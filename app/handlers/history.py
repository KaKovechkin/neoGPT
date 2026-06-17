from aiogram.filters import Command, callback_data
from aiogram.types import Message, CallbackQuery
from aiogram import Router
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
async def on_user_selected(callback: CallbackQuery, callback_data: UserID):
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
            type_message = "Изменено" if message[1] == 1 and message[2] == 0 else "Удалено"  if message[1] == 0 and message[2] == 1 else "Изменено и удалено."
            print(type_message, message)
            await callback.message.answer(f'дата: {message[3]}. Текст:{message[0]}. Тип {type_message}.')
            
    
    
    
            