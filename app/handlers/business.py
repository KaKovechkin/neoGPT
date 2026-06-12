from aiogram.types import Message, BusinessMessagesDeleted
from aiogram import Router, Bot


from app.database.db import save_message, message_update, mark_deleted, get_message


router = Router()


@router.business_message()
async def handle_business_message(message:Message):
    chat_id = message.chat.id
    business_connection_id = message.business_connection_id
    message_id = message.message_id
    from_user_id = message.from_user.id
    text = message.text
    date = message.date
    await save_message(chat_id, business_connection_id, message_id, from_user_id, text, date)
    
    
@router.edited_business_message()
async def handle_business_message_update(message:Message):
    await message_update(text = message.text , chat_id= message.chat.id , message_id= message.message_id)
    
    
@router.deleted_business_messages()
async def handle_deleted(event: BusinessMessagesDeleted, bot: Bot):
    connection = await bot.get_business_connection(event.business_connection_id)
    owner_id = connection.user.id
    for id in event.message_ids:
        await mark_deleted(message_id=id , chat_id=event.chat.id)
        row= await get_message(event.chat.id ,id)
        await bot.send_message(chat_id=owner_id, text = row[0])
   
    
    