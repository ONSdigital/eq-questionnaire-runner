import re
from typing import Union


def to_bytes(bytes_or_str: Union[bytes, str]) -> bytes:
    """
    Converts supplied data into bytes if the data is of type str.
    :param bytes_or_str: Data to be converted.
    :return: UTF-8 encoded bytes if the data was of type str. Otherwise it returns the supplied data as is.
    """
    if isinstance(bytes_or_str, str):
        return bytes_or_str.encode()
    return bytes_or_str


def to_str(bytes_or_str: Union[bytes, str]) -> str:
    """
    Converts supplied data into a UTF-8 encoded string if the data is of type bytes.
    :param bytes_or_str: Data to be converted.
    :return: UTF-8 encoded string if the data was of type bytes.  Otherwise it returns the supplied data as is.
    """
    if isinstance(bytes_or_str, bytes):
        return bytes_or_str.decode()
    return bytes_or_str


def safe_content(content: str) -> str:
    """Make content safe.

    Replaces variable with ellipsis and strips any HTML tags.

    :param (str) content: Input string.
    :returns (str): Modified string.
    """
    if content is not None:
        # Replace piping with ellipsis
        content = re.sub(r"{.*?}", "…", content)
        # Strip HTML Tags
        content = re.sub(r"</?[^>]+>", "", content)
    return content


def pascal_case_to_hyphenated_lowercase(string: str) -> str:
    """
    Changes text from PascalCase to hyphenated-lowercase
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "-", string).lower()
