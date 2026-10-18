from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.database import get_db
from database.models import Medicine
from schemas.schemas import MedicinesCreate, MedicinesResponse

router = APIRouter(prefix="/medicines", tags=["Препараты"])


@router.get("/", response_model=list[MedicinesResponse])
async def get_medicines(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Medicine))
    return result.scalars().all()


@router.get("/{medicine_id}", response_model=MedicinesResponse)
async def get_medicine(medicine_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Medicine).where(Medicine.id == medicine_id))
    return result.scalars().first()


@router.post("/", response_model=MedicinesResponse)
async def create_medicine(medicine_data: MedicinesCreate,db: AsyncSession = Depends(get_db)):
    medicine = Medicine(**medicine_data.model_dump())
    db.add(medicine)
    await db.commit()
    await db.refresh(medicine)
    return medicine
