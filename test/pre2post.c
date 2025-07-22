#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_EXPR_SIZE 50

char stack[MAX_EXPR_SIZE][MAX_EXPR_SIZE];
int top = -1;

void push(char *s) {
    if (top == MAX_EXPR_SIZE - 1) {
        printf("Stack Overflow\n");
        exit(EXIT_FAILURE);
    }
    strcpy(stack[++top], s);
}

char* pop() {
    if (top == -1) {
        printf("Stack Underflow\n");
        exit(EXIT_FAILURE);
    }
    return stack[top--];
}

int is_operator(char x) {
    return (x == '+' || x == '-' || x == '*' || x == '/');
}

void prefixToPostfix(char *prefix) {
    int i, l;
    char op1[50], op2[50];

    l = strlen(prefix);

    for (i = l - 1; i >= 0; i--) {
        if (!is_operator(prefix[i])) {
            char temp[3] = {prefix[i], '\0'};
            push(temp);
        } else {
            if (top < 1) {
                printf("Invalid Prefix Expression\n");
                exit(EXIT_FAILURE);
            }

            strcpy(op1, pop());
            strcpy(op2, pop());

            char temp[50];
            temp[0] = '\0';
            strcat(temp, op1);
            strcat(temp, op2);
            temp[strlen(temp)] = prefix[i];
            push(temp);
        }
    }

    if (top != 0) {
        printf("Invalid Prefix Expression\n");
        exit(EXIT_FAILURE);
    }

    printf("Postfix Expression: %s\n", stack[top]);
}

int main() {
    char prefix[MAX_EXPR_SIZE];
    printf("Enter prefix expression: ");
    scanf("%s", prefix);

    prefixToPostfix(prefix);

    return 0;
}
