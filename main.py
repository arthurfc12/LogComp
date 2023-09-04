import sys
import re
import string

def calculate_expression(eq):
    # Initialize variables
    resultado = 0
    prev_num_index = 0
    subtstring = eq[prev_num_index:i]
    number = int(subtstring)
    sinal = 0  # 0 represents addition, 1 represents subtraction

    # Iterate through the characters in the expression
    for i, char in enumerate(eq):
        if char == "+":
            if sinal == 0:
                resultado += number
            else:
                resultado -= number
            sinal = 0
            prev_num_index = i + 1
        elif char == "-":
            if sinal == 0:
                resultado += number
            else:
                resultado -= number
            sinal = 1
            prev_num_index = i + 1

    # Handle the last part of the expression
    if sinal == 0:
        resultado += int(eq[prev_num_index:])
    else:
        resultado -= int(eq[prev_num_index:])

    return resultado

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("python script_name.py <expression>")
    else:
        expression = sys.argv[1]
        result = calculate_expression(expression)
        print(result)
