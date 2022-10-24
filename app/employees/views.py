import aiohttp_jinja2
import db
from aiohttp import web


async def index(request):
    return web.Response(text="Hello, world")


@aiohttp_jinja2.template("employees.html")
class EmployeeView(web.View):
    async def get(self):
        async with self.request.app["db"].acquire() as conn:
            cursor = await conn.execute(db.employees.select())
            records = await cursor.fetchall()
            employees = [dict(r) for r in records]

            for employee in employees:
                employee["position"] = await self.get_position(employee["position_id"])
                employee["chief"] = await self.get_chief(employee["chief_id"])

            for employee in employees:
                if employee["chief"]:
                    for chief in employees:
                        if chief["name"] == employee["chief"]:
                            chief.setdefault("subordinates", []).append(employee)

            chief = [employee for employee in employees if not employee["chief"]][0]
            return {"chief": chief}

    async def post(self):
        data = await self.request.json()
        async with self.request.app["db"].acquire() as conn:
            await conn.execute(db.employees.insert().values(**data))

            return web.Response(status=201, text="Employee created.")

    async def put(self):
        data = await self.request.json()
        async with self.request.app["db"].acquire() as conn:
            await conn.execute(
                db.employees.update()
                .where(db.employees.c.id == data["id"])
                .values(**data)
            )
            return web.Response(status=200, text="Employee updated.")

    async def delete(self):
        data = await self.request.json()
        async with self.request.app["db"].acquire() as conn:
            await conn.execute(
                db.employees.delete().where(db.employees.c.id == data["id"])
            )
            return web.Response(status=204, text="Employee deleted.")

    async def get_position(self, position_id):
        async with self.request.app["db"].acquire() as conn:
            cursor = await conn.execute(
                db.positions.select().where(db.positions.c.id == position_id)
            )
            record = await cursor.fetchone()
            return dict(record)["name"]

    async def get_chief(self, chief_id):
        async with self.request.app["db"].acquire() as conn:
            cursor = await conn.execute(
                db.employees.select().where(db.employees.c.id == chief_id)
            )
            record = await cursor.fetchone()
            return dict(record)["name"] if record else None
