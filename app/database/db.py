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
    file_id TEXT,
    type_message TEXT,
    from_user_id INTEGER , 
    text TEXT , 
    date  INTEGER, 
    is_deleted INTEGER , 
    first_name TEXT, 
    username TEXT,
    is_edited INTEGER DEFAULT 0
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
        

async def save_message(chat_id, business_connection_id, message_id, file_id, type_message, from_user_id, text, date, first_name, username):
        await db_connection.execute(''' 
            INSERT INTO messages (chat_id, business_connection_id, message_id, file_id, type_message, from_user_id, text, date, first_name, username, is_deleted)
            VALUES(?, ?, ?, ?, ? , ?, ?, ?,?,?,?)             
                         
                         ''' , (chat_id, business_connection_id, message_id, file_id, type_message, from_user_id, text, date, first_name, username, 0))
        await db_connection.commit()
        
        
async def mark_deleted(message_id , chat_id):
        await db_connection.execute('''
            UPDATE messages SET is_deleted = 1 WHERE chat_id = ? AND message_id = ?
                         '''  , (chat_id , message_id))
        await db_connection.commit()
        
        
async def message_update(text , chat_id , message_id, is_edited):
        await db_connection.execute('''
           UPDATE messages SET text  = ?, is_edited = ?  WHERE chat_id = ?  AND message_id = ?      
                         ''' , (text, is_edited, chat_id , message_id))
        await db_connection.commit()
        
        
async def get_message(chat_id, message_id):
        cursor =  await db_connection.execute('''
            SELECT text , username, file_id, type_message FROM messages WHERE chat_id = ? AND message_id = ?
                         ''' , (chat_id , message_id))
        row = await cursor.fetchone()
        return row
    
    
async def get_list_usernames(business_connection_id):
        cursor =  await db_connection.execute('''
            SELECT DISTINCT username, from_user_id,first_name FROM messages WHERE  business_connection_id = ?
                         ''' , (business_connection_id,))
        row = await cursor.fetchall()
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


async def get_update_message(business_connection_id,from_user_id):
    cursor = await db_connection.execute('''
            SELECT text , is_edited , is_deleted, date, file_id, type_message FROM messages WHERE business_connection_id = ? AND from_user_id = ? AND (is_edited = 1 OR is_deleted = 1)                        
                                         ''' , (business_connection_id, from_user_id))
    row = await cursor.fetchall()
    return row