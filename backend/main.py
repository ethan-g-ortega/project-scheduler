from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query, status
from pydantic import BaseModel
from contextlib import asynccontextmanager
from sqlalchemy.exc import IntegrityError
from typing import List, Annotated
import models
from schemas import CustomerCreate, CustomerRead, CustomerUpdate, ProjectCreate, ProjectRead, ProjectUpdate
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import inspect

@asynccontextmanager
async def lifespan(app: FastAPI):
    import models
    models.Base.metadata.create_all(bind=engine)
    print("Tables now:", inspect(engine).get_table_names())  # should show ['customers', 'projects']
    yield


app = FastAPI(lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/customers/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    obj = models.Customers(
        first_name = payload.first_name,
        last_name=payload.last_name,
        email=str(payload.email),
        preferred_lang=payload.preferred_lang,
        )
    db.add(obj)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        #UNIQUE violation on email (CITEXT)
        raise HTTPException(status_code=409, detail="Email already exists") from e
    db.refresh(obj)
    return obj

@app.patch("/customers/{customer_id}", response_model=CustomerRead, status_code=status.HTTP_202_ACCEPTED)
def update_customer(customer_id:int, payload: CustomerUpdate, db: Session=Depends(get_db)):
    obj = db.get(models.Customers, customer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    #only update fields that were provided
    changes = payload.model_dump(exclude_unset=True)
    for k, v in changes.items():
        setattr(obj, k, v)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()

        raise HTTPException(status_code=409, detail="Email already exists") from e
    
    db.refresh(obj)
    return obj
            
@app.get("/customers/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, db: Session=Depends(get_db)):
    obj = db.get(models.Customers, customer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Customer not found")
    return obj


@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session=Depends(get_db)):
    obj = db.get(models.Customers, customer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(obj)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()

        raise HTTPException(status_code=409, detail="Cannot delete: customer has related projects") from e
    
@app.post("/projects/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session=Depends(get_db)):
    #ensure customer exists
    parent = db.get(models.Customers, payload.customer_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Customer does not exist")

    obj = models.Projects(**payload.model_dump())
    db.add(obj)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()

        raise HTTPException(status_code=409, detail="Could not create project/") from e
    db.refresh(obj)
    return obj

@app.get("/projects/{project_id}", response_model=ProjectRead, status_code=status.HTTP_200_OK)
def get_project(project_id: int, db: Session=Depends(get_db)):
    obj = db.get(models.Projects, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return obj

@app.patch("/projects/{project_id}/", response_model=ProjectRead, status_code=status.HTTP_200_OK)
def update_project(project_id: int, payload: ProjectUpdate, db: Session=Depends(get_db)):
    obj = db.get(models.Projects, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="project not found")
    
    changes = payload.model_dump(exclude_unset=True)

    for k,v in changes.items():
        setattr(obj, k, v)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()

        raise HTTPException(status_code=409, detail="Unable to update project") from e
    
    db.refresh(obj)
    return obj

@app.delete("/projects/{project_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session=Depends(get_db)):
    obj = db.get(models.Projects, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="project not found")
    db.delete(obj)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()

        raise HTTPException(status_code=409, detail="Unable to delete projetct") from e
    
@app.get("/customers/{customer_id}/projects/", response_model=list[ProjectRead])
def list_projects_for_customer(customer_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Customers, customer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return db.query(models.Projects).where(models.Projects.customer_id == customer_id).order_by(models.Projects.start_date).all()