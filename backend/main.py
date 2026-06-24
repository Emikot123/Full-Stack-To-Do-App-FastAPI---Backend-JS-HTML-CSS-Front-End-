from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, Base,Todo
from pydantic import BaseModel

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LoginSchema(BaseModel):
    email: str
    password: str

class UserSchema(BaseModel):
    email: str
    password: str

class ToDoSchema(BaseModel):
    title: str
    email: str
    password: str

class TaskDoneSchema(BaseModel):
    email: str
    password: str
    todo_id: int

#Creating Somethins

@app.post('/users')
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    check = db.query(User).filter(user.email == User.email).first()
    if check:
        return "Existing Email"
    new_user = User(email = user.email, password = user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/login')
def login(credentials: LoginSchema, db: Session = Depends(get_db)):
    check = db.query(User).filter(
        credentials.email == User.email,
        credentials.password == User.password).first()
    if not check:
        return "Wrong Email or Password"
    return check

@app.post('/todos')
def add_task(todo: ToDoSchema, db: Session = Depends(get_db)):
    check = db.query(User).filter(
        todo.email == User.email,
        todo.password == User.password).first()
    if not check:
        return "ERROR"
    new_todo = Todo(title = todo.title, done = False, user_id = check.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.put('/todos')
def task_done(data: TaskDoneSchema, db: Session = Depends(get_db)):
    check = db.query(User).filter(
        data.email == User.email,
        data.password == User.password).first()
    if not check:
        return "ERROR"
    todo = db.query(Todo).filter(
    Todo.id == data.todo_id,
    Todo.user_id == check.id
    ).first()

    todo.done = True
    db.commit()
    db.refresh(todo)
    return todo

    

