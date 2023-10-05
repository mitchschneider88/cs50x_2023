// Capitalizes a string

#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(void)
{
    // Get a string
    char *s = get_string("s: ");

    // Copy string's address
    char *t = malloc(strlen(s) + 1);

    // Capitalize first letter in string
    strcpy(t, s);

    if (strlen(t) > 0)
    {
        t[0] = toupper(t[0]);
    }


    // Print string twice
    printf("s: %s\n", s);
    printf("t: %s\n", t);
}