from fastapi import FastAPI
from app.db.database import engine
from app.models import schema
from app.routers import account, auth, transactions, category

app = FastAPI()

schema.Base.metadata.create_all(bind=engine)


app.include_router(account.router)
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(category.router)
