import sys
from pathlib import Path
from typing import Any, Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

root = Path(__file__).resolve().parent.parent.parent
print("root-path-conftest", root)
sys.path.append(str(root))


from libs.env.gerenciador_de_envs import ENVS  # noqa: E402
from libs.orm.caregar_orm import carregar_orm  # noqa: E402
from libs.orm.sqlalchemy import metadata  # noqa: E402
from servidor.config import app  # noqa: E402

api = TestClient(app)


@pytest.fixture
def client() -> Generator[TestClient | None, Any, None]:
    idenificador_teste = "test_" + str(uuid4()).replace("-", "")

    _engine = create_engine(ENVS.DB_URI, isolation_level="AUTOCOMMIT")
    _cnx = _engine.connect()
    _cnx.execute(text(f"CREATE DATABASE {idenificador_teste}"))
    _cnx.close()
    _engine.dispose()

    ENVS.DB_NAME = idenificador_teste

    _engine = create_engine(ENVS.DB_URI, isolation_level="AUTOCOMMIT")

    carregar_orm()
    metadata.create_all(bind=_engine)
    yield api
    metadata.drop_all(bind=_engine)

    _engine.dispose()
