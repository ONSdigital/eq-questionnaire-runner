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
    DESNZ = "desnz"
    DESNZ_NI = "desnz-ni"
    UKHSA_ONS = "ukhsa-ons"
    ONS_NHS = "ons-nhs"
