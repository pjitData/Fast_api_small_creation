from fastapi import Body, FastAPI

app = FastAPI()

Books = [
    {'Name': 'Prasenjit', 'add': 'Belonia', 'Subject': 'Python'},
    {'Name': 'Rohan', 'add': 'Agartala', 'Subject': 'Math'},
    {'Name': 'Sonali', 'add': 'Sikkim', 'Subject': 'English'},
    {'Name': 'Jiban', 'add': 'Jolahat', 'Subject': 'Bengali'},
    {'Name': 'Kunal', 'add': 'Jolahat', 'Subject': 'Bengali'}
]


# show all the dict

@app.get("/books")
async def read_all_books():
    return Books


# show the perticular 'JSON' by typing 'Subject'

@app.get("/books/{Enter_subject}")
def find_by_subj(Enter_subject: str):
    for subject in Books:
        if subject.get('Subject').casefold() == Enter_subject.casefold():
            return subject


# show the perticular 'JSON' by typing 'add'
@app.get("/book/")
async def find_by_add(address: str):
    home_address = []
    for home in Books:
        if home.get('add').casefold() == address.casefold():
            home_address.append(home)
    return home_address


# show the perticular 'JSON' by typing two str
@app.get("/book/{Enter_name&_subj}")
async def find_by_name_and_sub(Name: str, Subject: str):
    name_and_subj = []
    for book in Books:
        if book.get('Name').casefold() == Name.casefold() and book.get('Subject').casefold() == Subject.casefold():
            name_and_subj.append(book)
    return name_and_subj


# by POST method we can new update in dict
@app.post("/book/create_book")
async def create_book(new_book=Body()):
    Books.append(new_book)


# by using PUT method we can update our main dict
@app.put("/book/update_book")
async def update_book(update_book=Body()):
    for i in range(len(Books)):
        if Books[i].get('Name').casefold() == update_book.get('Name').casefold():
            Books[i] = update_book


# delete method in dict
@app.delete("/book/delete_book/{book_title}")
async def delete_book(Book_Title: str):
    for i in range(len(Books)):
        if Books[i].get('Subject').casefold() == Book_Title.casefold():
            Books.pop(i)
            break
