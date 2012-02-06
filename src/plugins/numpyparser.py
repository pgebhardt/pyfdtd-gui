import numpy
import string


class BooleanParser:
    def __init__(self):
        pass

    def parse(self, expr, **kargs):
        # not parsable callback
        def callback_not_parasable(x, kargs):
            print '\"{}\" not parsable'.format(x)

        # not callback
        def callback_not(x, kargs):
            # parse not
            return self.unary_pareser(x, 'not', numpy.logical_not,
                    callback_not_parasable, kargs)

        # and callback
        def callback_and(x, kargs):
            # parse and
            return self.binary_pareser(x, None, 'and', numpy.logical_and,
                    callback_not, kargs)

        # try parse or
        result = self.binary_pareser(expr, None, 'or', numpy.logical_or,
                callback_and, kargs)

        # return result
        return result

    def binary_pareser(self, x1, x2, keyword, function, callback, kargs):
        print 'input: {}'.format([x1, x2])

        # check type of x1
        if isinstance(x1, str):
            expressions = x1.split(keyword)
            print 'x1: {}'.format(expressions)

            # check for length of expressions
            if len(expressions) > 1:
                x1 = self.binary_pareser(string.strip(expressions[0]),
                        string.strip(string.join(expressions[1:], keyword)),
                        keyword, function, callback, kargs)

        # check type of x2
        if isinstance(x2, str):
            expressions = x2.split(keyword)
            print 'x2: {}'.format(expressions)

            # check for length of expressions
            if len(expressions) > 1:
                x2 = self.binary_pareser(string.strip(expressions[0]),
                        string.strip(string.join(expressions[1:], keyword)),
                        keyword, function, callback, kargs)

        # evaluate
        def evaluate(x):
            # check for list
            if isinstance(x, list):
                x = x[0]

            # check for string
            if isinstance(x, str):
                try:
                    x = eval(x, kargs)
                except ValueError as e:
                    # if evaluation does not work call callback
                    if callback:
                        x = callback(x, kargs)
                    else:
                        raise e

            # check for numpy array
            elif isinstance(x, numpy.ndarray):
                pass

            else:
                raise ValueError('x is invalid: ' + str(x))

            return x

        # evaluate
        x1 = evaluate(x1)
        if x2 == None:
            result = x1

        else:
            x2 = evaluate(x2)
            result = function(x1, x2)

        # return
        print 'result: {}'.format(result)
        return result

    def unary_pareser(self, x1, keyword, function, callback, kargs):
        print 'input: {}'.format(x1)

        # check type of x1
        if isinstance(x1, str):
            expressions = x1.split(keyword)
            print 'x1: {}'.format(expressions)

            # check for length of expressions
            if len(expressions) != 2:
                raise ValueError('\"{}\" not parsable'.format(x1))

            x1 = string.strip(expressions[1])

        # evaluate
        def evaluate(x):
            # check for list
            if isinstance(x, list):
                x = x[0]

            # check for string
            if isinstance(x, str):
                try:
                    x = eval(x, kargs)
                except ValueError as e:
                    # if evaluation does not work call callback
                    if callback:
                        x = callback(x, kargs)
                    else:
                        raise e

            # check for numpy array
            elif isinstance(x, numpy.ndarray):
                pass

            else:
                raise ValueError('x is invalid: ' + str(x))

            return x

        # evaluate
        x1 = evaluate(x1)
        print x1
        result = function(x1)

        # return
        print 'result: {}'.format(result)
        return result

if __name__ == '__main__':
    expr = 'not X == 2'

    X, Y = numpy.meshgrid(numpy.arange(0.0, 10.0, 1.0), numpy.arange(0.0, 10.0,
        1.0))

    # create parser
    parser = BooleanParser()
    print numpy.where(parser.parse(expr, X=X, Y=Y), 1.0, 0.0)
