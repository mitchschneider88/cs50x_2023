#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;

            image[i][j].rgbtRed = (int) round((red + green + blue) / 3.0);
            image[i][j].rgbtGreen = (int) round((red + green + blue) / 3.0);
            image[i][j].rgbtBlue = (int) round((red + green + blue) / 3.0);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;
            if ((.393 * red) + (.769 * green) + (.189 * blue) < 255)
            {
                image[i][j].rgbtRed = (int) round((.393 * red) + (.769 * green) + (.189 * blue));
            }

            else
            {
                image[i][j].rgbtRed = 255;
            }

            if ((.349 * red) + (.686 * green) + (.168 * blue) < 255)
            {
                image[i][j].rgbtGreen = (int) round((.349 * red) + (.686 * green) + (.168 * blue));
            }

            else
            {
                image[i][j].rgbtGreen = 255;
            }

            if ((.272 * red) + (.534 * green) + (.131 * blue) < 255)
            {
                image[i][j].rgbtBlue = (int) round((.272 * red) + (.534 * green) + (.131 * blue));
            }

            else
            {
                image[i][j].rgbtBlue = 255;
            }

        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;

        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

            copy[i][j] = image[i][j];

        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumRed = 0;
            int sumGreen = 0;
            int sumBlue = 0;
            float avg = 0.0;

            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    int x = i + k;
                    int y = j + l;
                    if (x < 0 || x > (height - 1) || y < 0 || y > (width - 1))
                    {
                        continue;
                    }

                    sumRed += copy[x][y].rgbtRed;
                    sumGreen += copy[x][y].rgbtGreen;
                    sumBlue += copy[x][y].rgbtBlue;
                    avg++;

                }
            }

            image[i][j].rgbtRed = (int) round(sumRed / avg);
            image[i][j].rgbtGreen = (int) round(sumGreen / avg);
            image[i][j].rgbtBlue = (int) round(sumBlue / avg);
        }
    }
    return;
}
