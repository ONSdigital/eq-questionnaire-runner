class RoutingPath:
    """Holds a list of block_ids and has section_id, list_item_id and list_name attributes"""

    def __init__(self, block_ids, section_id, list_item_id=None, list_name=None):
        self.block_ids = tuple(block_ids)
        self.section_id = section_id
        self.list_item_id = list_item_id
        self.list_name = list_name

    def __len__(self):
        return len(self.block_ids)

    def __getitem__(self, index):
        return self.block_ids[index]

    def __iter__(self):
        return iter(self.block_ids)

    def __reversed__(self):
        return reversed(self.block_ids)

    def __eq__(self, other):
        if isinstance(other, RoutingPath):
            return (
                self.block_ids == other.block_ids
                and self.section_id == other.section_id
                and self.list_item_id == other.list_item_id
                and self.list_name == other.list_name
            )

        if isinstance(other, list):
            return self.block_ids == tuple(other)

        return self.block_ids == other

    def index(self, *args):
        return self.block_ids.index(*args)
