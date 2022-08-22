import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .system.database import register_orm
from .system.logger import init_logging
from .system.settings import Settings, config
from .system.strawberry.schema import graphql_router


class Kernel:
    def __init__(self, config: Settings) -> None:
        self.__config = config
        self.__app = FastAPI(debug=self.__config.debug)
        self.__boot = False

    def __load_routes(self) -> None:
        self.__app.include_router(graphql_router, prefix="/graphql", include_in_schema=False)

    def __configure_cors(self) -> None:
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def boot(self) -> FastAPI:
        if self.__boot:
            return self.__app

        self.__boot = True
        self.__configure_cors()
        self.__load_routes()

        register_orm(
            app=self.__app,
            database_url=self.__config.database_url,
            generate_schemas=self.__config.generate_schemas,
        )

        return self.__app


app = Kernel(config=config).boot()

init_logging()


if __name__ == "__main__":
    if config.debug:
        import debugpy

        debugpy.listen(("0.0.0.0", 5678))

    uvicorn.run(
        "pizzeria.kernel:app",
        host=config.host,
        port=config.port,
        reload=config.reload,
        workers=config.workers,
    )
