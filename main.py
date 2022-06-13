import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import Optional, List, Union
from database import SessionLocal
import book
from database import Base, engine
import requests

Base.metadata.create_all(engine)

app = FastAPI()

class Book(BaseModel):
    ID: Union[int, None] = None
    title: str
    author: str
    publication_year: str
    acquired: bool

    class Config:
        orm_mode = True

class BookUpdate(BaseModel):
    ID: Optional[int]
    title: Optional[str]
    author: Optional[str]
    publication_year: Optional[str]
    acquired: Optional[bool]


db = SessionLocal()

@app.get("/api_spec", response_class=PlainTextResponse)
def version():
    output = '{ \n "info": {\n "version": "2022.05.16"\n }\n }'
    return output

@app.get("/books", response_model=List[Book])
def get_all_books():
    books = db.query(book.Book).all()
    return books

@app.get("/books_by")
def get_book_by(author_name: str, from_y: int, to_y: int, acquired_book: bool):
    for x in db.query(book.Book).all():
        lista = x.publication_year.split("-")
        year = int(lista[0])
        if author_name in x.author and (from_y <= year <= to_y) and x.acquired == acquired_book:
            return x
    raise HTTPException(
        status_code=404,
        detail=f"There is no such book"
    )


@app.get("/books/{book_id}", response_model=Book)
def get_one_book(book_id: int):
    for x in db.query(book.Book).all():
        if x.ID == book_id:
            return x
    raise HTTPException(
        status_code=404,
        detail=f"There is no such book in database"
    )

@app.post("/add-book")
def add_book(book1: Book):
    new_book = book.Book(
        title=book1.title,
        author=book1.author,
        publication_year=book1.publication_year,
        acquired=book1.acquired
    )

    db.add(new_book)
    db.commit()
    return new_book

@app.patch("/update-book/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: BookUpdate):
    for x in db.query(book.Book).all():
        if x.ID == book_id:
            if book_update.title is not None:
                x.title = book_update.title
            if book_update.author is not None:
                x.author = book_update.author
            if book_update.publication_year is not None:
                x.publication_year = book_update.publication_year
            if book_update.acquired is not None:
                x.acquired = book_update.acquired
            return
    raise HTTPException(
        status_code=404,
        detail=f"Book not found"
    )

@app.delete("/delete-book/{book_id}", response_model=Book)
def delete_book(book_id: int):
    book_delete = db.query(book.Book).filter(book.Book.ID == book_id).first()
    if book_delete is None:
        raise HTTPException(
            status_code=404,
            detail=f"This book does not exist"
        )
    db.delete(book_delete)
    db.commit()

    return book_delete

@app.post("/import")
def import_books(author_n: str):
    response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{author_n}&key=AIzaSyDxFmU7kG_TuiFfHbAZ6-XjIykmaKW6YhY')
    response = response.json()
    response = response["items"]
    tytuly = []
    autor = []
    data = []
    acquired = []
    count = 0
    for x in range(len(response)):
        tytuly.append(response[x]["volumeInfo"]["title"])
        y = json.dumps(response[x]["volumeInfo"]["authors"])
        autor.append(y)
        data.append(response[x]["volumeInfo"]["publishedDate"])
        acquired.append(response[x]["accessInfo"]["epub"]["isAvailable"])
        new_book = book.Book(
            title=tytuly[x],
            author=autor[x],
            publication_year=data[x],
            acquired=acquired[x]
        )

        try:
            db.add(new_book)
            db.commit()
        except:
            db.rollback()
            raise
        count += 1
    return {"Imported": f"{count}"}