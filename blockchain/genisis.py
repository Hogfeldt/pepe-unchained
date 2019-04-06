from block import Block

genesis_block = Block(
    0,
    "816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7",
    None,
    1554544077.638083,
    bytes("My genises!!", "utf-8"),
)

def get_genesis_block():
    return genesis_block
