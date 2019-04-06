from genisis import get_genesis_block

chain = [get_genesis_block()]


def main():
    first_block = get_genesis_block().generate_next_block(bytes("awesome pepe meme", "utf-8"))
    chain.append(first_block)
    second_block = first_block.generate_next_block(bytes("awesome Pepe 2", "utf-8"))
    chain.append(second_block)
    print(first_block)
    print(second_block)


if __name__ == "__main__":
    main()
