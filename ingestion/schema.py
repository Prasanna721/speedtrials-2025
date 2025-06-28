TABLE_SCHEMAS = {
    "events_milestones": {
        "file_name": "SDWA_EVENTS_MILESTONES.csv",
        "date_columns": ["EVENT_END_DATE", "EVENT_ACTUAL_DATE", "FIRST_REPORTED_DATE", "LAST_REPORTED_DATE"],
    },
    "facilities": {
        "file_name": "SDWA_FACILITIES.csv",
        "date_columns": ["FACILITY_DEACTIVATION_DATE", "FIRST_REPORTED_DATE", "LAST_REPORTED_DATE"],
    },
    "geographic_areas": {
        "file_name": "SDWA_GEOGRAPHIC_AREAS.csv",
        "date_columns": ["LAST_REPORTED_DATE"],
    },
    "lcr_samples": {
        "file_name": "SDWA_LCR_SAMPLES.csv",
        "date_columns": ["SAMPLING_END_DATE", "SAMPLING_START_DATE", "SAMPLE_FIRST_REPORTED_DATE", "SAMPLE_LAST_REPORTED_DATE", "SAR_FIRST_REPORTED_DATE", "SAR_LAST_REPORTED_DATE"],
    },
    "pn_violation_assoc": {
        "file_name": "SDWA_PN_VIOLATION_ASSOC.csv",
        "date_columns": ["NON_COMPL_PER_BEGIN_DATE", "NON_COMPL_PER_END_DATE", "FIRST_REPORTED_DATE", "LAST_REPORTED_DATE"],
    },
    "pub_water_systems": {
        "file_name": "SDWA_PUB_WATER_SYSTEMS.csv",
        "date_columns": ["PWS_DEACTIVATION_DATE", "FIRST_REPORTED_DATE", "LAST_REPORTED_DATE", "SOURCE_PROTECTION_BEGIN_DATE", "OUTSTANDING_PERFORM_BEGIN_DATE", "REDUCED_MONITORING_BEGIN_DATE", "REDUCED_MONITORING_END_DATE"],
    },
    "ref_code_values": {
        "file_name": "SDWA_REF_CODE_VALUES.csv",
        "date_columns": [],
    },
    "service_areas": {
        "file_name": "SDWA_SERVICE_AREAS.csv",
        "date_columns": ["FIRST_REPORTED_DATE", "LAST_REPORTED_DATE"],
    },
    "site_visits": {
        "file_name": "SDWA_SITE_VISITS.csv",
        "date_columns": ["VISIT_DATE", "FIRST_REPORTED_DATE", "LAST_REPORTED_DATE"],
    },
    "violations_enforcement": {
        "file_name": "SDWA_VIOLATIONS_ENFORCEMENT.csv",
        "date_columns": ["NON_COMPL_PER_BEGIN_DATE", "NON_COMPL_PER_END_DATE", "CALCULATED_RTC_DATE", "VIOL_FIRST_REPORTED_DATE", "VIOL_LAST_REPORTED_DATE", "ENFORCEMENT_DATE", "ENF_FIRST_REPORTED_DATE", "ENF_LAST_REPORTED_DATE"],
    },
}

MATERIALIZED_VIEW_QUERY = """
CREATE TABLE clean_violations AS
SELECT
    v.PWSID,
    pws.PWS_NAME,
    pws.POPULATION_SERVED_COUNT,
    pws.PWS_TYPE_CODE,
    pws.CITY_NAME,
    v.VIOLATION_ID,
    v.VIOLATION_CODE,
    ref_viol.VALUE_DESCRIPTION AS VIOLATION_DESCRIPTION,
    v.CONTAMINANT_CODE,
    ref_cont.VALUE_DESCRIPTION AS CONTAMINANT_DESCRIPTION,
    v.NON_COMPL_PER_BEGIN_DATE,
    v.NON_COMPL_PER_END_DATE,
    v.VIOLATION_STATUS,
    v.IS_HEALTH_BASED_IND,
    v.PUBLIC_NOTIFICATION_TIER,
    v.VIOL_MEASURE,
    v.UNIT_OF_MEASURE,
    v.FEDERAL_MCL,
    v.STATE_MCL
FROM
    violations_enforcement v
LEFT JOIN
    pub_water_systems pws ON v.PWSID = pws.PWSID
LEFT JOIN
    ref_code_values ref_viol ON v.VIOLATION_CODE = ref_viol.VALUE_CODE AND ref_viol.VALUE_TYPE = 'VIOLATION_CODE'
LEFT JOIN
    ref_code_values ref_cont ON v.CONTAMINANT_CODE = ref_cont.VALUE_CODE AND ref_cont.VALUE_TYPE = 'CONTAMINANT_CODE';
"""