#!/usr/bin/env python3
import argparse
import difflib
import logging
import subprocess
import sys
import tempfile

import coloredlogs

logger = logging.getLogger(__name__)

coloredlogs.install(level="DEBUG", logger=logger, fmt="%(message)s")


def get_template_content(filename, ignore_context=False):
    line_beginnings_to_ignore = ['"POT-Creation-Date']

    if ignore_context:
        line_beginnings_to_ignore += ["#:"]

    with open(filename, encoding="UTF-8") as file:
        return list(
            filter(
                lambda line: all(
                    not line.startswith(param) for param in line_beginnings_to_ignore
                ),
                file.readlines(),
            )
        )


def print_filename_results(filename, success=True):
    if success:
        logger.debug("%s - NO CHANGES", filename)
    else:
        logger.error("%s - CHANGES FOUND", filename)


def build_static_template(output_filepath):
    subprocess.run(
        [
            "poetry",
            "run",
            "pybabel",
            "extract",
            "-F",
            "babel.cfg",
            "-k",
            "lazy_gettext",
            "-k",
            "gettext",
            "-o",
            output_filepath,
            ".",
        ],
        check=False,
    )


def compare_files(source_dir, target_dir, filename):
    source_file = f"{source_dir}/{filename}"
    target_file = f"{target_dir}/{filename}"

    source_contents = get_template_content(source_file, ignore_context=True)
    target_contents = get_template_content(target_file, ignore_context=True)

    contents_match = source_contents == target_contents

    if not contents_match:
        diff_results = difflib.unified_diff(
            source_contents, target_contents, fromfile=source_file, tofile=target_file
        )
        logger.info("".join(list(diff_results)))

    print_filename_results(f"{source_file}", contents_match)

    return contents_match


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract translation templates from runner"
    )
    parser.add_argument(
        "--test", help="Test the templates without making changes", action="store_true"
    )

    args = parser.parse_args()

    if args.test:
        with tempfile.TemporaryDirectory(dir="/tmp") as temp_dir:
            build_static_template(f"{temp_dir}/messages.pot")

            static_success = compare_files("app/translations", temp_dir, "messages.pot")

            if not static_success:
                logger.error(
                    "Translation templates are not up to date. Run make translation-templates to fix this"
                )
                sys.exit(1)

            logger.debug("Translation templates are up to date.")
        sys.exit(0)

    build_static_template("app/translations/messages.pot")
