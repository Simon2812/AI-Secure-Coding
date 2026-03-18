#include <stdio.h>
#include <limits.h>

static void evaluate_score()
{
    char score = CHAR_MAX;

    char squared = score * score;
    printf("%x\n", (unsigned char)squared);
}

int main(void)
{
    evaluate_score();
    return 0;
}