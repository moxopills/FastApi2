from http.client import HTTPException
from typing import Annotated
from fastapi import FastAPI
from mypy.dmypy.client import request

from app.models.users import UserModel, UserCreateRequest

app = FastAPI()
UserModel.create_dummy() # API 테스트를 위한 더미를 생성하는 메서드 입니다.

@app.get("/users")
async def create_users(data:UserCreateRequest):
    user = UserModel(**data.model_dump())
    return user.id

@app.get("/users")
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

@app.get("users/{user_id}")
async def get_user(data:UserUpdateRequest,user_id: int= Path(gt=0)):
    user = UserModel.get(id=user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="NOT Found User")
    user.update(**data.model_dump())
    return user

@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HttpException(status_code=404)
    user.delete()

    return {'detail':f"User {user_id}, Successfully Deleted"}

@app.get("/users")
async def get_serch_user(query_params: Annotated[UserSearchRequest, Query()]):
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
    filtered_users = UserModel.filter(**valid_query)
    if not filtered_users:
        raise HTTPException(status_code=404)
    return filtered_users

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)