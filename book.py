from database import Base
from sqlalchemy import String,Boolean,Integer,Column

class Book(Base):
    __tablename__="books"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    author = Column(String(170), nullable=False)
    publication_year = Column(String(100))
    acquired = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Book name={self.title} author={self.author}>"