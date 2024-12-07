# db/init_db.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import UserDb




async def get_user_db(db: AsyncSession, username: str) -> UserDb:
    """Get user by username using SQLAlchemy async ORM"""
    try:
        query = select(UserDb).where(UserDb.username == username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        return user
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

async def create_user(db: AsyncSession, user: UserDb):
    """Create a new user using SQLAlchemy async ORM"""
    try:
        db.add(user)
        await db.commit()
        return user
    except Exception as e:
        await db.rollback()
        print(f"Error creating user: {e}")
        return None