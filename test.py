from blocks import Block

for name, blocks in Block.BLOCKS.items():
    print(name)

    width = max(x for x, y in blocks) + 1
    height = max(y for x, y in blocks) + 1

    for y in range(height):
        print(
            "".join(
                "██" if (x, y) in blocks else "  "
                for x in range(width)
            )
        )

    print()