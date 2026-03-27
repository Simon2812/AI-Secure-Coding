#include <stdio.h>

int binary_search(const int *arr, int left, int right, int target) {
    if (left > right) {
        return -1;
    }

    int mid = left + (right - left) / 2;

    if (arr[mid] == target) {
        return mid;
    }

    if (target < arr[mid]) {
        return binary_search(arr, left, mid - 1, target);
    }

    return binary_search(arr, mid + 1, right, target);
}

int main(void) {
    int data[] = {2, 5, 8, 12, 16, 23, 38, 56};
    int size = sizeof(data) / sizeof(data[0]);

    int target = 23;
    int index = binary_search(data, 0, size - 1, target);

    if (index >= 0) {
        printf("Found at index %d\n", index);
    } else {
        printf("Not found\n");
    }

    return 0;
}