import random


def vvcode():
    num0 = random.randint(1, 9)
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    num3 = random.randint(0, 9)
    num4 = random.randint(0, 9)
    num5 = random.randint(1, 9)
    verifCode = f'{num0}{num1}{num2}{num3}{num4}{num5}'
    return verifCode