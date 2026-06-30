from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, Base, Todo
from pydantic import BaseModel
import bcrypt
from schemas import UserSchema, LoginSchema, ToDoSchema, GetTodosSchema, TaskDoneSchema, DeleteTodoSchema

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Creating and Updating

@app.post('/users')
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    check = db.query(User).filter(user.email == User.email).first()
    if check:
        raise HTTPException(status_code=409, detail="Email already exists")
    
    hashed = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(email = user.email, password = hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/login')
def login(credentials: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == credentials.email
    ).first()
    if not user:
        raise HTTPException(status_code=400, detail="Wrong email or password")
    if not bcrypt.checkpw(credentials.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Wrong email or password")
    return user

@app.post('/todos')
def add_task(todo: ToDoSchema, db: Session = Depends(get_db)):
    check = db.query(User).filter(
        todo.email == User.email,
        todo.password == User.password).first()
    if not check:
        raise HTTPException(status_code=400, detail="Error")
    new_todo = Todo(title = todo.title, done = False, user_id = check.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.put('/todos/done')
def task_done(data: TaskDoneSchema, db: Session = Depends(get_db)):
    check = db.query(User).filter(
        data.email == User.email,
        data.password == User.password).first()
    if not check:
        raise HTTPException(status_code=400, detail="Error")
    todo = db.query(Todo).filter(
    Todo.id == data.todo_id,
    Todo.user_id == check.id
    ).first()

    todo.done = True
    db.commit()
    db.refresh(todo)
    return todo

@app.put('/todos/undone')
def task_false(data: TaskDoneSchema, db: Session = Depends(get_db)):
    check = db.query(User).filter(
        data.email == User.email,
        data.password == User.password).first()
    if not check:
        return "ERROR"
    todo = db.query(Todo).filter(
    Todo.id == data.todo_id,
    Todo.user_id == check.id
    ).first()

    todo.done = False
    db.commit()
    db.refresh(todo)
    return todo

#View

@app.post('/todos/get')
def get_todos(credentials: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == credentials.email,
        User.password == credentials.password
    ).first()
    if not user:
        return "Wrong Email or Password"
    return db.query(Todo).filter(Todo.user_id == user.id).all()


#Delete Tasks

@app.delete('/todos')
def del_todo(credentials: DeleteTodoSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == credentials.email,
        User.password == credentials.password
    ).first()
    if not user:
        return { 'error': 'wrong email or password' }
    task = db.query(Todo).filter(
        Todo.id == credentials.todo_id,
        Todo.user_id == user.id
    ).first()
    if not task:
        return { 'error': 'todo not found' }
    db.delete(task)
    db.commit()
    return task
    



    

