import json

from aiohttp import web
from aiohttp.web import Application, Request, Response, json_response, run_app
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession as SessType

from models import AsyncSession, Desk, close_orm, init_orm
from pynda_model import CreateOwnerRequest, UpdateOwnerRequest, validate


def get_error(error_cls, message):
    err_message = {"error": message}
    error_json = json.dumps(err_message)
    return error_cls(text=error_json, content_type="application/json")


async def orm_context(app: web.Application):
    print("START")
    await init_orm()
    yield
    await close_orm()
    print("FINISH")


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with AsyncSession() as sess:
        request.sess = sess
        response = await handler(request)

        return response


app = Application()
app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


async def add_desk(sess: SessType, desk: Desk):
    sess.add(desk)
    try:
        await sess.commit()
    except IntegrityError:

        raise web.HTTPConflict(
            text='{"error":"Desk already create"}', content_type="application/json"
        )


class DeskView(web.View):

    @property
    def desk_id(self):
        return int(self.request.match_info["desk_id"])

    @property
    def sess(self) -> SessType:
        return self.request.sess

    async def get_curr_desk(self):
        desk = await self.sess.get(Desk, self.desk_id)
        if desk is None:
            raise get_error(web.HTTPNotFound, "Desk not found")
        return desk

    async def get(self):
        desk = await self.get_curr_desk()
        return web.json_response(desk.dict)

    async def post(self):
        json_data = await self.request.json()
        validate_data = validate(CreateOwnerRequest, json_data)

        desk = Desk(
            header=validate_data["header"],
            description=validate_data["description"],
            owner=validate_data["owner"],
        )
        await add_desk(self.sess, desk)
        return web.json_response(desk.id_dict, status=201)

    async def patch(self):
        json_data = await self.request.json()
        validate_data = validate(UpdateOwnerRequest, json_data)
        desk = await self.get_curr_desk()
        if "header" in validate_data:
            desk.header = validate_data["header"]
        if "description" in validate_data:
            desk.description = validate_data["description"]
        if "owner" in validate_data:
            desk.owner = validate_data["owner"]
        await add_desk(self.sess, desk)

        return web.json_response(desk.id_dict)

    async def delete(self):

        desk = await self.get_curr_desk()
        await self.sess.delete(desk)
        await self.sess.commit()
        return web.json_response({"status": "deleted"})


app.add_routes(
    [
        web.get(r"/desk/{desk_id:\d+}", DeskView),
        web.patch(r"/desk/{desk_id:\d+}", DeskView),
        web.delete(r"/desk/{desk_id:\d+}", DeskView),
        web.post(r"/desk/", DeskView),
    ]
)

run_app(app, port=8081)
