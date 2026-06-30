from pydantic import BaseModel

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

class DeleteTodoSchema(BaseModel):
    email: str
    password: str
    todo_id: int