#include <stdio.h>

typedef enum {
    ORDER_CREATED,
    ORDER_PAID,
    ORDER_SHIPPED,
    ORDER_DELIVERED,
    ORDER_CANCELLED
} OrderState;

const char* state_name(OrderState s) {
    switch (s) {
        case ORDER_CREATED: return "CREATED";
        case ORDER_PAID: return "PAID";
        case ORDER_SHIPPED: return "SHIPPED";
        case ORDER_DELIVERED: return "DELIVERED";
        case ORDER_CANCELLED: return "CANCELLED";
        default: return "UNKNOWN";
    }
}

int can_transition(OrderState from, OrderState to) {
    switch (from) {
        case ORDER_CREATED:
            return to == ORDER_PAID || to == ORDER_CANCELLED;

        case ORDER_PAID:
            return to == ORDER_SHIPPED || to == ORDER_CANCELLED;

        case ORDER_SHIPPED:
            return to == ORDER_DELIVERED;

        case ORDER_DELIVERED:
            return 0;

        case ORDER_CANCELLED:
            return 0;

        default:
            return 0;
    }
}

OrderState apply_transition(OrderState current, OrderState next) {
    if (can_transition(current, next)) {
        return next;
    }
    return current;
}

int main(void) {
    OrderState state = ORDER_CREATED;

    printf("Initial: %s\n", state_name(state));

    state = apply_transition(state, ORDER_PAID);
    printf("After payment: %s\n", state_name(state));

    state = apply_transition(state, ORDER_SHIPPED);
    printf("After shipping: %s\n", state_name(state));

    state = apply_transition(state, ORDER_DELIVERED);
    printf("After delivery: %s\n", state_name(state));

    state = apply_transition(state, ORDER_CANCELLED);
    printf("After invalid cancel attempt: %s\n", state_name(state));

    return 0;
}