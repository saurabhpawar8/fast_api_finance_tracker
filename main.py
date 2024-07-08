from fastapi import FastAPI
from core.models.database import engine
from core.schemas import schema
from core.routers import account, auth, transactions, category

app = FastAPI()

schema.Base.metadata.create_all(bind=engine)


app.include_router(account.router)
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(category.router)
