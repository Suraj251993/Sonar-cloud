from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, String
from pydantic import BaseModel
from typing import List
from sqlalchemy.sql import func
import haversine as hs
from haversine import Unit

app = FastAPI()

DATABASE_URL = "mysql+pymysql://root:password123.@localhost/mydatabase"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

class MW(Base):
    _tablename_ = "mw"

    id = Column(Float, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    location_name = Column(String)
    street_address = Column(String)
    country = Column(String)  # Add this column

class Point(BaseModel):
    latitude: float
    longitude: float
    location_name: str
    street_address: str
    country: str  # Add this field

class PointsResponse(BaseModel):
    points: List[Point]

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def get_points_nearby(latitude: float, longitude: float, db: Session = Depends(get_db)):
    points = db.execute(
        text(
            """
            SELECT latitude, longitude, location_name, street_address, country
            FROM mw
            WHERE ST_Distance(
                POINT(latitude, longitude),
                POINT(:latitude, :longitude)
            ) * 111195.0 < 500
            """
        ),
        {"latitude": latitude, "longitude": longitude},
    )

    point_list = [
        Point(
            latitude=point[0],
            longitude=point[1],
            location_name=point[2],
            street_address=point[3],
            country=point[4],
        )
        for point in points
    ]

    nearby_points = []
    for point in point_list:
        haversine_distance = hs.haversine(
            (latitude, longitude),
            (point.latitude, point.longitude),
            unit=Unit.METERS
        )
        
        if haversine_distance < 500:  # Check if the distance is within 500 meters
            nearby_points.append(point)

    return PointsResponse(points=nearby_points)