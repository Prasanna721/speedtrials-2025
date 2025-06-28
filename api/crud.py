from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional

from . import schemas

def search_systems_by_zip(db: Session, zip_code: str) -> List[dict]:
    query = text("""
        SELECT
            pws.PWSID,
            pws.PWS_NAME,
            pws.CITY_NAME,
            pws.POPULATION_SERVED_COUNT,
            (
                SELECT geo.COUNTY_SERVED
                FROM geographic_areas AS geo
                WHERE geo.PWSID = pws.PWSID
                  AND geo.AREA_TYPE_CODE = 'CN'
                LIMIT 1
            ) as COUNTY_SERVED
        FROM
            pub_water_systems AS pws
        WHERE
            pws.PWS_ACTIVITY_CODE = 'A' AND
            pws.ZIP_CODE LIKE :zip_code || '%'
        GROUP BY
            pws.PWSID
        ORDER BY
            pws.POPULATION_SERVED_COUNT DESC
        LIMIT 50;
    """)
    result = db.execute(query, {"zip_code": zip_code}).mappings().all()
    return result

def get_system_by_pwsid(db: Session, pwsid: str) -> Optional[dict]:
    query = text("""
        SELECT * FROM pub_water_systems WHERE PWSID = :pwsid LIMIT 1
    """)
    result = db.execute(query, {"pwsid": pwsid}).mappings().first()
    return result

def get_violations_by_pwsid(db: Session, pwsid: str) -> List[dict]:
    query = text("""
        SELECT * FROM clean_violations 
        WHERE PWSID = :pwsid 
        ORDER BY NON_COMPL_PER_BEGIN_DATE DESC
    """)
    result = db.execute(query, {"pwsid": pwsid}).mappings().all()
    return result

def get_lcr_samples_by_pwsid(db: Session, pwsid: str) -> List[dict]:
    query = text("""
        SELECT * FROM lcr_samples 
        WHERE PWSID = :pwsid 
        ORDER BY SAMPLING_END_DATE DESC
    """)
    result = db.execute(query, {"pwsid": pwsid}).mappings().all()
    return result

def get_facilities_by_pwsid(db: Session, pwsid: str) -> List[dict]:
    query = text("""
        SELECT * FROM facilities
        WHERE PWSID = :pwsid AND FACILITY_ACTIVITY_CODE = 'A'
        ORDER BY FACILITY_TYPE_CODE
    """)
    result = db.execute(query, {"pwsid": pwsid}).mappings().all()
    return result

def get_site_visits_by_pwsid(db: Session, pwsid: str) -> List[dict]:
    query = text("""
        SELECT * FROM site_visits
        WHERE PWSID = :pwsid
        ORDER BY VISIT_DATE DESC
    """)
    result = db.execute(query, {"pwsid": pwsid}).mappings().all()
    return result

def get_system_summary(db: Session, pwsid: str) -> Optional[dict]:
    system_info = get_system_by_pwsid(db, pwsid)
    if not system_info:
        return None

    query = text("""
        SELECT
            (SELECT COUNT(*) FROM clean_violations WHERE PWSID = :pwsid AND VIOLATION_STATUS != 'Resolved' AND IS_HEALTH_BASED_IND = 'Y') as open_health_violations_count,
            (SELECT COUNT(*) FROM clean_violations WHERE PWSID = :pwsid AND VIOLATION_STATUS = 'Resolved') as resolved_violations_count,
            (SELECT MAX(VISIT_DATE) FROM site_visits WHERE PWSID = :pwsid) as last_site_visit_date
    """)
    summary_stats = db.execute(query, {"pwsid": pwsid}).mappings().first()
    
    return {
        "system_info": system_info,
        **summary_stats
    }