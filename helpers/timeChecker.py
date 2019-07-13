def checkElapsedTime(measuredFunction):
    """
        Декоратор, засечет время работы функции
        Пример работы
        @timeChecker.checkElapsedTime
        def foo():
            print("foo")
    """
    import time
    def the_wrapper(*args, **kwargs):
        start = time.time()
        res = measuredFunction(*args, **kwargs)
        end = time.time()
        print('[*] elapsed time: {} second'.format(end-start))
        return res
    return the_wrapper



def checkElapsedTimeAndCompair(criticalTime, permissibleTime, greatTime):
    """
        Декоратор, засечет время работы функции и сравнит с необходимыми
        ВРФ = время работы функции
        Время рассчитывается в секнудах
        criticalTime - максимальное время работы, если ВРФ больше, то оно будет выведено красным [c]
        permissibleTime - допустимое время работы - желтое [c]
        greatTime - прекрасно, мы вошли в рамки - зеленое [c]
    """
    def checkElapsedTime(measuredFunction):
        import time
        def the_wrapper(*args, **kwargs):
            start = time.time()
            res = measuredFunction(*args, **kwargs)
            end = time.time()
            color, state = getColorForTime(end-start, criticalTime, permissibleTime, greatTime)
            print(color + '[*{}] elapsed time: {} second'.format(state, end-start))
            return res
        return the_wrapper

    return checkElapsedTime

def getColorForTime(currentTime, criticalTime, permissibleTime, greatTime):
    from colorama import Fore
    if (currentTime >= criticalTime):
        return Fore.RED, "critical"
    elif (currentTime < criticalTime and currentTime >= permissibleTime):
        return Fore.LIGHTRED_EX, "not permissable"
    elif (currentTime < permissibleTime and currentTime >= greatTime):
        return Fore.YELLOW, "permissable"
    elif (currentTime < greatTime):
        return Fore.GREEN, "ok"
    else:
        pass



    