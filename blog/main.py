from fastapi import Depends, FastAPI, status, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext


from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog")
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog/{id}")
def get_blog(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).first()
    db.commit()
    return "deleted"


@app.put("/blog/{id}")
def get_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update(request)
    db.commit()
    return "deleted"


@app.delete("/blog/{id}")
def delete_blog(id, db: Session = Depends(get_db)):
    delete_blog = (
        db.query(models.Blog)
        .filter(models.Blog.id == id)
        .delete(synchronize_session=False)
    )
    return delete_blog


@app.post("/user", response_model=schemas.ShowUser)
def create_user(
    request: schemas.User, db: Session = Depends(get_db), status=status.HTTP_201_CREATED
):
    hashed_password = pwd_cxt.hash(request.password)
    db_user = models.User(
        name=request.name, email=request.email, password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/user", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found"
        )
    return user
