from typing import Generator, Iterable, Mapping


def find_pointers_containing(
    input_data: Mapping | Iterable[Mapping],
    search_key: str,
    pointer: str | None = None,
) -> Generator[str, None, None]:
    """
    Recursive function which lists pointers which contain a search key

    :param input_data: the input data to search
    :param search_key: the key to search for
    :param pointer: the key to search for
    :return: generator of the json pointer paths
    """
    if isinstance(input_data, dict):
        if search_key in input_data:
            yield pointer or ""
        for k, v in input_data.items():
            if isinstance(v, (list, tuple, dict)):
                yield from find_pointers_containing(
                    v, search_key, pointer + "/" + k if pointer else "/" + k
                )
    elif isinstance(input_data, (list, tuple)):
        for index, item in enumerate(input_data):
            yield from find_pointers_containing(item, search_key, f"{pointer}/{index}")


def get_answers_from_question(question: Mapping) -> list:
    static_answers = question.get("answers", [])
    dynamic_answers = question.get("dynamic_answers", {}).get("answers", [])
    return [*dynamic_answers, *static_answers]


def get_answer_ids_in_block(block: Mapping) -> list[str]:
    question = block["question"]
    answer_ids = []
    for answer in get_answers_from_question(question):
        answer_ids.append(answer["id"])

    return answer_ids
