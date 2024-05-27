from pydantic import BaseModel


def para_camel_case(string: str) -> str:
    palavras = string.split("_")
    nova_palavra = palavras[0]
    for palavra in palavras[1:]:
        nova_palavra += palavra.capitalize()

    return nova_palavra


class Modelo(BaseModel):
    class Config:
        alias_generator = para_camel_case
        populate_by_name = True
