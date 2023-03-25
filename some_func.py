"""
Дано положительное число. Вам необходимо подсчитать
произведение всех цифр в этом числе, за исключением нулей.
"""


def get_mul(number):
    res = 1
    for i in str(number):
        if i != '0':
            res *= int(i)
    # res = 1
    return res


if __name__ == '__main__':
    assert get_mul(123405) == 120
    assert get_mul(999) == 729
    assert get_mul(1000) == 1
    assert get_mul(1111) == 1
