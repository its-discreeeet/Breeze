#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

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

// Function to get the incoming precedence of an operator
int icp(char ch) {
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

// Function to convert infix to postfix
void infixToPostfix(char* infix, char* postfix) {
    int i = 0, k = 0;
    char tkn = infix[i];

    while (tkn != '\0') {
    if (isalnum(tkn)) {
        postfix[k++] = tkn;
    } else if (tkn == '(') {
        push('(');
    } else if (tkn == ')') {
        while ((tkn = pop()) != '(') {
            postfix[k++] = tkn;
        }
    } else {
        while (top != -1 && isp(stack[top]) >= icp(tkn)) {
            postfix[k++] = pop();
        }
        push(tkn);
    }
    i++;
    tkn = infix[i];
}


    while (top != -1) {
        postfix[k++] = pop();
    }

    postfix[k] = '\0';
}

// Main function
int main() {
    char infix[MAX_EXPR_SIZE];
    printf("Enter infix expression: ");
    scanf("%s", infix);

    char postfix[MAX_EXPR_SIZE];

    // Function call to convert infix to postfix
    infixToPostfix(infix, postfix);

    // Print the results
    printf("Infix Expression: %s\n", infix);
    printf("Postfix Expression: %s\n", postfix);

    return 0;
}
