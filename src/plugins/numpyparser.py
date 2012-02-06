import numpy
import string


class BooleanParser:
    def __init__(self):
        pass

    def parse(self, expr, **kargs):
        # try parse and
        result = self.generic_pareser(expr, None, 'and', numpy.logical_and,
                kargs)

        # return result
        return result

    def binary_pareser(self, x1, x2, keyword, function, kargs):
        print 'input: {}'.format([x1, x2])

        # check type of x1
        if isinstance(x1, str):
            expressions = x1.split(keyword)
            print 'x1: {}'.format(expressions)

            # check for length of expressions
            if len(expressions) > 1:
                x1 = self.binary_pareser(string.strip(expressions[0]),
                        string.strip(string.join(expressions[1:], keyword)),
                        keyword, function, kargs)

        # check type of x2
        if isinstance(x2, str):
            expressions = x2.split('and')
            print 'x2: {}'.format(expressions)

            # check for length of expressions
            if len(expressions) > 1:
                x2 = self.binary_pareser(string.strip(expressions[0]),
                        string.strip(string.join(expressions[1:], keyword)),
                        keyword, function, kargs)

        # evaluate
        def evaluate(x):
            # check for list
            if isinstance(x, list):
                x = x[0]

            # check for string
            if isinstance(x, str):
                x = eval(x, kargs)

            # check for numpy array
            elif isinstance(x, numpy.ndarray):
                pass

            else:
                raise ValueError('x is invalid: ' + str(x))

            return x

        # evaluate
        x1 = evaluate(x1)
        if x2 == None:
            return x1

        x2 = evaluate(x2)

        # return
        return function(x1, x2)

if __name__ == '__main__':
    expr = 'X > 2 and X < 4'

    X, Y = numpy.meshgrid(numpy.arange(0.0, 10.0, 1.0), numpy.arange(0.0, 10.0,
        1.0))

    # create parser
    parser = BooleanParser()
    print numpy.where(parser.parse(expr, X=X, Y=Y), 1.0, 0.0)