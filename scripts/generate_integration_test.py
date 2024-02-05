from urllib.parse import parse_qs

from playwright.sync_api import Playwright, Request, sync_playwright
from structlog import get_logger

logger = get_logger()


previous_request_method = ""
survey_start = True
schema_name = ""

LAUNCHER_ROOT_URL = "http://localhost:8000/"
RUNNER_ROOT_URL = "http://localhost:5000"


# pylint: disable=global-variable-not-assigned
def process_request(request):
    global schema_name

    with open(f"{schema_name}.py", "a", encoding="utf-8") as file:
        if request.method == "POST":
            process_post(request, file)

        elif request.method == "GET":
            process_get(request, file)


# pylint: disable=global-statement
def process_post(request, file):
    global previous_request_method
    global survey_start
    global schema_name

    previous_request_method = "POST"

    query_string = parse_qs(request.post_data, keep_blank_values=True)
    del query_string["csrf_token"]

    if not query_string.items():
        file.write("\n        self.post()")
        logger.info("self.post()")
        return

    items = {}
    for answer_id, answer_values in query_string.items():
        if any(
            answer_values
        ):  # Only populate items if non-empty answers dict in request
            if len(answer_values) > 1:  # Handle multiple values in list
                items[answer_id] = answer_values
            elif len(answer_values) == 1:
                items[answer_id] = answer_values[0]  # A single item in list

    if len(items) > 0:
        file.write(f"\n        self.post({items})")
        logger.info(f"self.post({items})")
        return

    if len(items) == 0:  # Empty post for no answers and non question pages
        file.write("\n        self.post()")
        logger.info("self.post()")


# pylint: disable=global-statement
def process_get(request, file):
    global previous_request_method
    global survey_start
    global schema_name

    if (  # Logic to filter out the session and root questionnaire GET requests at the start
        previous_request_method == "GET"
        and "session?token" not in request.url
        and request.url != "http://localhost:5000/questionnaire/"
    ):
        path = request.url.lstrip(RUNNER_ROOT_URL)
        file.write(f'\n        self.get("/{path}")')
        logger.info(f'self.get("/{path}")')

    if not survey_start:
        previous_request_method = request.method

    if (
        previous_request_method == ""
        and survey_start
        and request.url == "http://localhost:5000/questionnaire/"
    ):
        survey_start = False


def request_handler(request: Request):
    global schema_name
    matching_url_found = RUNNER_ROOT_URL in request.url

    if matching_url_found:
        process_request(request)
    elif request.url != LAUNCHER_ROOT_URL and LAUNCHER_ROOT_URL in request.url:
        schema_name = request.url.split("=")[-1]
        with open(f"{schema_name}.py", "w", encoding="utf-8") as file:
            file.write(
                f'from tests.integration.integration_test_case import IntegrationTestCase\n\n\nclass {schema_name.title().replace("_", "")}'
                f'(IntegrationTestCase):\n    def {schema_name}(self):\n        self.launchSurvey("{request.url.split("=")[-1]}")'
            )
            logger.info(f'self.launchSurvey("{request.url.split("=")[-1]}")')


def run(pl: Playwright):
    chromium = pl.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("http://localhost:8000/")

    page.on("request", request_handler)

    input(
        "Pause script. Start navigating through the browser for journey & press enter when finished to capture the output and add into a test\n"
    )
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
