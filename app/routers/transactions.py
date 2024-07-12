from fastapi import APIRouter, Path, File, UploadFile, HTTPException
from app.models.schema import Transaction, Account
from app.dependencies.dependencies import db_dependecy, user_dependecy
from pydantic import BaseModel
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
from sqlalchemy import func
import io
import pandas as pd
import os
from decimal import Decimal
from app.utils.utils_functions import extractTransactionData

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


def decimalToFloat(value):
    if isinstance(value, Decimal):
        return float(value)
    return value


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
    earning = db.query(func.coalesce(func.sum(Transaction.amount), 0).label("earning"))

    if allTransactionRequest.category != "ALL":
        trn = trn.filter(Transaction.category == allTransactionRequest.category)
        earning = earning.filter(Transaction.category == allTransactionRequest.category)

    if allTransactionRequest.transaction_type != "ALL":
        trn = trn.filter(
            Transaction.transaction_type == allTransactionRequest.transaction_type
        )

    if allTransactionRequest.account != "ALL":
        trn = trn.filter(Account.name == allTransactionRequest.account)
        earning = earning.filter(Account.name == allTransactionRequest.account)

    if allTransactionRequest.from_date and allTransactionRequest.to_date:
        from_date_obj = datetime.strptime(allTransactionRequest.from_date, "%Y-%m-%d")
        to_date_obj = datetime.strptime(allTransactionRequest.to_date, "%Y-%m-%d")
        trn = trn.filter(Transaction.date.between(from_date_obj, to_date_obj))
        earning = earning.filter(Transaction.date.between(from_date_obj, to_date_obj))

    if allTransactionRequest.transaction_type == "Income":
        income = db.execute(
            earning.filter(Transaction.transaction_type == "Income")
        ).scalar()
        db.execute(income).scalar()
        expense = 0

    elif allTransactionRequest.transaction_type == "Expense":
        expense = earning.filter(Transaction.transaction_type == "Expense")
        db.execute(income).scalar()
        income = 0

    else:
        income = db.execute(
            earning.filter(Transaction.transaction_type == "Income")
        ).scalar()
        expense = db.execute(
            earning.filter(Transaction.transaction_type == "Expense")
        ).scalar()

    netEarnings = income - expense
    transactions = [
        {
            "category": transaction.category,
            "date": transaction.date,
            "transaction_type": transaction.transaction_type,
            "amount": transaction.amount,
            "account": transaction.name,
            "remarks": transaction.remarks,
        }
        for transaction in trn.all()
    ]
    print(netEarnings, income, expense)
    return JSONResponse(
        {
            "transactions": transactions,
            "net_earnings": decimalToFloat(netEarnings),
            "total_income": decimalToFloat(income),
            "total_expense": decimalToFloat(expense),
        }
    )


@router.get("/get_transaction/{id}")
async def getTransaction(user: user_dependecy, db: db_dependecy, id: int = Path(gt=0)):
    trn = (
        db.query(Transaction)
        .filter(Transaction.user_id == 1, Transaction.id == id)
        .first()
    )
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


@router.post("/extract_and_uplod_trasaction")
async def extractAndUploadTrasaction(
    db: db_dependecy, user: user_dependecy, file: UploadFile = File(...)
):
    try:
        content = file.file.read()
        df = pd.read_excel(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading Excel file: {e}")
    transactions = extractTransactionData(df)

    if any(
        [
            True
            for each in transactions
            for k, v in each.items()
            if (k != "remarks" and v == "")
        ]
    ):
        return JSONResponse({"error": "One of column is empty"})

    for each in transactions:
        account = (
            db.query(Account)
            .filter(
                Account.name == each.get("account_name"),
                Account.user_id == user.get("user_id"),
            )
            .first()
        )
        if each.get("transaction_type") == "Income":
            account.balance += each.get("amount")
        if each.get("transaction_type") == "Expense":
            account.balance += each.get("amount")
        trn = Transaction(
            amount=each.get("amount"),
            date=each.get("date"),
            category=each.get("category"),
            transaction_type=each.get("transaction_type"),
            remarks=each.get("remarks"),
            account_id=account.id,
            user_id=user.get("user_id"),
        )
        db.add(trn)
        db.commit()

    return JSONResponse({"message": "Succefully added transactions"})


@router.get("/download_sample_file")
async def download_sample_file(user: user_dependecy):
    if not user:
        return JSONResponse({"message": "Not Authenticated"})
    filePath = os.path.join("app/static", "transactions.xlsx")
    if not os.path.exists(filePath):
        return {"error": "File not found"}
    return FileResponse(filePath)


@router.post("/transaction_report")
async def transactionReport(
    db: db_dependecy, user: user_dependecy, allTransactionRequest: AllTransactionRequest
):
    trn = (
        db.query(
            Transaction.amount,
            func.date_format(Transaction.date, "%Y-%m-%d").label("date"),
            Transaction.category,
            Transaction.transaction_type,
            Transaction.remarks,
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

    transactions_list = [
        {
            "category": transaction.category,
            "date": transaction.date,
            "transaction_type": transaction.transaction_type,
            "amount": transaction.amount,
            "account": transaction.name,
            "remarks": transaction.remarks,
        }
        for transaction in trn.all()
    ]

    df = pd.DataFrame(transactions_list)
    df.columns = [
        "Category",
        "Transaction Date",
        "Transaction Type",
        "Amount",
        "Account",
        "Remarks",
    ]

    excel_file = "transaction_report.xlsx"

    df.to_excel(excel_file, index=False)

    response = FileResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=excel_file,
    )
    # os.remove(excel_file)

    return response
