from libs.env.gerenciador_de_envs import ENVS

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "servidor.config:app",
        host=ENVS.SERVER_HOST,
        port=ENVS.SERVER_PORT,
        workers=ENVS.SERVER_WORKERS,
    )
