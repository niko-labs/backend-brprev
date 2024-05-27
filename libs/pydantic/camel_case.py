from pydantic import BaseModel, Extra


class CamelModel(BaseModel):
    class Config:
        def alias_generator(v):
            return CamelModel.to_camel_case(v)

        allow_population_by_field_name = True
        extra: Extra.forbid

    @staticmethod
    def to_camel_case(word):
        return "".join(
            v.capitalize() if i > 0 else v for i, v in enumerate(word.split("_"))
        )
