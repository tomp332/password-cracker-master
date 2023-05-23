from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from password_cracker_master.src.routes.minion_routes.router import minion_router
from password_cracker_master.src.routes.password_routes.router import passwords_router
from password_cracker_master.src.routes.tasks_routes.router import tasks_router
from password_cracker_master.src.utils import startup_actions

main_api_router = FastAPI(
    title="Password Cracker API",
    description="Password Cracker Master API",
    version="1.0.0"
)

origins = ["*"]

main_api_router.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@main_api_router.on_event("startup")
async def on_startup() -> None:
    await startup_actions()


# include routes
main_api_router.include_router(passwords_router, tags=["Passwords"])
main_api_router.include_router(tasks_router, tags=["Tasks"])
main_api_router.include_router(minion_router, tags=["Minions"])
