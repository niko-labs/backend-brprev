from uuid import UUID, uuid4

from libs.pydantic.conversor import PydanticConversor


class BaseUUID(UUID, PydanticConversor):
    def __init__(self, *args):
        if not args:
            _id = str(uuid4())
        elif isinstance(args[0], (UUID, str)) or issubclass(self.__class__, BaseUUID):
            _id = str(args[0])
        else:
            raise ValueError(f"Você não pode transformar um {args[0]} em um UUID")

        super().__init__(_id)

    @staticmethod
    def is_valid(uuid_to_test):
        if isinstance(uuid_to_test, UUID):
            return True

        try:
            uuid_obj = UUID(uuid_to_test, version=4)
        except Exception:
            return False
        return str(uuid_obj) == uuid_to_test
