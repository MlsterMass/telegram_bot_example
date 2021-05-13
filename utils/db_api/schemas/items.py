from sqlalchemy import Column, String, sql, Integer, Sequence

from utils.db_api.db_gino import TimedBasedModel


class Item(TimedBasedModel):
    __tablename__ = "items"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(50))
    photo = Column(String(250))
    price = Column(Integer)

    query: sql.Select
