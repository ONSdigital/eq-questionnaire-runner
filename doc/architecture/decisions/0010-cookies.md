# 10. Cookies

## Context

We should be clear about what we store in the session cookie and why.

We store a number of properties in the `session` cookie:

| Property | Description |
|----------|-------------|
| eq-session-id | The session identifier |
| user_ik  | The user half of the encryption key |
| csrf_token | The CSRF token (generated for each request) |
| theme | Survey theme from the schema (`theme`) |
| survey_title | Survey title from the schema (`title`) |
| expires_in | Session timeout in seconds from schema (`session_timeout_in_seconds`) or application default (`EQ_SESSION_TIMEOUT_SECONDS`) |
| account_service_url | The link back to the launch service. Used on the signed out and session expired pages. From metadata claims (`account_service_url`) |
| account_service_log_out_url | The The URL to redirect to on signout. From metadata claims (`account_service_log_out_url`) |

- The CSRF token changes per request, meaning that the session cookie is set for most requests.

- Language is accessed from the server-side session via the Babel `get_locale` method. This means it's only available if the user has a valid session; when the session has timed out, screens are not in the appropriate language.

## Decision

- Continue using the session cookie for properties that are set on sign-in as they are relevant to the current session. Storing them in the cookie rather than the server-side session means that they are still accessible after the server-side session times out.
- Store `schema_name` or `schema_url` in the cookie and remove schema properties i.e. `theme`, `survey_title` and `expires_in`. This simplifies runner code as we will always be able to load a schema for any request (if they have successfully launched a questionnaire), and it provides a way to use other schema properties without adding to the cookie.
- The session cookie will contain:

  | Property | Description |
  |----------|-------------|
  | eq_session_id | The session identifier |
  | user_ik  | The user half of the encryption key |
  | csrf_token | The CSRF token (generated for each request) |
  | account_service_url | The link back to the launch service |
  | account_service_log_out_url | The The URL to redirect to on signout |
  | schema_name | The schema filename |
  | schema_url | A URL to a schema |

- The `session` cookie should be set once on successful authentication. To enable this, we will review our CSRF token implementation - one per session or a separate cookie.

- Set `language` in a cookie, so it’s not lost as a preference when there is no server-side session. This will be stored in a separate cookie as the user can change it.

- Any future user preferences that need to be remembered will be stored in separate named cookies.

## Additional information

- An `ons_cookie_policy` cookie is set in the front end and is used to enable/disable Google tracking.
