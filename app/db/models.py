from typing import List

from sqlalchemy import BigInteger, Text, Numeric, VARCHAR, String, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    ...


organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column("organization_id", BigInteger, ForeignKey("organizations.id", ondelete='CASCADE'), primary_key=True),
    Column("activity_id", BigInteger, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True)
)


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    building_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("buildings.id", ondelete="SET NULL"))

    building: Mapped["Building"] = relationship("Building", back_populates="organizations")
    phones: Mapped[List["Phone"]] = relationship("Phone", back_populates="organization", cascade="all, delete-orphan")
    activities: Mapped[List["Activity"]] = relationship("Activity", secondary=organization_activities, back_populates="organizations")


class Phone(Base):
    __tablename__ = "phones"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    organization_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("organizations.id", ondelete="CASCADE")) # foreign key
    phone: Mapped[str] = mapped_column(VARCHAR(16), nullable=False, unique=True, index=True)

    organization: Mapped["Organization"] = relationship(back_populates="phones")


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[float] = mapped_column(Numeric, nullable=False)
    longitude: Mapped[float] = mapped_column(Numeric, nullable=False)

    organizations: Mapped[List["Organization"]] = relationship("Organization", back_populates="building")


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False, unique=True)

    organizations: Mapped[List["Organization"]] = relationship("Organization", secondary=organization_activities, back_populates="activities")
    ancestors: Mapped[list["ActivityClosure"]] = relationship("ActivityClosure", foreign_keys="ActivityClosure.descendant_id", back_populates="descendant")
    descendants: Mapped[list["ActivityClosure"]] = relationship("ActivityClosure", foreign_keys="ActivityClosure.ancestor_id", back_populates="ancestor")


class ActivityClosure(Base):
    __tablename__ = "activity_closure"

    ancestor_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True)
    descendant_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True)
    depth: Mapped[int] = mapped_column(Integer, nullable=False)

    ancestor: Mapped["Activity"] = relationship("Activity", foreign_keys=[ancestor_id], back_populates="descendants")
    descendant: Mapped["Activity"] = relationship("Activity", foreign_keys=[descendant_id], back_populates="ancestors")

