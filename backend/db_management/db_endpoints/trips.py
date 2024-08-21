"""Set API routes for CRUD operations with trips."""

import datetime
import pandas as pd
from db_management.db.database import get_db
from db_management.db.database_models import TripList
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from db_management.schemas.pydantic_schemas import Trip

router = APIRouter()

@router.post("/register_trip", response_model=Trip)
def register_trip(item: Trip, db: Session = Depends(get_db)):  # noqa: ANN201, B008
    """Register new trip."""
    new_trip = TripList(
        dt_created=item.dt_created,
        category=item.category,
        distance=item.distance,
        total_cost=item.total_cost,
        user_id=item.user_id,
    )
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip


@router.get("/get_trip", response_model= Trip | None)  
def get_trip(trip_date: datetime.datetime, db: Session = Depends(get_db)):  # noqa: ANN201, B008
    """Get one concrete trip."""
    trip_date = trip_date.strftime("%Y-%m-%d %H:%M")
    trip = db.query(TripList).filter_by(dt_created=trip_date).first()
    if trip:
        return trip
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Trip not found",
    )


@router.get("/show_total_money_spent")
def show_total_money_spent(username: str, 
                           trip_date: datetime.datetime | None = None, 
                           db: Session = Depends(get_db)) -> str:  # noqa: ANN201, B008
    """Show how much is spent on trips."""
    query = f"SELECT SUM(total_cost) FROM (user_account JOIN trips ON user_account.id=trips.user_id) as t WHERE t.username='{username}' "
    if not trip_date:
        total_cost=db.execute(text(query)).first()
    else:
        trip_date = trip_date.strftime("%Y-%m-%d %H:%M")
        tail = f"AND t.dt_created='{trip_date}'"
        query = query + tail
        total_cost=db.execute(text(query)).first()
    return f"Spent {total_cost[0]} USD"


@router.get("/get_trips_by_user") 
def get_trips_by_user(username: str, db: Session = Depends(get_db)):  # noqa: ANN201, B008
    """Get trips of user."""
    query = text(f"SELECT t.username, t.category, t.dt_created, t.total_cost, t.distance FROM \
        (trips JOIN user_account ON trips.user_id=user_account.id) AS t WHERE t.username='{username}'")  # noqa: E501, S608
    user_trips = db.execute(query).all()
    if user_trips:
        res = pd.DataFrame(user_trips).to_dict(orient="records")
        return res
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Trips not found",
    )


@router.patch("/change_trip_category", response_model=Trip)
def change_trip_category(item: Trip, db: Session = Depends(get_db)):  # noqa: ANN201, B008
    """Change trip category."""
    if not db.query(TripList).filter_by(dt_created=item.dt_created).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trip not found",
        )
    trip = db.query(TripList).filter_by(dt_created=item.dt_created).first()
    trip.category = item.category
    db.commit()
    return trip