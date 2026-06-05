from aiogram.types import ReplyKeyboardMarkup , ReplyKeyboardRemove 
from aiogram.types import InlineKeyboardButton , InlineKeyboardMarkup , KeyboardButton


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Что умеет этот бот.'  , callback_data='none_b')]
])


back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Назад' , callback_data='back')]
])