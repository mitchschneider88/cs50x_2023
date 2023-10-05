#include <cs50.h>
#include <stdio.h>

int get_cents(void);
int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);

int main(void)
{
    // Ask how many cents the customer is owed
    int cents = get_cents();

    // Calculate the number of quarters to give the customer
    int quarters = calculate_quarters(cents);
    cents = cents - quarters * 25;

    // Calculate the number of dimes to give the customer
    int dimes = calculate_dimes(cents);
    cents = cents - dimes * 10;

    // Calculate the number of nickels to give the customer
    int nickels = calculate_nickels(cents);
    cents = cents - nickels * 5;

    // Calculate the number of pennies to give the customer
    int pennies = calculate_pennies(cents);
    cents = cents - pennies * 1;

    // Sum coins
    int coins = quarters + dimes + nickels + pennies;

    // Print total number of coins to give the customer
    printf("%i\n", coins);
}

int get_cents(void) // creating a variable for the user to input the amount of change needed
{
    int change;
    do
    {
        change = get_int("Change: ");
    }
    while (change < 0);
    return change;

}

int calculate_quarters(int cents) // running a loop to determine how many quarters are needed
{
    int quarters;
    for (quarters = 0; cents > 24; quarters++)
    {
        cents -= 25;
    }

    return quarters;
}

int calculate_dimes(int cents) // running a loop to determine how many dimes are needed
{
    int dimes;
    for (dimes = 0; cents > 9; dimes++)
    {
        cents -= 10;
    }

    return dimes;
}

int calculate_nickels(int cents) // running a loop to determine how many nickels are needed
{
    int nickels;
    for (nickels = 0; cents > 4; nickels++)
    {
        cents -= 5;
    }

    return nickels;
}

int calculate_pennies(int cents) // running a loop to determine how many pennies are needed
{
    int pennies;
    for (pennies = 0; cents > 0; pennies++)
    {
        cents -= 1;
    }

    return pennies;
}
