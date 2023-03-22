from enum import Enum


class SurveyType(Enum):
    BUSINESS = "business"
    SOCIAL = "social"
    DEFAULT = "default"
    HEALTH = "health"
    NORTHERN_IRELAND = "northernireland"
    DBT = "dbt"
    DBT_NI = "dbt-ni"
    DBT_DSIT = "dbt-dsit"
    DBT_DSIT_NI = "dbt-dsit-ni"
    ORR = "orr"
    CENSUS = "census"
    CENSUS_NISRA = "census-nisra"
