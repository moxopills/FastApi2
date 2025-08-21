from fastapi import FastAPI, HTTPException, Path, Query
from typing import Annotated
from app.models.users import UserModel, UserCreateRequest, UserUpdateRequest, UserSearchRequest

app = FastAPI()
UserModel.create_dummy()  # 더미 데이터 생성

@app.get("/users")
async def create_users(data: UserCreateRequest):
    user = UserModel(**data.model_dump())
    return {"id": user.id}

@app.get("/users/all")
async def get_all_users():
    result = UserModel.all()
    if not result:
        raise HTTPException(status_code=404, detail="No Users")
    return result

@app.get("/users/user_id")
async def get_user_id(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="No User")
    return user

@app.put("/users/{user_id}")
async def update_user(data: UserUpdateRequest, user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="NOT Found User")
    user.update(**data.model_dump())
    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    user.delete()
    return {"detail": f"User {user_id}, Successfully Deleted"}

@app.get("/users/search")
async def get_search_user(query_params: Annotated[UserSearchRequest, Query()]):
    valid_query = {k: v for k, v in query_params.model_dump().items() if v is not None}
    filtered_users = UserModel.filter(**valid_query)
    if not filtered_users:
        raise HTTPException(status_code=404)
    return filtered_users

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
