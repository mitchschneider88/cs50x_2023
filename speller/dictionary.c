// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

const unsigned int N = 10000000;

// Hash table
node *table[N];

int dict_size = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);

    node *cursor = table[index];

    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }

        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number

unsigned int hash(const char *word)
{
    // originally was multiplying by an odd number, wouldn't fit into N size
    // modified the djb hash function to fit into N size

    int number = 5381;

    for (int i = 0; i < strlen(word); i++)
    {
        number = (number * 33) + tolower(word[i]);
    }

    number = number % N;

    return number;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{

    FILE *dictionaryfile = fopen(dictionary, "r");
    if (dictionaryfile == NULL)
    {
        printf("Cannot open dictionary file\n");
        return 1;
    }

    char word[LENGTH + 1];

    while (fscanf(dictionaryfile, "%s", word) != EOF)
    {

        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }

        strcpy(n->word, word);

        int index = hash(word);

        n->next = table[index];

        table[index] = n;

        dict_size++;
    }

    fclose(dictionaryfile);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dict_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{

    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }

        if (cursor == NULL && i == (N - 1))
        {
            return true;
        }
    }

    return false;
}

