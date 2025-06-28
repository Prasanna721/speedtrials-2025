from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime

class System(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    PWSID: str
    PWS_NAME: str
    PWS_TYPE_CODE: Optional[str] = None
    POPULATION_SERVED_COUNT: Optional[int] = None
    SERVICE_CONNECTIONS_COUNT: Optional[int] = None
    PRIMACY_AGENCY_CODE: Optional[str] = None
    PWS_ACTIVITY_CODE: Optional[str] = None
    ORG_NAME: Optional[str] = None
    ADMIN_NAME: Optional[str] = None
    EMAIL_ADDR: Optional[str] = None
    PHONE_NUMBER: Optional[str] = None
    ADDRESS_LINE1: Optional[str] = None
    CITY_NAME: Optional[str] = None
    STATE_CODE: Optional[str] = None
    ZIP_CODE: Optional[str] = None

class Violation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    PWSID: str
    VIOLATION_ID: str
    VIOLATION_CODE: str
    VIOLATION_DESCRIPTION: Optional[str] = None
    CONTAMINANT_CODE: str
    CONTAMINANT_DESCRIPTION: Optional[str] = None
    NON_COMPL_PER_BEGIN_DATE: Optional[date] = None
    NON_COMPL_PER_END_DATE: Optional[date] = None
    VIOLATION_STATUS: Optional[str] = None
    IS_HEALTH_BASED_IND: Optional[str] = None
    PUBLIC_NOTIFICATION_TIER: Optional[int] = None
    VIOL_MEASURE: Optional[float] = None
    UNIT_OF_MEASURE: Optional[str] = None

class LCRSampleResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    SAMPLE_ID: str
    PWSID: str
    SAMPLING_START_DATE: Optional[date] = None
    SAMPLING_END_DATE: Optional[date] = None
    CONTAMINANT_CODE: str
    RESULT_SIGN_CODE: Optional[str] = None
    SAMPLE_MEASURE: Optional[float] = None
    UNIT_OF_MEASURE: Optional[str] = None

class Facility(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    FACILITY_ID: str
    PWSID: str
    FACILITY_NAME: Optional[str] = None
    STATE_FACILITY_ID: Optional[str] = None
    FACILITY_ACTIVITY_CODE: Optional[str] = None
    FACILITY_TYPE_CODE: Optional[str] = None
    WATER_TYPE_CODE: Optional[str] = None
    IS_SOURCE_IND: Optional[str] = None

class SiteVisit(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    VISIT_ID: str
    PWSID: str
    VISIT_DATE: Optional[date] = None
    AGENCY_TYPE_CODE: Optional[str] = None
    VISIT_REASON_CODE: Optional[str] = None
    TREATMENT_EVAL_CODE: Optional[str] = None
    DISTRIBUTION_EVAL_CODE: Optional[str] = None
    COMPLIANCE_EVAL_CODE: Optional[str] = None

class SystemSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    system_info: System
    open_health_violations_count: int
    resolved_violations_count: int
    last_site_visit_date: Optional[date] = None

class SystemSearchResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    PWSID: str
    PWS_NAME: str
    CITY_NAME: Optional[str] = None
    COUNTY_SERVED: Optional[str] = Field(None, description="Primary county served by the water system.")
    POPULATION_SERVED_COUNT: Optional[int] = None