import aiosqlite


db_connection = None 


async def init_db():
    global db_connection
    db_connection = await aiosqlite.connect('messages.db')
    await db_connection.execute("""CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER  ,
    business_connection_id TEXT , 
    message_id  INTEGER ,
    from_user_id INTEGER , 
    text TEXT , 
    date  INTEGER, 
    is_deleted INTEGER , 
    first_name TEXT, 
    username TEXT
    )""")
    await db_connection.execute("""CREATE TABLE IF NOT EXISTS connections (
        owner_id TEXT,
        business_connection_id TEXT, 
        UNIQUE(owner_id)
        )""")
    await db_connection.commit()
        
        
async def close_db():
    global db_connection
    await db_connection.close()
        

async def save_message(chat_id ,business_connection_id, message_id, from_user_id, text, date, first_name, username):
        await db_connection.execute(''' 
            INSERT INTO messages (chat_id, business_connection_id, message_id, from_user_id, text, date, first_name, username)
            VALUES(?, ?, ?, ?, ? , ?, ?, ?)             
                         
                         ''' , (chat_id ,business_connection_id, message_id, from_user_id, text, date, first_name, username))
        await db_connection.commit()
        
        
async def mark_deleted(message_id , chat_id):
        await db_connection.execute('''
            UPDATE messages SET is_deleted = 1 WHERE chat_id = ? AND message_id = ?
                         '''  , (chat_id , message_id))
        await db_connection.commit()
        
        
async def message_update(text , chat_id , message_id):
        await db_connection.execute('''
           UPDATE messages SET text  = ? WHERE chat_id = ?  AND message_id = ?      
                         ''' , (text , chat_id , message_id ))
        await db_connection.commit()
        
        
async def get_message(chat_id, message_id):
        cursor =  await db_connection.execute('''
            SELECT text , username FROM messages WHERE chat_id = ? AND message_id = ?
                         ''' , (chat_id , message_id))
        row = await cursor.fetchone()
        return row
            
                     
async def save_connection(owner_id, business_connection_id):
    await db_connection.execute("""
            INSERT OR IGNORE INTO connections (owner_id, business_connection_id)
            VALUES(?,?)
                                """ , (owner_id , business_connection_id))
    await db_connection.commit()
    
    
async def get_connection(owner_id):
    cursor = await db_connection.execute('''
            SELECT business_connection_id FROM connections WHERE owner_id = ?
                                ''' , (owner_id,))
    row = await cursor.fetchone()
    return row 