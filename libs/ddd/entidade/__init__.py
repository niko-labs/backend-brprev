import abc


class Entidade(abc.ABC):
    ...

    arbitrary_types_allowed = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={getattr(self, 'id', None)})"
