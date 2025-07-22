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

void postfixToPrefix(char *postfix) {
    int i, l;
    char op1[50], op2[50];

    l = strlen(postfix);

    for (i = 0; i < l; i++) {
        if (!is_operator(postfix[i])) {
            char temp[3] = {postfix[i], '\0'};
            push(temp);
        } else {
            if (top < 1) {
                printf("Invalid Postfix Expression\n");
                exit(EXIT_FAILURE);
            }

            strcpy(op2, pop());
            strcpy(op1, pop());

            char temp[50];
            temp[0] = postfix[i];
            temp[1] = '\0';
            strcat(temp, op1);
            strcat(temp, op2);

            push(temp);
        }
    }

    if (top != 0) {
        printf("Invalid Postfix Expression\n");
        exit(EXIT_FAILURE);
    }

    printf("Prefix Expression: %s\n", stack[top]);
}

int main() {
    char postfix[MAX_EXPR_SIZE];
    printf("Enter postfix expression: ");
    scanf("%s", postfix);

    postfixToPrefix(postfix);

    return 0;
}
