# db/init_db.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User


async def init_default_user(db: AsyncSession) -> None:
    """Initialize database with default user if not exists"""
    try:
        # Check if default user exists
        query = select(User).where(User.username == fake_users_db["johndoe"]["username"])
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            # Create default user
            default_user = User(
                username='johndoe',
                full_name='John Doe',
                email='johndoe@example.com',
                hashed_password='$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
                disabled=False
            )
            
            db.add(default_user)
            await db.commit()
    except Exception as e:
        await db.rollback()
        print(f"Error creating default user: {e}")

async def get_user_db(db: AsyncSession, username: str) -> User:
    """Get user by username using SQLAlchemy async ORM"""
    try:
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        return user
    except Exception as e:
        print(f"Error getting user: {e}")
        return None