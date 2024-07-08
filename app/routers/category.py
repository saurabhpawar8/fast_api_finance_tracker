from fastapi import APIRouter, Path
from app.models.schema import Category
from app.dependencies.dependencies import db_dependecy, user_dependecy
from pydantic import BaseModel
from fastapi.responses import JSONResponse


router = APIRouter()


class CategoryRequest(BaseModel):
    name: str


@router.post("/create_category")
async def createCategory(
    user: user_dependecy, db: db_dependecy, categoryRequest: CategoryRequest
):
    category = Category(**categoryRequest.model_dump(), user_id=user.get("user_id"))
    db.add(category)
    db.commit()
    return JSONResponse(content={"message": "Added successfully"})


@router.get("/get_category/{id}")
async def getCategory(user: user_dependecy, db: db_dependecy, id: int = Path(gt=0)):
    category = (
        db.query(Category)
        .filter(Category.id == id, Category.user_id == user.get("user_id"))
        .first()
    )
    return category


@router.put("/update_category/{id}")
async def updateCategory(
    user: user_dependecy,
    db: db_dependecy,
    categoryRequest: CategoryRequest,
    id: int = Path(gt=0),
):
    category = (
        db.query(Category)
        .filter(Category.id == id, Category.user_id == user.get("user_id"))
        .first()
    )
    category.name = categoryRequest.name

    db.add(category)
    db.commit()

    return JSONResponse(content={"message": "Category updated successfully"})


@router.get("/get_all_accounts")
async def getAllCategories(user: user_dependecy, db: db_dependecy):
    categories = (
        db.query(Category).filter(Category.user_id == user.get("user_id")).all()
    )
    return categories
