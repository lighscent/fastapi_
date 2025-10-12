from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/book/{book_id}", response_class=HTMLResponse)
async def read_book(book_id: int, request: Request, book: str = "default"):
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "book": book, 
            "id": book_id
        }
    )
