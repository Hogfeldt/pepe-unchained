import time

BLOCK_GENERATION_INTERVAL = 10

DIFFICULTY_ADJUSTMENT_INTERVAL = 10


def get_genesis_block():
    return GENESIS_BLOCK


def get_block_generation_interval():
    return BLOCK_GENERATION_INTERVAL


def get_difficulty_adjustment_interval():
    return DIFFICULTY_ADJUSTMENT_INTERVAL


def calculate_hash(index, previous_hash, timestamp, data):
    return str(
        hashlib.sha256(
            str(index).encode()
            + previous_hash.encode()
            + str(timestamp).encode()
            + data
        ).digest()
    )


class Block:
    def __init__(self, index, hash, previous_hash, timestamp, data, difficulty, nonce):
        self.index = index
        self.hash = hash
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def generate_next_block(self, data):
        index = self.index + 1
        previous_hash = self.hash
        timestamp = time.time()
        hash = calculate_hash(index, previous_hash, timestamp, data.encode()).decode()
        return Block(index, hash, previous_hash, timestamp, data)

    def __str__(self):
        return "{index: %s, hash: %s, previous_hash: %s, timestamp: %s, data: %s, difficulty: %s, nonce: %s}" % (
            self.index,
            self.hash,
            self.previous_hash,
            self.timestamp,
            self.data,
            self.difficulty,
            self.nonce,
        )


def dict_to_block(dict_block):
    return Block(
        int(dict_block["index"]),
        dict_block["hash"],
        dict_block["previous_hash"],
        float(dict_block["timestamp"]),
        dict_block["data"],
        int(dict_block["difficulty"]),
        int(dict_block["nonce"]),
    )


GENESIS_BLOCK = Block(
    0,
    "816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7",
    None,
    1554544077.638083,
    "My genises!!",
    4,
    0,
)
