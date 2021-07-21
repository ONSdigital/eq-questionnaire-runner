from flask_babel import lazy_gettext

# Set up default error and warning messages
# lazy_gettext is used as the string needs to be resolved at runtime
# for translations to work.

# NOTE: `%` style string formatting is used for compatibility with WTForms default field
# validators - using `.format` for non-WTForm field validation would introduce
# inconsistency.
error_messages = {
    "MANDATORY_QUESTION": lazy_gettext("Enter an answer"),
    "MANDATORY_TEXTFIELD": lazy_gettext("Enter an answer"),
    "MANDATORY_NUMBER": lazy_gettext("Enter an answer"),
    "MANDATORY_TEXTAREA": lazy_gettext("Enter an answer"),
    "MANDATORY_RADIO": lazy_gettext(
        'Select an answer <span class="u-vh">to ‘%(question_title)s’</span>'
    ),
    "MANDATORY_DROPDOWN": lazy_gettext("Select an answer"),
    "MANDATORY_CHECKBOX": lazy_gettext(
        'Select at least one answer <span class="u-vh">to ‘%(question_title)s’</span>'
    ),
    "MANDATORY_DATE": lazy_gettext("Enter a date"),
    "MANDATORY_ADDRESS": lazy_gettext("Enter an address"),
    "MANDATORY_DURATION": lazy_gettext("Enter a duration"),
    "MANDATORY_EMAIL": lazy_gettext("Enter an email address"),
    "MANDATORY_MOBILE_NUMBER": lazy_gettext("Enter a UK mobile number"),
    "NUMBER_TOO_SMALL": lazy_gettext("Enter an answer more than or equal to %(min)s"),
    "NUMBER_TOO_LARGE": lazy_gettext("Enter an answer less than or equal to %(max)s"),
    "NUMBER_TOO_SMALL_EXCLUSIVE": lazy_gettext("Enter an answer more than %(min)s"),
    "NUMBER_TOO_LARGE_EXCLUSIVE": lazy_gettext("Enter an answer less than %(max)s"),
    "TOTAL_SUM_NOT_EQUALS": lazy_gettext("Enter answers that add up to %(total)s"),
    "TOTAL_SUM_NOT_LESS_THAN_OR_EQUALS": lazy_gettext(
        "Enter answers that add up to or are less than %(total)s"
    ),
    "TOTAL_SUM_NOT_LESS_THAN": lazy_gettext(
        "Enter answers that add up to less than %(total)s"
    ),
    "TOTAL_SUM_NOT_GREATER_THAN": lazy_gettext(
        "Enter answers that add up to greater than %(total)s"
    ),
    "TOTAL_SUM_NOT_GREATER_THAN_OR_EQUALS": lazy_gettext(
        "Enter answers that add up to or are greater than %(total)s"
    ),
    "INVALID_EMAIL_FORMAT": lazy_gettext(
        "Enter an email address in a valid format, for example name@example.com"
    ),
    "INVALID_NUMBER": lazy_gettext("Enter a number"),
    "INVALID_INTEGER": lazy_gettext("Enter a whole number"),
    "INVALID_DECIMAL": lazy_gettext("Enter a number rounded to %(max)d decimal places"),
    "MAX_LENGTH_EXCEEDED": lazy_gettext(
        "You have entered too many characters. Enter up to %(max)d characters"
    ),
    "INVALID_DATE": lazy_gettext("Enter a valid date"),
    "INVALID_DATE_RANGE": lazy_gettext(
        "Enter a 'period to' date later than the 'period from' date"
    ),
    "INVALID_DURATION": lazy_gettext("Enter a valid duration"),
    "INVALID_MOBILE_NUMBER": lazy_gettext(
        "Enter a UK mobile number in a valid format, for example, 07700 900345 or +44 7700 900345"
    ),
    "DATE_PERIOD_TOO_SMALL": lazy_gettext(
        "Enter a reporting period greater than or equal to %(min)s"
    ),
    "DATE_PERIOD_TOO_LARGE": lazy_gettext(
        "Enter a reporting period less than or equal to %(max)s"
    ),
    "SINGLE_DATE_PERIOD_TOO_EARLY": lazy_gettext("Enter a date after %(min)s"),
    "SINGLE_DATE_PERIOD_TOO_LATE": lazy_gettext("Enter a date before %(max)s"),
    "MUTUALLY_EXCLUSIVE": lazy_gettext("Remove an answer"),
}
