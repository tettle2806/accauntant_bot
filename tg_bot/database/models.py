from sqlalchemy import BigInteger, String, DateTime, Integer, func

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class User(Base):
    __tablename__ = 'users'
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[BigInteger] = mapped_column(BigInteger, unique=True, primary_key=True)
    name: Mapped[String] = mapped_column(String)
    phone_number: Mapped[String] = mapped_column(String, unique=True)
    expenses: Mapped[BigInteger] = mapped_column(BigInteger, default=0)
    income: Mapped[BigInteger] = mapped_column(BigInteger, default=0)
    balance: Mapped[BigInteger] = mapped_column(BigInteger, default=0)
    transactions: Mapped[Integer] = mapped_column(Integer, default=0)
    family_id: Mapped[Integer] = mapped_column(Integer, nullable=True, default=None)


class Family(Base):
    __tablename__ = 'families'
    family_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    family_name: Mapped[String] = mapped_column(String)
    family_password: Mapped[String] = mapped_column(String)
    expenses: Mapped[BigInteger] = mapped_column(BigInteger, default=0)
    income: Mapped[BigInteger] = mapped_column(BigInteger, default=0)
    balance: Mapped[BigInteger] = mapped_column(BigInteger, default=0)


class TransactionUser(Base):
    __tablename__ = 'transaction_users'
    transaction_id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Integer] = mapped_column(Integer)
    type_transactions: Mapped[String] = mapped_column(String)  # income / expenses
    quantity: Mapped[Integer] = mapped_column(Integer)
    description: Mapped[String] = mapped_column(String)
    user_name: Mapped[String] = mapped_column(String)


class TransactionFamily(Base):
    __tablename__ = 'transaction_families'
    transaction_id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Integer] = mapped_column(Integer)
    type_transactions: Mapped[String] = mapped_column(String)  # income / expenses
    quantity: Mapped[Integer] = mapped_column(Integer)
    description: Mapped[String] = mapped_column(String)
    family_id: Mapped[Integer] = mapped_column(Integer)


