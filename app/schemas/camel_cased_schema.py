from pydantic import BaseModel


def to_camel_case(input: str) -> str:
    '''Returns a camelCased version of the given input.'''

    words = input.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])


class CamelCasedSchema(BaseModel):
    '''A schema that serializes its fields to camelCased versions of their regular names.
    The fields are still programatically accessible using their original snake_cased names.'''

    class Config:
        alias_generator = to_camel_case
        allow_population_by_field_name = True
