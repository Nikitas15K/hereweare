from typing import Optional, List
from app.db.repositories.base import BaseRepository

GET_ALL_USERS_QUERY = """
    SELECT id, username, email, email_verified, is_active, is_superuser, created_at, updated_at
    FROM users;
"""

SEARCH_USERS = """
    SELECT id, username, email, email_verified, is_active, is_superuser, created_at, updated_at
    FROM users WHERE username like :username ; 
"""



class AdminRepository(BaseRepository):

    async def get_all_users(self) -> List:
        user_records = await self.db.fetch_all(query=GET_ALL_USERS_QUERY)
        return user_records

    async def get_search(self, username: str) -> List:
        username = username.replace('\\','\\\\').replace('%','\\%').replace('_', '\\_')
        user_records = await self.db.fetch_all(query=SEARCH_USERS,values={"username": '%{}%'.format(username)})
        return user_records  