from block import Block

BLOCK_GENERATION_INTERVAL = 10

DIFFICULTY_ADJUSTMENT_INTERVAL = 10

GENESIS_BLOCK = Block(
    0,
    "816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7",
    None,
    1554544077.638083,
    bytes("My genises!!", "utf-8"),
)


def get_genesis_block():
    return GENESIS_BLOCK

def get_block_generation_interval():
    return BLOCK_GENERATION_INTERVAL

def get_difficulty_adjustment_interval():
    return DIFFICULTY_ADJUSTMENT_INTERVAL
