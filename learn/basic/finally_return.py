def bool_return():
    try:
        print("try")
        return True
        print("has returned")
    finally:
        return False

# print( bool_return() )

def divide(x, y):
    try:
        result = x / y
        # y = 0
        # result = x / y
        # print("is error returned?", result)
    except ZeroDivisionError:
        print("ZeroDivisionError")
    else:
        print("result is", result)
    finally:
        print("executing finally clause")
divide(2, 1)

# If a finally clause is present, the finally clause will execute as the last task before the try statement completes. The finally clause runs whether or not the try statement produces an exception. The following points discuss more complex cases when an exception occurs:
#
# If an exception occurs during execution of the try clause, the exception may be handled by an except clause. If the exception is not handled by an except clause, the exception is re-raised after the finally clause has been executed.
#
# An exception could occur during execution of an except or else clause. Again, the exception is re-raised after the finally clause has been executed.
#
# If the finally clause executes a break, continue or return statement, exceptions are not re-raised.
#
# If the try statement reaches a break, continue or return statement, the finally clause will execute just prior to the break, continue or return statement’s execution.
#
# If a finally clause includes a return statement, the returned value will be the one from the finally clause’s return statement, not the value from the try clause’s return statement.