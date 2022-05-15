from typing import List
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from server import crud, models, schemas
from server.database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bank", docs_url="/")

@app.get("/ping")
def ping():
    return {"ping": "pong"}

@app.post("/accounts/", response_model=schemas.Account)
def create_account(account: schemas.AccountIn, db: Session = Depends(get_db)):
    return crud.create_account(db=db, account=account)

@app.get("/accounts/", response_model=List[schemas.Account])
def read_accounts(db: Session = Depends(get_db)):
    accounts = crud.get_accounts(db)
    return accounts

@app.get("/accounts/{account_id}", response_model=schemas.Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@app.get("/accounts/{account_id}/transactions/", response_model=List[schemas.Transaction])
def get_transactions_by_account(
    account_id: int, db: Session = Depends(get_db)
):
    return crud.get_transactions_by_acc(db=db, id=account_id)

@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionIn, db: Session = Depends(get_db)):
    return crud.create_transaction(db=db, transaction=transaction)

@app.get("/transactions/", response_model=List[schemas.Transaction])
def read_transactions(db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db)
    return transactions


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
