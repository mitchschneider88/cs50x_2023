#include <stdio.h>
#include <cs50.h>

int get_height(void);
void print_grid(int height);

int main(void)
{

    // gets height of grid
    int n = get_height();

    // prints grid
    print_grid(n);

}

















int get_height(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n > 8 || n < 1);
    return n;
}

void print_grid(int height)

{
    for (int i = 0; i < height; i++)
        // helpful to think of "i" as the line you are on... the loop will iterate a certain amount of times depeneding on height variable

    {
        for (int j = i + 2; j <= height; j++) // this loop adds spaces to the left column
        {
            printf(" ");
        }

        for (int k = 0; k <= i; k++) // the following loops adds the hashes and space between the hashes
        {
            printf("#");
        }

        printf("  ");

        for (int l = 0; l <= i; l++)
        {
            printf("#");
        }

        printf("\n");

    }
}