from sqlalchemy import select, delete, update
from tg_bot.database.db_helper import db_helper
from tg_bot.database.models import User, Family, TransactionFamily
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
        try:
            for user in users:
                name = user.name
                phone = str(user.phone_number)
                expenses = user.expenses
                income = user.income
                balance = user.balance
                family_id = user.family_id
                created_at = str(user.created_at)

            user_info.append([name, phone, expenses, income, balance, family_id, created_at])
            print(user_info)
            return user_info
        except:
            return None

async def update_user(telegram_id: int, family_id:int):
    async with db_helper.session_factory() as session:
        stmt = update(User).where(User.telegram_id == telegram_id).values(family_id=family_id)
        await session.execute(stmt)
        await session.commit()

async def delete_user():
    async with db_helper.session_factory() as session:
        stmt = delete(User).where(User.telegram_id == 660515831)
        user = await session.execute(stmt)
        return user


async def insert_family(family_name, family_password):
    async with db_helper.session_factory() as session:
        family = Family(
            family_name=family_name,
            family_password=family_password,
        )
        session.add(family)
        await session.commit()
        print(family)
        return family




async def get_family(family_name: str):
    async with db_helper.session_factory() as session:
        stmt = select(Family).where(Family.family_name == family_name)
        result = await session.scalars(stmt)
        family_info = []
        try:
            for row in result:
                family_id = row.family_id
                family_name = row.family_name
                family_pass = row.family_password
                family_balance = row.balance
                family_income = row.income
                family_expenses = row.expenses

            family_info.append([family_id, family_name, family_pass, family_balance, family_income, family_expenses])
            return family_info
        except:
            return None


async def family_transactions():
    async with db_helper.session_factory() as session:
        transaction = TransactionFamily(

        )





        # user = User(
        #     telegram_id=telegram_id,
        #     phone_number=phone,
        #     name=name
        # )
        # session.add(user)
        # await session.commit()
        # return user


if __name__ == '__main__':
    # asyncio.run(insert_family('RASULOV', 'PASSWORD'))
    # asyncio.run(get_family('RASULOV'))
    asyncio.run(update_user(660515831, None))