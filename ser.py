# from aiohttp.web import run_app, Application, Request, Response, json_response
# from aiohttp import web
# from pip._vendor.rich import status
# from models import init_orm, close_orm, AsyncSession, Desk
# from sqlalchemy.exc import IntegrityError
#
#
# async def orm_context(app: web.Application):
#     print("START")ф
#     await init_orm()
#     yield
#     await close_orm()
#     print("FINISH")
#
#
# app = Application()
# app.cleanup_ctx.append(orm_context)
#
#
# class DeskView(web.View):
#     async def get(self):
#         desk_id = int(self.request.match_info["desk_id"])
#         async with AsyncSession() as sess:
#             desk = await sess.get(Desk, desk_id)
#             if desk is None:
#                 raise web.HTTPFound(
#                     text='{"error":"Desk not found"}',
#                     content_type="application/json"
#                 )
#             return web.json_response(desk.dict)
#
#     async def post(self):
#         json_data = await self.request.json()
#         async with AsyncSession() as sess:
#             desk = Desk(header=json_data["header"], description=json_data["description"], owner=json_data["owner"])
#
#             sess.add(desk)
#             print(desk.id_dict)
#             try:
#                 await sess.commit()
#             except IntegrityError:
#
#                 raise web.HTTPConflict(
#                     text='{"error":"Desk already create"}',
#
#                     content_type="application/json"
#                 )
#                 return web.json_response(desk.id_dict)
#
#             return web.json_response(desk.id_dict, status=201)
#
#     async def patch(self):
#         desk_id = int(self.request.match_info["desk_id"])
#         json_data = await self.request.json()
#         async with AsyncSession() as sess:
#             desk = await sess.get(Desk, desk_id)
#             if desk is None:
#                 raise web.HTTPFound(
#                     text='{"error":"Desk not found"}',
#                     content_type="application/json"
#                 )
#             if "header" in json_data:
#                 desk.header = json_data["header"]
#             if "description" in json_data:
#                 desk.header = json_data["description"]
#             if "owner" in json_data:
#                 desk.header = json_data["owner"]
#
#             sess.add(desk)
#             try:
#                 await sess.commit()
#             except IntegrityError:
#                 raise web.HTTPConflict(
#                     text='{"error":"Desk already create"}',
#                     content_type="application/json"
#                 )
#
#             return web.json_response(desk.id_dict)
#
#     async def delete(self):
#         desk_id = int(self.request.match_info["desk_id"])
#         async with AsyncSession() as sess:
#             desk = await sess.get(Desk, desk_id)
#             if desk is None:
#                 raise web.HTTPFound(
#                     text='{"error":"Desk not found"}',
#                     content_type="application/json"
#                 )
#             await sess.delete(desk)
#             await sess.commit()
#             return web.json_response({"status": "deleted"})
#
#     # async def hello_world(request: Request):
#     #     try:
#     #         some_id = int(request.match_info["some_id"])
#     #         json_data = await request.json()
#     #         qs = request.query
#     #         headers = request.headers
#     #         print(f"{some_id=},{json_data=},{qs=},{headers=}")
#     #         http_resp = json_response({"hello": "world"})
#     #     except Exception as e:
#     #         return json_response({"error": str(e)}, status=400)
#     #     return http_resp
#
#
# app.add_routes(
#     [
#         web.get(r"/desk/{desk_id:\d+}", DeskView),
#         web.patch(r"/desk/{desk_id:\d+}", DeskView),
#         web.delete(r"/desk/{desk_id:\d+}", DeskView),
#         web.post(r"/desk/", DeskView),
#     ]
# )
#
# run_app(app, port=8081)
