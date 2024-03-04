from typing import IO, Dict
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import Playwright, Request, sync_playwright
from structlog import get_logger

logger = get_logger()

LAUNCHER_ROOT_URL = "http://localhost:8000"
RUNNER_ROOT_URL = "http://localhost:5000"
TEST_TEMPLATE = """from tests.integration.integration_test_case import IntegrationTestCase


class {class_name}(IntegrationTestCase):
    def {function_name}(self):
        self.launchSurvey("{schema_name}")
"""

survey_journey: Dict[str, str | bool | None] = {
    "previous_request_method": None,
    "started": True,
    "schema_name": None,
}

output: Dict[str, str] = {"file_name": ""}


def process_runner_request(request: Request) -> None:
    with open(output["file_name"], "a", encoding="utf-8") as file:
        if request.method == "POST":
            process_post(request, file)

        elif request.method == "GET":
            process_get(request, file)


def process_post(request: Request, file: IO) -> None:
    survey_journey["previous_request_method"] = "POST"

    # Playwright Request.post_data comes formatted like a URL query string, so can be parsed
    post_data = parse_qs(request.post_data)
    del post_data["csrf_token"]

    items = {
        answer_id: answer_values[0] if len(answer_values) == 1 else answer_values
        for answer_id, answer_values in post_data.items()
    }

    # Post items, or empty post for no answers/non-question pages
    file.write(generate_method_request(method="post", data=items or ""))


def process_get(request: Request, file: IO) -> None:
    if (  # Logic to filter out the session and root questionnaire GET requests at the start
        survey_journey["previous_request_method"] == "GET"
        and "session?token" not in request.url
        and request.url != f"{RUNNER_ROOT_URL}/questionnaire/"
    ):
        path = f'"{urlparse(request.url).path}"'
        file.write(generate_method_request(method="get", data=path))

    if not survey_journey["started"]:
        survey_journey["previous_request_method"] = request.method

    if (
        not survey_journey["previous_request_method"]
        and survey_journey["started"]
        and request.url == f"{RUNNER_ROOT_URL}/questionnaire/"
    ):
        survey_journey["started"] = False


def process_launcher_request(request: Request) -> None:
    if request.method == "GET":
        if survey_journey["started"]:
            # start of journey, so create a skeleton file using the schema name
            survey_journey["schema_name"] = parse_qs(request.url)["schema_name"][0]
            output[
                "file_name"
            ] = f"./scripts/{survey_journey['schema_name']}.py"

            with open(output["file_name"], "w", encoding="utf-8") as file:
                # Type ignore: schema_name is taken as string from query string
                class_name = survey_journey["schema_name"].title().replace("_", "")  # type: ignore
                file.write(
                    TEST_TEMPLATE.format(
                        class_name=class_name,
                        function_name=survey_journey["schema_name"],
                        schema_name=survey_journey["schema_name"],
                    )
                )
                logger.info(request)
        else:
            # capture launcher urls for sign-out, save etc
            with open(output["file_name"], "a", encoding="utf-8") as file:
                path = f'"{urlparse(request.url).path}"'
                file.write(generate_method_request(method="get", data=path))


def generate_method_request(*, method: str, data: dict | str | None = None) -> str:
    snippet = f"self.{method}({data})"
    logger.info(f'Generating Runner code snippet for HTTP request: "{snippet}"')
    return f"\n        {snippet}"


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

    input("Script is paused. Start navigating through the browser for the journey & press Enter when finished to capture"
          " the output and add into a test file\n")
    browser.close()
    logger.info(
        "Integration test generated successfully",
        integration_test_file=output["file_name"],
    )


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
