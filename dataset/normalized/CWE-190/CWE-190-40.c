#include <stdio.h>
#include <limits.h>

static void evaluate()
{
    int value = 10000;
    
    int doubled = value * 2;
    printf("%d\n", doubled);

}

int main(void)
{
    evaluate();
    return 0;
}
