def find_pointers_containing(input_data, search_key, pointer=None):
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
            if (isinstance(v, dict)) and search_key in v:
                yield pointer + "/" + k if pointer else "/" + k
            else:
                yield from find_pointers_containing(
                    v, search_key, pointer + "/" + k if pointer else "/" + k
                )
    elif isinstance(input_data, (list, tuple)):
        for index, item in enumerate(input_data):
            yield from find_pointers_containing(item, search_key, f"{pointer}/{index}")


def get_answer_ids_in_block(block):
    question = block["question"]
    answer_ids = []
    for answer in question["answers"]:
        answer_ids.append(answer["id"])

    return answer_ids
