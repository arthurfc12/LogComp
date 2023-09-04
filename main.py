import sys

def calc(equation):
    resultado = 0
    sinal = 0
    previous = 0
    for i in range (len(equation)):
        substring = equation[previous:i]
        number  = int(substring)
        if equation[i] == "+":
            if sinal == 0:
                resultado += number
            else:
                resultado -= number
            sinal = 0
            previous = i+1
        if equation[i] == "-":
            if sinal == 0:
                resultado += number
            else:
                resultado -= number
            sinal = 1
            previous = i+1
    if sinal == 0:
        resultado += int(equation[previous:])
    else:
        resultado -= int(equation[previous:])
    print(resultado)

if __name__ == "__main__":
    calc(sys.argv[1])