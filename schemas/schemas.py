from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal


class MedicinesCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    prescription: bool = False
    stock: int = Field(ge=0)


class MedicinesResponse(MedicinesCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SaleCreate(BaseModel):
    medicine_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class SaleResponse(SaleCreate):
    id: int
    sold_at: datetime

    model_config = ConfigDict(from_attributes=True)