import hashlib

import genisis

def calculate_hash(index, previous_hash, timestamp, data):
    return str(
        hashlib.sha256(
            str(index).encode()
            + previous_hash.encode()
            + str(timestamp).encode()
            + data
        ).digest()
    )


def calculate_hash_for_block(block):
    return calculate_hash(block.index, block.previous_hash, block.timestamp, block.data)


def is_valid_new_block(previous_block, new_block):
    if previous_block.index != new_block.index - 1:
        print("Is valid new block check: index do not match")
        return False
    elif previous_block.hash != new_block.previous_hash:
        print("Is valid new block check: previous_hash do not match")
        return False
    elif calculate_hash_for_block(new_block) != new_block.hash:
        print("Is valid new block check: hash do not match")
        return False
    else:
        return True


def is_valid_block_structure(block):
    return (
        type(block.index) is int
        and type(hash) is str
        and type(previous_hash) is str
        and type(timestamp) is float
        and type(data) is bytes
    )


def is_valid_chain(chain):
    def is_valid_genisis(block):
        return str(block) == str(genesis_block)

    if not is_valid_genisis(chain[0]):
        return False

    for i in range(1, len(chain)):
        if not is_valid_new_block(chain[i - 1], chain[i]):
            return False
    return True


def replace_chain(new_chain):
    if is_valid_chain(new_blocks) and len(new_chain) > len(
        chain
    ):  # TODO: chain should probably be changed to something like get_block_chain()
        chain = new_chain
        # TODO: Should broadcast the new chain
