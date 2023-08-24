import datetime
from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Boolean, Column, Float, Integer, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from geoalchemy2 import Geography
from geoalchemy2.functions import ST_DWithin, ST_PointFromText


# Database setup
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/postgis_33_sample"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define the POI model based on the database schema
class POI(Base):
    __tablename__ = "mwpoidata"

    mw_poi_id = Column(String, primary_key=True, index=True)
    location_name = Column(String)
    parent_category = Column(String)
    child_category = Column(String)
    grand_child_category = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    street_address = Column(String)
    country = Column(String)
    region_state = Column(String)
    postal_code = Column(String)
    location_type = Column(String)
    location_subtype = Column(String)
    category_place_tags = Column(String)
    website = Column(String)
    time_zone = Column(String)
    peak_hours = Column(String)
    relative_wealth_index = Column(Float)
    verified = Column(Boolean)
    naics_business_code = Column(Integer)
    last_refreshed = Column(TIMESTAMP)
    source = Column(String)
    source_id = Column(String)
    geog = Column(Geography(geometry_type='POINT', srid=4326))


# Define the POI Pydantic model for request and response handling
class POIModel(BaseModel):
    mw_poi_id: str
    location_name: str
    parent_category: Optional[str]
    child_category: Optional[str]
    grand_child_category: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    street_address: Optional[str]
    country: Optional[str]
    region_state: Optional[str]
    postal_code: Optional[str]
    location_type: Optional[str]
    location_subtype: Optional[str]
    category_place_tags: Optional[str]
    website: Optional[str]
    time_zone: Optional[str]
    peak_hours: Optional[str]
    relative_wealth_index: Optional[float]
    verified: Optional[bool]
    naics_business_code: Optional[int]
    last_refreshed: Optional[datetime.datetime]  # you can use datetime.datetime if you want datetime object
    source: Optional[str]
    source_id: Optional[str]
    # geog: Geography  # GeoAlchemy types are not supported in Pydantic

class POISearchModel(BaseModel):
    mw_poi_id: Optional[str] = None
    parent_category: Optional[str] = None
    child_category: Optional[str] = None
    grand_child_category: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def convert_poi_to_dict(poi: POI):
    poi_dict = poi.__dict__
    poi_dict.pop('_sa_instance_state', None)
    return poi_dict

def get_poi_by_id(db: Session, poi_id: str):
    poi = db.query(POI).filter(POI.mw_poi_id == poi_id).first()
    if poi is None:
        raise HTTPException(status_code=404, detail="POI not found")
    return poi

@app.get("/poi/search", response_model=List[POIModel])
def search_poi(
    mw_poi_id: Optional[str] = None,
    parent_category: Optional[str] = None,
    child_category: Optional[str] = None,
    grand_child_category: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    db: Session = Depends(get_db),
):
    query = db.query(POI)

    if mw_poi_id is not None:
        query = query.filter(POI.mw_poi_id == mw_poi_id)

    if parent_category is not None:
        query = query.filter(POI.parent_category == parent_category)

    if child_category is not None:
        query = query.filter(POI.child_category == child_category)

    if grand_child_category is not None:
        query = query.filter(POI.grand_child_category == grand_child_category)

    if latitude is not None and longitude is not None:
        # Convert latitude and longitude to a point
        point = 'SRID=4326;POINT({} {})'.format(longitude, latitude)
        # Find points within 500 meters of the provided point
        query = query.filter(text("ST_DWithin(geog::geography, ST_PointFromText('{}')::geography, 500)".format(point)))

    pois = query.all()

    # Convert SQLAlchemy ORM models to dictionaries
    return [convert_poi_to_dict(poi) for poi in pois]

@app.get("/poi/{poi_id}", response_model=POIModel)
def read_poi(poi_id: str, db: Session = Depends(get_db)):
    poi = get_poi_by_id(db, poi_id)
    return convert_poi_to_dict(poi)

@app.post("/poi/", response_model=POIModel)
def create_poi(poi: POIModel, db: Session = Depends(get_db)):
    db_poi = POI(**poi.dict())
    db.add(db_poi)
    db.commit()
    db.refresh(db_poi)
    return convert_poi_to_dict(db_poi)

@app.put("/poi/{poi_id}", response_model=POIModel)
def update_poi(poi_id: str, poi: POIModel, db: Session = Depends(get_db)):
    db_poi = get_poi_by_id(db, poi_id)
    for key, value in poi.dict().items():
        setattr(db_poi, key, value)
    db.commit()
    db.refresh(db_poi)
    return convert_poi_to_dict(db_poi)

@app.delete("/poi/{poi_id}")
def delete_poi(poi_id: str, db: Session = Depends(get_db)):
    db_poi = get_poi_by_id(db, poi_id)
    db.delete(db_poi)
    db.commit()
    return {"message": "POI deleted"}
