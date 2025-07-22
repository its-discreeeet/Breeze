#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#define MAX_EXPR_SIZE 100

char stack[MAX_EXPR_SIZE];
int top = -1;

// Function to push an item onto the stack
void push(char item) {
    if (top == MAX_EXPR_SIZE - 1) {
        printf("Stack Overflow\n");
        exit(EXIT_FAILURE);
    }
    stack[++top] = item;
}

// Function to pop an item from the stack
char pop() {
    if (top == -1) {
        printf("Stack Underflow\n");
        exit(EXIT_FAILURE);
    }
    return stack[top--];
}

// Function to get the in-stack precedence of an operator
int isp(char ch) {
    switch (ch) {
        case '^':
            return 4;
        case '*':
        case '/':
            return 2;
        case '+':
        case '-':
            return 1;
        default:
            return 0;
    }
}

// Function to get the incoming precedence of an operator
int icp(char ch) {
    switch (ch) {
        case '^':
            return 3;
        case '*':
        case '/':
            return 2;
        case '+':
        case '-':
            return 1;
        default:
            return 0;
    }
}

// Function to reverse a string
void reverseString(char str[]) {
    int length = strlen(str);

    for (int i = 0; i < length / 2; i++) {
        // Swap characters from the beginning and end of the string
        char temp = str[i];
        str[i] = str[length - i - 1];
        str[length - i - 1] = temp;
    }
}

// Function to convert infix to prefix
void infixToPrefix(char infix[], char prefix[]) {
    int i = 0, k = 0;
    char tkn = infix[i];

    // Reverse the infix expression
    reverseString(infix);

    while (tkn != '\0') {
        if (isalnum(tkn)) {
            prefix[k++] = tkn;
        } else if (tkn == ')') {
            push(')');
        } else if (tkn == '(') {
            while ((tkn = pop()) != ')') {
                prefix[k++] = tkn;
            }
        } else {
            while (top != -1 && isp(stack[top]) >= icp(tkn)) {
                prefix[k++] = pop();
            }
            push(tkn);
        }
        i++;
        tkn = infix[i];
    }

    while (top != -1) {
        prefix[k++] = pop();
    }

    prefix[k] = '\0';

    // Reverse the prefix expression
    reverseString(prefix);
}

// Main function
int main() {
    char infix[MAX_EXPR_SIZE];
    printf("Enter infix expression: ");
    scanf("%s", infix);

    char prefix[MAX_EXPR_SIZE];

    // Function call to convert infix to prefix
    infixToPrefix(infix, prefix);

    // Print the results
    printf("Infix Expression: %s\n", infix);
    printf("Prefix Expression: %s\n", prefix);

    return 0;
}
