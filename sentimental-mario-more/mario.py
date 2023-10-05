import cs50


def main():

    art = getheight()

    print_grid(art)


def getheight():

    while True:
        height = cs50.get_int("Height: ")
        if height < 9 and height > 0:
            break

    return height


def print_grid(height):

    for i in range(height):
        print(" " * (height - (i + 1)), end="")
        print("#" * (i + 1), end="")
        print("  ", end="")
        print("#" * (i + 1), end="")
        print("")


if __name__ == "__main__":
    main()