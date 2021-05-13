from sqlalchemy import Column, String, BigInteger, sql, Integer, Sequence, TIMESTAMP, JSON, Boolean

from utils.db_api.db_gino import TimedBasedModel


class Purchase(TimedBasedModel):
    __tablename__ = "purchases"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    buyer = Column(BigInteger)
    item_id = Column(Integer)
    amount = Column(Integer)
    quantity = Column(Integer)
    purchases = Column(TIMESTAMP)
    shipping_address = Column(JSON)
    phone_number = Column(String(50))
    email = Column(String(200))
    receiver = Column(String(100))
    succefull = Column(Boolean, default=False)
    query: sql.Select
