from fastapi import APIRouter, Path
from app.models.schema import Transaction, Account
from app.dependencies.dependencies import db_dependecy, user_dependecy
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy import func


router = APIRouter()


class TransactionRequest(BaseModel):
    amount: float
    date: str
    transaction_type: str
    category: str
    remarks: str
    account: str


class AllTransactionRequest(BaseModel):
    from_date: str
    to_date: str
    transaction_type: str
    category: str
    account: str


@router.post("/create_transaction")
async def createTransaction(
    user: user_dependecy, db: db_dependecy, transactionRequest: TransactionRequest
):
    account_id = (
        db.query(Account)
        .filter(
            Account.name == transactionRequest.account,
            Account.user_id == user.get("user_id"),
        )
        .first()
        .id
    )
    date = datetime.strptime(transactionRequest.date, "%Y-%m-%d")
    trn = Transaction(
        amount=transactionRequest.amount,
        date=date,
        category=transactionRequest.category,
        transaction_type=transactionRequest.transaction_type,
        remarks=transactionRequest.remarks,
        account_id=account_id,
        user_id=user.get("user_id"),
    )
    db.add(trn)
    db.commit()

    return JSONResponse(content={"message": "Transaction created successfully"})


@router.post("/get_all_transactions")
async def getAllTransactions(
    user: user_dependecy, db: db_dependecy, allTransactionRequest: AllTransactionRequest
):

    trn = (
        db.query(
            Transaction.id,
            Transaction.amount,
            func.date_format(Transaction.date, "%Y-%m-%d").label("date"),
            Transaction.category,
            Transaction.transaction_type,
            Transaction.remarks,
            Transaction.user_id,
            Account.name,
        )
        .join(Account, Transaction.account_id == Account.id)
        .filter(Transaction.user_id == user.get("user_id"))
    )

    if allTransactionRequest.category != "ALL":
        trn = trn.filter(Transaction.category == allTransactionRequest.category)

    if allTransactionRequest.transaction_type != "ALL":
        trn = trn.filter(
            Transaction.transaction_type == allTransactionRequest.transaction_type
        )

    if allTransactionRequest.account != "ALL":
        trn = trn.filter(Account.name == allTransactionRequest.account)

    if allTransactionRequest.from_date and allTransactionRequest.to_date:
        from_date_obj = datetime.strptime(allTransactionRequest.from_date, "%Y-%m-%d")
        to_date_obj = datetime.strptime(allTransactionRequest.to_date, "%Y-%m-%d")
        trn = trn.filter(Transaction.date.between(from_date_obj, to_date_obj))

    t = trn.all()
    print(t)
    return t


@router.get("/get_transaction/{id}")
async def getTransaction(user: user_dependecy, db: db_dependecy, id: int = Path(gt=0)):
    trn = db.query(Transaction).filter(Transaction.user_id == 1).first()
    return trn


@router.put("/update_transaction/{id}")
async def updateTransaction(
    user: user_dependecy,
    db: db_dependecy,
    transactionRequest: TransactionRequest,
    id: int = Path(gt=0),
):
    trn = (
        db.query(Transaction)
        .filter(Transaction.user_id == user.get("user_id"), Transaction.id == id)
        .first()
    )
    accounts = (
        db.query(Transaction)
        .filter(Transaction.user_id == user.get("user_id"), Transaction.id == id)
        .first()
    )
    previousAmount = trn.amount
    if transactionRequest.transaction_type == "Income":
        accounts.amount = accounts.amount + (transactionRequest.amount - previousAmount)
    elif transactionRequest.transaction_type == "Expense":
        accounts.amount = accounts.amount - (transactionRequest.amount - previousAmount)

    trn.amount = transactionRequest.amount
    trn.account_id = accounts.id
    trn.category = transactionRequest.category
    trn.transaction_type = transactionRequest.transaction_type
    trn.date = transactionRequest.date
    trn.remarks = transactionRequest.remarks

    db.commit()
    return JSONResponse(content={"message": "Transaction updated successfully"})
