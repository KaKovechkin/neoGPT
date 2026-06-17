from aiogram.filters.callback_data import CallbackData


class UserID(CallbackData, prefix = 'user'):
    user_id: int
    
    
