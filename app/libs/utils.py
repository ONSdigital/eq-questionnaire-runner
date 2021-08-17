def convert_tx_id(tx_id: str) -> str:
    """
    Converts the guid tx_id to uppercase string of 16 characters with a dash between every 4 characters
    :param tx_id: tx_id to be converted
    :return: String in the form of xxxx-xxxx-xxxx-xxxx
    """
    return " - ".join(((tx_id[:4] + "-" + tx_id[4:])[:19]).split("-")).upper()
