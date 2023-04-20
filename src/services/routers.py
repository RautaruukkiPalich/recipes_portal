# import json
#
# from fastapi import APIRouter, Request, Response
#
# router = APIRouter()
#
#
# @router.get("/", tags=["index"])
# async def start(request: Request) -> Response:
#     content = json.dumps({"data": "Hello world"})
#     return Response(
#         content=content,
#         status_code=200,
#         headers=request.headers,
#     )
#
# #
# # @router.get("/register", tags=["register"])
# # async def get_register():
# #     content = {"data": "get_register"}
# #     return content
# #
# #
# # @router.post("/register", tags=["register"])
# # async def post_register():
# #     content = {
# #         "status": 200,
# #         "message": "success",
# #         "data": "post_register",
# #     }
# #     return content
#
#
# @router.get("/user/{user_nickname}")
# async def get_user(user_nickname: str):
#     content = [user for user in users if user.get("nickname").lower() == user_nickname.lower()]
#     return content
