import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from graphql_api.mutations import Mutation
from graphql_api.queries import Query


app = FastAPI(
    title="Actividad 4 - Empresa y Usuarios",
    version="1.0.0"
)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=strawberry.schema.config.StrawberryConfig(
        auto_camel_case=True
    )
)

graphql_app = GraphQLRouter(schema)


app.include_router(
    graphql_app,
    prefix="/graphql"
)


@app.get("/")
def inicio():
    return {
        "mensaje": "Backend de la Actividad 4 funcionando"
    }


@app.get("/sistema")
def obtener_sistema():
    return {
        "aplicacion": "Actividad 4 - Empresa y Usuarios",
        "version": "1.0.0",
        "framework": "FastAPI",
        "ambiente": "Docker"
    }