import time

from utils import calculate_hash

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
        hash = calculate_hash(index, previous_hash, timestamp, data)
        return Block(index, hash, previous_hash, timestamp, data)

    def __str__(self):
        return "{index: %s, hash: %s, previous_hash: %s, timestamp: %s, data: %s}" % (
            self.index,
            self.hash,
            self.previous_hash,
            self.timestamp,
            self.data,
        )

