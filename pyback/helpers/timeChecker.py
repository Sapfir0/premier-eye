
def checkElapsedTime(measuredFunction):
    """
        Decorator, timed function
        Work example:
        @timeChecker.checkElapsedTime
        def foo():
            print("foo")
    """
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        res = measuredFunction(*args, **kwargs)
        end = time.time()
        print('[*] elapsed time: {} second'.format(end - start))
        return res
    return wrapper


def checkElapsedTimeAndCompair(criticalTime, permissibleTime, greatTime, helperStr=""):
    """
        The decorator will detect the function time and compare it with the necessary ones.
        FT = function time
        Time is calculated in seconds
        criticalTime - the maximum running time, if the FT is longer, it will be displayed in red [seconds]
        permissibleTime - permissible working time - yellow [seconds]
        greatTime - great, we went into the frame - green [seconds]
    """
    def checkElapsedTime(measuredFunction):
        import time

        def wrapper(*args, **kwargs):
            start = time.time()
            res = measuredFunction(*args, **kwargs)
            end = time.time()
            color, state = getColorForTime(
                end - start, criticalTime, permissibleTime, greatTime)
            print(
                color + '[*{}] {} elapsed time: {} second'.format(state, helperStr, end - start))
            return res
        return wrapper

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
