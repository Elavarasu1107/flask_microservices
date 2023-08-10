from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Annotated, List
from pydantic.functional_validators import AfterValidator


class NoteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = None
    title: str
    description: str
    reminder: Optional[Annotated[datetime, AfterValidator(str)]] = None
    user_id: int
