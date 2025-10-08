from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.db.session import get_db
from app.models.projects import Projects
from app.models.customers import Customers
from app.schemas.projects import ProjectCreate, ProjectRead, ProjectUpdate
from sqlalchemy.orm import Session
from sqlalchemy import inspect


router = APIRouter()

@router.post("/projects/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session=Depends(get_db)):
    #ensure customer exists
    parent = db.get(Customers, payload.customer_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Customer does not exist")

    obj = Projects(**payload.model_dump())
    db.add(obj)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()

        raise HTTPException(status_code=409, detail="Could not create project/") from e
    db.refresh(obj)
    return obj

@router.get("/projects/{project_id}", response_model=ProjectRead, status_code=status.HTTP_200_OK)
def get_project(project_id: int, db: Session=Depends(get_db)):
    obj = db.get(Projects, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return obj

@router.patch("/projects/{project_id}/", response_model=ProjectRead, status_code=status.HTTP_200_OK)
def update_project(project_id: int, payload: ProjectUpdate, db: Session=Depends(get_db)):
    obj = db.get(Projects, project_id)
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

@router.delete("/projects/{project_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session=Depends(get_db)):
    obj = db.get(Projects, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="project not found")
    db.delete(obj)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()

        raise HTTPException(status_code=409, detail="Unable to delete projetct") from e
    
@router.get("/customers/{customer_id}/projects/", response_model=list[ProjectRead])
def list_projects_for_customer(customer_id: int, db: Session = Depends(get_db)):
    obj = db.get(Customers, customer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return db.query(Projects).where(Projects.customer_id == customer_id).order_by(Projects.start_date).all()