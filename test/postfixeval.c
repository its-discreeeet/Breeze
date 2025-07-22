#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define MAX_EXPR_SIZE 100

int stack[MAX_EXPR_SIZE];
int top = -1;

// Function to push an element onto the stack
void push(int item) {
    if (top == MAX_EXPR_SIZE - 1) {
        printf("Stack Overflow\n");
        exit(EXIT_FAILURE);
    }
    stack[++top] = item;
}

// Function to pop an element from the stack
int pop() {
    if (top == -1) {
        printf("Stack Underflow\n");
        exit(EXIT_FAILURE);
    }
    return stack[top--];
}

// Function to check if the character is an operator
int isOperator(char c) {
    return (c == '+' || c == '-' || c == '*' || c == '/');
}

// Function to evaluate a postfix expression
int evaluatePostfix(const char* postfix) {
    int i, operand1, operand2, result;
    char token;

    for (i = 0; postfix[i] != '\0'; i++) {
        token = postfix[i];

        if (isdigit(token)) { // Operand
            push(token - '0'); // Convert character to integer and push onto the stack
        } else if (isOperator(token)) { // Operator
            operand2 = pop();
            operand1 = pop();

            switch (token) {
                case '+':
                    result = operand1 + operand2;
                    break;
                case '-':
                    result = operand1 - operand2;
                    break;
                case '*':
                    result = operand1 * operand2;
                    break;
                case '/':
                    if (operand2 != 0) {
                        result = operand1 / operand2;
                    } else {
                        printf("Error: Division by zero\n");
                        exit(EXIT_FAILURE);
                    }
                    break;
                default:
                    printf("Error: Invalid operator\n");
                    exit(EXIT_FAILURE);
            }

            push(result); // Push the result back onto the stack
        }
    }

    return pop(); // The final result is on the top of the stack
}

int main() {
    char postfix[MAX_EXPR_SIZE];

    // Input the postfix expression
    printf("Enter the postfix expression: ");
    scanf("%s", postfix);

    // Evaluate the postfix expression
    int result = evaluatePostfix(postfix);

    // Print the result
    printf("Result: %d\n", result);

    return 0;
}
