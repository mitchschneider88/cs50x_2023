from cs50 import get_int

def main():
    length = get_length()
    for i in range(length):
        print("#", end="")
    print()


def get_length():
    while True:
        try:
            n = int(input("Length: "))
            if n > 0:
                return n
        except ValueError:
            print("Not an integer")


main()