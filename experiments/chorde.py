import math


b = 3
eps = 0.001

# def f(x):
#     return math.tan(0.4*x + 0.4) - x**2
def f(x):
    return x**3 - 0.1*(x**2) + 0.4*x - 1.5

def calc_next(x):
    return x - (b - x)/(f(b) - f(x))*f(x)

x_n = calc_next(1)
n = 1
while math.fabs(f(x_n)) >= eps:
    print(str(n) + ": " + str(x_n) + " " +str(math.fabs(f(x_n))))
    x_n = calc_next(x_n)
    n += 1
    pass