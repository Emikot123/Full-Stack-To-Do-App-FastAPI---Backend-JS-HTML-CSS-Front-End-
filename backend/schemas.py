from pydantic import BaseModel

class LoginSchema(BaseModel):
    email: str
    password: str

class UserSchema(BaseModel):
    email: str
    password: str

class ToDoSchema(BaseModel):
    title: str
    token: str

class TaskDoneSchema(BaseModel):
    token: str
    todo_id: int

class DeleteTodoSchema(BaseModel):
    token: str
    todo_id: int

class GetTodosSchema(BaseModel):
    token: str


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True