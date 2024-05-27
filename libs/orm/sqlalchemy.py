from typing import Final

from sqlalchemy import MetaData
from sqlalchemy.orm import registry

orm_registry: Final = registry()

metadata = MetaData()
