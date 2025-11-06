from pydantic import BaseModel, StringConstraints, Field, EmailStr, ConfigDict, computed_field
from typing import Annotated, Literal, Optional, List

class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr = Field(strict=True)
    first_name: Annotated[str, StringConstraints(max_length=255)]
    last_name: Annotated[str, StringConstraints(max_length=255)]


class NoteCreateModel(BaseModel):
    email: EmailStr
    title: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    content: Optional[str]
    codes: List['CodeModel']

class NoteModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    note_id: int = Field(strict=True)
    email: EmailStr
    title: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    content: Optional[str]
    codes: List['CodeModel']

class CodeModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chapter_code: Annotated[str, StringConstraints(max_length=1, to_upper=True)]
    category_code: Annotated[str, StringConstraints(max_length=2, min_length=2, to_upper=True)]
    subcategory_code: Annotated[str, StringConstraints(max_length=1, to_upper=True)] = Field(default='-')
    title: Annotated[str, StringConstraints(max_length=255)]
    description: Optional[str]

    @classmethod
    def icd_code_str(cls, repr_type: Literal['code', 'code+title', 'full']='code') -> str:
        category_code_str = f'{cls.category_code}'
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