from sqlalchemy import Column, String, Integer, Numeric, Boolean, DateTime, func, ForeignKey
from database.database import Base

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    prescription = Column(Boolean, default=False)
    stock = Column(Integer, default=0, nullable=False)


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    sold_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)