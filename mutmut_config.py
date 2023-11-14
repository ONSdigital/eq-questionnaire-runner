lines_to_skip = (
    "@dataclass",
    # we could skip more things here maybe?
)


def pre_mutation(context):
    line = context.current_source_line.strip()
    if any(line.startswith(skip) for skip in lines_to_skip):
        context.skip = True
