from sqlalchemy import sql, Column, Sequence, Integer, String

from utils.db_api.db_gino import db


class Menu(db.Model):
    __tablename__ = "items_menu"
    query: sql.Select
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    category_code = Column(String(20))
    category_name = Column(String(50))

    subcategory_code = Column(String(20))
    subcategory_name = Column(String(50))

    name = Column(String(50))
    photo = Column(String(250))
    price = Column(Integer)

    def __repr__(self):
        return f"""
        Product {self.id} - {self.name}
        Price: {self.price}
        """
