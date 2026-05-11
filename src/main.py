import logging

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

uvlog = logging.getLogger("uvicorn")

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str | None = Field(default=None, index=True)

sqlite_file_name = "src/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_sqlite_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_sqlite_session)]

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="passw0rd")

templates = Jinja2Templates(directory="src/templates")

@app.get("/")
def index(request: Request):
    error_state = request.session.pop("error", None)
    return templates.TemplateResponse(request=request, name="index.html", context={"error": error_state})

@app.post("/login", status_code=201)
def login(request: Request, session: SessionDep, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    statement = select(User).where(User.username == f"{username}")
    user = session.exec(statement).first()
    uvlog.info(f"User data is: {user}")
    if not user:
        request.session["error"] = "Wrong username or password"
        return RedirectResponse("http://localhost:8001/", status_code=303)
    return templates.TemplateResponse(request=request, name="dashboard.html")


@app.get("/users")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}