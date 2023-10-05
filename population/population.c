#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int start;
    do // gets starting population
    {
        start = get_int("Starting Population: ");
    }
    while (start < 9);

    int end;
    do // gets ending population
    {
        end = get_int("Ending Population: ");
    }
    while (end < start);

    int n;
    for (n = 0; end > start; n++) // loops through math, terminates when ending population is larger than starting
    {
        int born = start / 3;
        int died = start / 4;
        start = (start + born) - died;
    }

    printf("Years: %i\n", n);

}