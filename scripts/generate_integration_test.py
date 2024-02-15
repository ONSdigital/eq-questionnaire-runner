from typing import TextIO
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import Playwright, Request, sync_playwright
from structlog import get_logger

logger = get_logger()


previous_request_method = ""
survey_start = True
schema_name = ""

LAUNCHER_ROOT_URL = "http://localhost:8000"
RUNNER_ROOT_URL = "http://localhost:5000"
SPACE_INDENTATION = " " * 8


# pylint: disable=global-variable-not-assigned
def process_runner_request(request: Request) -> None:
    global schema_name

    with open(f"{schema_name}.py", "a", encoding="utf-8") as file:
        if request.method == "POST":
            process_post(request, file)

        elif request.method == "GET":
            process_get(request, file)


# pylint: disable=global-statement
def process_post(request: Request, file: TextIO) -> None:
    global previous_request_method

    previous_request_method = "POST"

    # Playwright Request.post_data comes formatted like a URL query string, so can be parsed
    post_data = parse_qs(request.post_data)
    del post_data["csrf_token"]

    items: dict[str, str | list[str]] = {}
    for answer_id, answer_values in post_data.items():
        if len(answer_values) > 1:  # Handle multiple values in list
            items[answer_id] = answer_values
        elif len(answer_values) == 1:
            items[answer_id] = answer_values[0]  # A single item in list

    if items:
        file.write(generate_post_code_snippet(items))
    else:
        # Empty post for no answers and non question pages
        file.write(generate_post_code_snippet())


# pylint: disable=global-statement
def process_get(request: Request, file: TextIO) -> None:
    global previous_request_method
    global survey_start

    if (  # Logic to filter out the session and root questionnaire GET requests at the start
        previous_request_method == "GET"
        and "session?token" not in request.url
        and request.url != f"{RUNNER_ROOT_URL}/questionnaire/"
    ):
        path = urlparse(request.url).path
        file.write(generate_get_code_snippet(path))

    if not survey_start:
        previous_request_method = request.method

    if (
        previous_request_method == ""
        and survey_start
        and request.url == f"{RUNNER_ROOT_URL}/questionnaire/"
    ):
        survey_start = False


def process_launcher_request(request: Request) -> None:
    global schema_name

    if request.method == "GET":
        if survey_start:
            # start of journey, so create a skeleton file using the schema name
            schema_name = parse_qs(request.url)["schema_name"][0]
            with open(f"{schema_name}.py", "w", encoding="utf-8") as file:
                file.write(
                    f"from tests.integration.integration_test_case import IntegrationTestCase\n\n\n"
                    f'class {schema_name.title().replace("_", "")}(IntegrationTestCase):\n'
                    f"    def {schema_name}(self):\n"
                    f'        self.launchSurvey("{schema_name}")'
                )
                logger.info(f"self.launchSurvey('{schema_name}')")
        else:
            # capture launcher urls for sign-out, save etc
            with open(f"{schema_name}.py", "a", encoding="utf-8") as file:
                path = urlparse(request.url).path
                file.write(generate_get_code_snippet(path))


def generate_post_code_snippet(post_data: dict | str | None = "") -> str:
    snippet = f"self.post({post_data})"
    logger.info(snippet)

    return f"\n{SPACE_INDENTATION}{snippet}"


def generate_get_code_snippet(url_path: str) -> str:
    snippet = f'self.get("{url_path}")'
    logger.info(snippet)

    return f"\n{SPACE_INDENTATION}{snippet}"


def request_handler(request: Request) -> None:
    if LAUNCHER_ROOT_URL in request.url:
        process_launcher_request(request)
    elif RUNNER_ROOT_URL in request.url:
        process_runner_request(request)


def run(pw: Playwright) -> None:
    chromium = pw.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(LAUNCHER_ROOT_URL)

    page.on("request", request_handler)

    input(
        ""
        "Script is paused. Start navigating through the browser for the journey & press Enter when finished to capture the output and add into a test file\n"
        ""
    )
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
