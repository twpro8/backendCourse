import asyncio
import sys
from contextlib import asynccontextmanager
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src import redis_manager
from src.api.auth import router as auth_router
from src.api.hotels import router as hotels_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router
from src.api.images import router as images_router


from src.api.dependencies import get_db
async def send_emails_regularly():
    async for db in get_db():
        res = await db.bookings.get_checkin_day()
        return print("GOT OT", f"{res=}")
async def run_send_emails_regularly():
    while True:
        await send_emails_regularly()
        await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(run_send_emails_regularly())
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()


app = FastAPI(title="Momoa Web API", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)
app.include_router(images_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True) # you can add workers but reload must be false
