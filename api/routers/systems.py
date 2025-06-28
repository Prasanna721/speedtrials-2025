from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api",
    tags=["systems"],
)

@router.get("/search", response_model=List[schemas.SystemSearchResult])
def search_systems(zip_code: str = Query(..., min_length=5, max_length=5, regex="^[0-9]{5}$"), db: Session = Depends(get_db)):
    systems = crud.search_systems_by_zip(db, zip_code=zip_code)
    if not systems:
        raise HTTPException(status_code=404, detail="No active water systems found for the provided ZIP code.")
    return systems

@router.get("/system/{pwsid}", response_model=schemas.System)
def read_system(pwsid: str, db: Session = Depends(get_db)):
    db_system = crud.get_system_by_pwsid(db, pwsid=pwsid)
    if db_system is None:
        raise HTTPException(status_code=404, detail="System not found")
    return db_system

@router.get("/system/{pwsid}/summary", response_model=schemas.SystemSummary)
def read_system_summary(pwsid: str, db: Session = Depends(get_db)):
    summary = crud.get_system_summary(db, pwsid=pwsid)
    if summary is None:
        raise HTTPException(status_code=404, detail="System not found")
    return summary

@router.get("/system/{pwsid}/violations", response_model=List[schemas.Violation])
def read_system_violations(pwsid: str, db: Session = Depends(get_db)):
    violations = crud.get_violations_by_pwsid(db, pwsid=pwsid)
    return violations

@router.get("/system/{pwsid}/lcr", response_model=List[schemas.LCRSampleResult])
def read_system_lcr_samples(pwsid: str, db: Session = Depends(get_db)):
    samples = crud.get_lcr_samples_by_pwsid(db, pwsid=pwsid)
    return samples
    
@router.get("/system/{pwsid}/facilities", response_model=List[schemas.Facility])
def read_system_facilities(pwsid: str, db: Session = Depends(get_db)):
    facilities = crud.get_facilities_by_pwsid(db, pwsid=pwsid)
    return facilities

@router.get("/system/{pwsid}/site-visits", response_model=List[schemas.SiteVisit])
def read_system_site_visits(pwsid: str, db: Session = Depends(get_db)):
    visits = crud.get_site_visits_by_pwsid(db, pwsid=pwsid)
    return visits