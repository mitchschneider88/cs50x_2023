#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string excerpt);
int count_words(string excerpt);
int count_sentences(string excerpt);

int main(void)
{
    string excerpt = get_string("Your Excerpt: \n");

    float L = ((float) count_letters(excerpt) / (float) count_words(excerpt)) * 100.0;

    float S = (float) count_sentences(excerpt) / (float) count_words(excerpt) * 100.0;

    float index = 0.0588 * L - 0.296 * S - 15.8;

    int index_rounded = round(index);s

    if (index_rounded < 16 && index_rounded > 0)
    {
        printf("Grade %i\n", index_rounded);
    }
    else if (index_rounded < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade 16+\n");
    }


}

int count_letters(string excerpt)
{
    int letters = 0;
    for (int i = 0; i < strlen(excerpt); i++)
    {
        if (isalpha(excerpt[i]))
        {
            letters++;
        }
    }

    return letters;
}

int count_words(string excerpt)
{
    int words = 0;
    for (int i = 0; i <= strlen(excerpt); i++)
    {
        if (isspace(excerpt[i]))
        {
            words++;
        }
    }

    return words + 1;
}

int count_sentences(string excerpt)
{
    int sentences = 0;
    for (int i = 0; i < strlen(excerpt); i++)
    {
        if (excerpt[i] == '!' || excerpt[i] == '.' || excerpt[i] == '?')
        {
            sentences++;
        }
    }

    return sentences;
}