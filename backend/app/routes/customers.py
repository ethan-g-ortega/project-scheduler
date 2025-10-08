from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db            # <-- move get_db here
from app.models.customers import Customers
from app.schemas.customers import CustomerCreate, CustomerRead, CustomerUpdate
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/customers/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    obj = Customers(
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

@router.patch("/customers/{customer_id}", response_model=CustomerRead, status_code=status.HTTP_202_ACCEPTED)
def update_customer(customer_id:int, payload: CustomerUpdate, db: Session=Depends(get_db)):
    obj = db.get(Customers, customer_id)
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
            
@router.get("/customers/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, db: Session=Depends(get_db)):
    obj = db.get(Customers, customer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Customer not found")
    return obj


@router.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session=Depends(get_db)):
    obj = db.get(Customers, customer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(obj)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()

        raise HTTPException(status_code=409, detail="Cannot delete: customer has related projects") from e