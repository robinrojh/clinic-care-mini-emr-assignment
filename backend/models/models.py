from pydantic import BaseModel, StringConstraints, Field
from typing import Annotated, Literal
from math import floor, log10

class User(BaseModel):
    user_id: int = Field(strict=True)
    first_name: Annotated[str, StringConstraints(max_length=255)]
    last_name: Annotated[str, StringConstraints(max_length=255)]

class Note(BaseModel):
    note_id: int = Field(strict=True)
    user_id: int = Field(strict=True)
    title: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    content: str

class Code(BaseModel):
    chapter_code: Annotated[str, StringConstraints(max_length=1, to_upper=True)]
    category_code: Annotated[str, StringConstraints(max_length=2, min_length=2, to_upper=True)]
    subcategory_code: Annotated[str, StringConstraints(max_length=1, to_upper=True)] = Field(default='X')
    title: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    description: str

    @classmethod
    def icd_code_str(cls, repr_type: Literal['code', 'code+title', 'full']='code') -> str:
        is_single_digit = cls.category_code < 10
        category_code_str = f'0{cls.category_code}' if is_single_digit else f'{cls.category_code}'
        if repr_type == 'code':
            if cls.subcategory_code == 'X':
                return f"{cls.chapter_code}{category_code_str}"
            else:
                return f'{cls.chapter_code}{category_code_str}.{cls.subcategory_code}'
        elif repr_type == 'code+title':
            if cls.subcategory_code == 'X':
                return f'{cls.chapter_code}{category_code_str} {cls.title}'
            else:
                return f'{cls.chapter_code}{category_code_str}.{cls.subcategory_code} {cls.title}'
        elif repr_type == 'full':
            if cls.subcategory_code == 'X':
                return f'{cls.chapter_code}{category_code_str} {cls.title}\n    {cls.description}'
            else:
                return f'{cls.chapter_code}{category_code_str}.{cls.subcategory_code} {cls.title}\n    {cls.description}'
        else:
            raise ValueError(f'repr_type {repr_type} is not a possible representation type. Try \'code\', \'code+title\', or \'full\'')