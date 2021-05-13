from sqlalchemy import Column, String, BigInteger, sql, Integer, Sequence

from utils.db_api.db_gino import TimedBasedModel


class User(TimedBasedModel):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(BigInteger)
    language = Column(String(2))
    full_name = Column(String(100))
    username = Column(String(50))
    referral = Column(Integer)
    email = Column(String(100))

    query: sql.Select
