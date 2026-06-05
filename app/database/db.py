import aiosqlite


async def init_db():
    async with aiosqlite.connect("messages.db") as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER  ,
    business_connection_id TEXT , 
    message_id  INTEGER ,
    from_user_id INTEGER , 
    text TEXT , 
    date  INTEGER, 
    is_deleted INTEGER 
    )""")
        await db.commit()
        

async def save_message(chat_id ,business_connection_id, message_id, from_user_id, text, date ):
    async with aiosqlite.connect('messages.db') as db:
        await db.execute(''' 
            INSERT INTO messages (chat_id, business_connection_id, message_id, from_user_id, text, date)
            VALUES(?, ?, ?, ?, ? , ?)             
                         
                         ''' , (chat_id ,business_connection_id, message_id, from_user_id, text, date ))
        await db.commit()
        
        
async def mark_deleted(message_id , chat_id):
    async with aiosqlite.connect('messages.db') as db:
        await db.execute('''
            UPDATE messages SET is_deleted = 1 WHERE chat_id = ? AND message_id = ?
                         '''  , (chat_id , message_id))
        await db.commit()