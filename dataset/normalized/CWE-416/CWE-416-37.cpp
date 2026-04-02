#include <iostream>

class TwoIntsClass
{
public:
    int intOne;
    int intTwo;
};

void execute()
{
    TwoIntsClass *obj = new TwoIntsClass;
    obj->intOne = 1;
    obj->intTwo = 2;

    int values[2];
    values[0] = obj->intOne;
    values[1] = obj->intTwo;

    delete obj;

    int diff = values[1] - values[0];
    int sum = values[0] + values[1];

    if(diff >= 0)
    {
        std::cout << sum << std::endl;
    }
}

int main()
{
    execute();
    return 0;
}