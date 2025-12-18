import asyncio
import logging
from app.core.database import AsyncSessionLocal
from app.modules.users.seeds import seed_users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting database seeding...")
    
    async with AsyncSessionLocal() as session:
        try:
            await seed_users(session)
            
            # Add other module seeds here
            
            await session.commit()
            logger.info("Database seeding completed successfully.")
        except Exception as e:
            logger.error(f"Seeding failed: {e}")
            await session.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(main())
