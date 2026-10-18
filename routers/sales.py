from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.database import get_db
from database.models import Medicine, Sale
from schemas.schemas import SaleCreate, SaleResponse


router = APIRouter(prefix="/sales", tags=["Продажи"])


@router.get("/", response_model=list[SaleResponse])
async def get_sales(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sale).order_by(Sale.id.desc()))
    return result.scalars().all()


@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(sale_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sale).where(Sale.id == sale_id)  )
    return result.scalars().first()


@router.post("/", response_model=SaleResponse)
async def create_sale(sale_data: SaleCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Medicine).where(Medicine.id == sale_data.medicine_id))
    medicine = result.scalars().first()

    if medicine is None:
        return {"message": "Лекарство не найдено"}

    if medicine.stock < sale_data.quantity:
        return {"message": "Недостаточно лекарства на складе"}

    medicine.stock -= sale_data.quantity

    sale = Sale(medicine_id=sale_data.medicine_id, quantity=sale_data.quantity)

    db.add(sale)
    await db.commit()
    await db.refresh(sale)

    return sale
