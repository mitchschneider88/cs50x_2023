#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage

    if (argc != 3)
    {
        printf("Usage: ./reverse input.wav output.wav\n");
        return 1;
    }

    // Open input file for reading

    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Cannot open input file\n");
        return 1;
    }

    // Read header into an array

    WAVHEADER head;
    fread(&head, sizeof(head), 1, input);

    // Use check_format to ensure WAV format

    check_format(head);

    // Open output file for writing

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Cannot create output file\n");
        return 1;
    }

    // Write header to file

    fwrite(&head, sizeof(head), 1, output);

    // Use get_block_size to calculate size of block

    int blocksize = get_block_size(head);

    // Write reversed audio to file
    // TODO #8
    WORD buffer[blocksize];
    fseek(input, 0, SEEK_END);

    while (ftell(input) > sizeof(head))
    {
        fseek(input, -1 * blocksize, SEEK_CUR);
        fread(buffer, blocksize, 1, input);
        fwrite(buffer, blocksize, 1, output);
        fseek(input, -1 * blocksize, SEEK_CUR);
    }

    fclose(input);
    fclose(output);
}

int check_format(WAVHEADER header)
{

    if (header.format[0] == 87 && header.format[1] == 65 && header.format[2] == 86 && header.format[3] == 69)
    {
        return true;
    }
    else
    {
        return false;
    }
    // TODO #4
    return 0;
}

int get_block_size(WAVHEADER header)
{
    int block = header.numChannels * (header.bitsPerSample / 8);
    return block;
    return 0;
}