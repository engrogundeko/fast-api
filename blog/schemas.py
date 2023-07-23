from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str
    
    class config:
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

    class config:
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str

    class config:
        orm_mode = True
