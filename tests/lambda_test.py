# PYTHON IS A STUPID ASS LANGUAGE. WHY DOES THIS BEHAVE THIS WAY??


class Test:
    def __init__(self, test) -> None:
        self.test = test


def lul(ar, ag):
    print(ar, ag)


# wrong test
asd = [1, 2, 3, 4]
for i in range(4):
    asd[i] = Test(lambda a: lul(a, i))

asd[0].test(1)
asd[1].test(2)
asd[2].test(3)
asd[3].test(4)


# succesfull test
asd1 = Test(lambda a: lul(a, 1))
asd2 = Test(lambda a: lul(a, 2))

asd1.test(13)
asd2.test(14)


class TestTest:
    def __init__(self, test) -> None:
        self.test = test


def lel(ar):
    print(ar)


# wrong test
asdasd = [1, 2, 3, 4]
for i in range(4):
    asdasd[i] = TestTest(lambda: lel(i + 30))
    asdasd[i].test()

asdasd[0].test()
asdasd[1].test()
asdasd[2].test()
asdasd[3].test()


# succesfull test
asd1 = Test(lambda: lel(41))
asd2 = Test(lambda: lel(42))

asd1.test()
asd2.test()