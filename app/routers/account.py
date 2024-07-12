from fastapi import APIRouter, Path
from app.models.schema import Account
from app.dependencies.dependencies import db_dependecy, user_dependecy
from pydantic import BaseModel
from fastapi.responses import JSONResponse


router = APIRouter()


class AccountRequest(BaseModel):
    name: str
    type: str
    balance: float


@router.post("/create_account")
async def createAccount(
    user: user_dependecy,
    db: db_dependecy,
    accountRequest: AccountRequest,
):
    print(user)
    if user is None:
        return JSONResponse({"error": "Authentication failed"})
    if (
        db.query(Account)
        .filter(
            Account.name == accountRequest.name, Account.user_id == user.get("user_id")
        )
        .first()
    ):
        return JSONResponse({"message": "Account already exists"})
    acc = Account(**accountRequest.model_dump(), user_id=user.get("user_id"))
    db.add(acc)
    db.commit()
    return JSONResponse(content={"message": "Added successfully"})


@router.get("/get_account/{id}")
async def getAccount(user: user_dependecy, db: db_dependecy, id: int = Path(gt=0)):
    if user is None:
        return JSONResponse({"error": "Authentication failed"})
    account = (
        db.query(Account)
        .filter(Account.id == id, Account.user_id == user.get("user_id"))
        .first()
    )
    return JSONResponse(account)


@router.put("/update_account/{id}")
async def updateAccount(
    user: user_dependecy,
    db: db_dependecy,
    accountRequest: AccountRequest,
    id: int = Path(gt=0),
):
    account = (
        db.query(Account)
        .filter(Account.id == id, Account.user_id == user.get("user_id"))
        .first()
    )
    account.name = accountRequest.name
    account.type = accountRequest.type
    account.balance = accountRequest.balance

    db.add(account)
    db.commit()

    return JSONResponse({"message": "Account updated successfully"})


@router.get("/get_all_accounts")
async def getAllAccounts(user: user_dependecy, db: db_dependecy):
    accounts = db.query(Account).filter(Account.user_id == user.get("user_id")).all()
    return accounts
