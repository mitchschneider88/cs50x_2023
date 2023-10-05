import cs50


def main():

    dollars = get_dollar()

    quarters = calculate_quarters(dollars)
    dollars = dollars - quarters * 0.25

    dimes = calculate_dimes(dollars)
    dollars = dollars - dimes * 0.10

    nickels = calculate_nickels(dollars)
    dollars = dollars - nickels * 0.05

    pennies = calculate_pennies(dollars)
    dollars = dollars - pennies * 0.01

    coins = quarters + dimes + nickels + pennies

    print(coins)


def get_dollar():

    while True:
        change = cs50.get_float("Change: ")
        if change > 0:
            break

    return change


def calculate_quarters(dollars):

    quarters = 0

    while dollars > 0.24:
        quarters += 1
        dollars -= 0.25

    return quarters


def calculate_dimes(dollars):

    dimes = 0

    while dollars > 0.09:
        dimes += 1
        dollars -= 0.10

    return dimes


def calculate_nickels(dollars):

    nickels = 0

    while dollars > 0.04:
        nickels += 1
        dollars -= 0.05

    return nickels


def calculate_pennies(dollars):

    pennies = 0

    while dollars > 0.009:
        pennies += 1
        dollars -= 0.01

    return pennies


if __name__ == "__main__":
    main()