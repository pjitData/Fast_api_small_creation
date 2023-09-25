from dataclasses import Field
from typing import Optional
from starlette import status

from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: float
    language :str

    def __init__(self, id, title, author, description, rating, language):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.language= language


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=25)
    rating: float = Field(gt=0, lt=7.3)
    language: str = Field(min_length=2)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'Written by',
                'description': 'short sample of body',
                'rating': 5,
                'language': 'abc'
            }
        }


Books = [
    Book(1, 'Python', 'SK Jha', 'Programing', 7, 'English'),
    Book(2, 'English', 'Parul Prakashini', 'language', 5, 'English'),
    Book(3, 'Math', 'S.Chand', 'Basic Alzebra', 4, 'Bengali'),
    Book(4, 'Computer', 'T.K.L Publisher', 'Basic Computer Knowledge', 6, 'English'),
    Book(5, 'Tripura GK', 'TPSCE', 'General Knowledge', 5, 'Bengali'),
    Book(6, 'Bengali', 'Vidyasagar', 'Gramer', 7, 'Bengali'),

]


@app.get("/books") #read all books
async def read_all_books():
    return Books

@app.get("/book/{book_id}") #read book by searching book_id
async def read_book_by_id(book_id:int = Path(gt=0,lt=5)):
    for book in Books:
        if book.id==book_id:
            return book

@app.get("/books/") #get book by typing rating only
async def read_book_by_rating(book_rating: int= Query(gt=0, lt=6)):
    bookk_to_return=[]
    for book in Books:
        if book.rating == book_rating:
            bookk_to_return.append(book)
    return bookk_to_return

@app.get("/book/language/") #read book by languase
async def read_book_by_language(language: str):
    book_to_return=[]
    for book in Books:
        if book.language==language:
            book_to_return.append(book)
    return book_to_return

@app.post("/create_book") #post new item in Books(automatic book_id generate)
async def create_book(Book_Request: BookRequest):
    new_book = Book(**Book_Request.model_dump())
    Books.append(generate_book_id(new_book))

def generate_book_id(book:Books): #Automatic book_id generate
    book.id=1 if len(Books)==0 else Books[-1].id + 1
    return book

@app.put("/books/update_book", status_code=status.HTTP_200_OK) #uodate book if not update it will show HTTP status
async def update_book(book: BookRequest):
    book_changed= False
    for i in range(len(Books)):
        if Books[i].id == book.id:
            Books[i] = book
    #return book
            book_changed= True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Error!')

@app.delete("/books/book_id") #delete Books from list by using book_id
async def delete_book(book_id: int):
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            break