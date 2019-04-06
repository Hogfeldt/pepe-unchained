import hashlib

import genisis
from block import Block


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


def get_accumulated_difficulty(chain):
    return sum([2 ** d for d in [b.difficulty for b in chain]])


def replace_chain(chain, new_chain):
    if is_valid_chain(new_chain) and get_accumulated_difficulty(
        new_chain
    ) > get_accumulated_difficulty(chain):
        return new_chain
    else:
        return chain


def hash_matched_difficulty(hash, difficulty):
    required_prefix = 0 * difficulty
    return hash.startswith(required_prefix)


def find_block(index, previous_hash, timestamp, data, difficulty):
    nonce = 0
    while True:
        hash = calculate_hash(index, previous_hash, data, difficulty, nonce)
        if hash_matched_difficulty(hash, difficulty):
            return Block(index, hash, previous_hash, timestamp, data, difficulty, nonce)
        nonce += 1


def get_adjusted_difficulty(latest_block, chain):
    prev_adjustment_block = chain[-1 * genisis.get_difficulty_adjustment_interval()]
    time_expected = (
        genisis.get_block_generation_interval()
        * genisis.get_difficulty_adjustment_interval
    )
    time_taken = latest_block.timestamp - prev_adjustment_block.timestamp
    if time_taken < time_expected / 2:
        return prev_adjustment_block.difficulty + 1
    elif time_taken > time_expected * 2:
        return prev_adjustment_block - 1
    else:
        return prev_adjustment_block.difficulty


def get_difficulty(chain):
    latest_block = chain[-1]
    if (
        latest_block.index % genisis.get_difficulty_adjustment_interval == 0
        and latest_block.index != 0
    ):
        return genisis.get_adjusted_difficulty(latest_block, chain)
    else:
        return latest_block.difficulty


def is_valid_timestamp(new_block, previous_block):
    return (
        previous_block.timestamp - 60 < new_block.timestamp
        and new_block.timestamp - 60 < time.time()
    )
