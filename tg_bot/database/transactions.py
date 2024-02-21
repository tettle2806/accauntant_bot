from sqlalchemy import select, delete, update
from tg_bot.database.db_helper import db_helper
from tg_bot.database.models import User
import asyncio


async def create_user(telegram_id: int, phone: str, name: str) -> User:
    async with db_helper.session_factory() as session:
        user = User(
            telegram_id=telegram_id,
            phone_number=phone,
            name=name
        )
        session.add(user)
        await session.commit()
        return user


async def select_telegram_id_by_phone(phone: str):
    async with db_helper.session_factory() as session:
        stmt = select(User.telegram_id).where(User.phone_number == phone)
        telegram_id = await session.scalar(stmt)
        print(telegram_id)
        return telegram_id


async def select_user(telegram_id: int):
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        users = await session.scalars(stmt)
        user_info = []
        for user in users:
            name = user.name
            phone = str(user.phone_number)
            expenses = user.expenses
            income = user.income
            balance = user.balance
            family_id = user.family_id
            created_at = str(user.created_at)
        user_info.append([name, phone, expenses, income, balance, family_id, created_at])
        return user_info




async def delete_user():
    async with db_helper.session_factory() as session:
        stmt = delete(User).where(User.telegram_id == 660515831)
        user = await session.execute(stmt)
        return user


if __name__ == '__main__':
    asyncio.run(select_user(660515831))
