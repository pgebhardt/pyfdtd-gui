import numpy
import string


class BooleanParser:
    def __init__(self):
        pass

    def parse(self, expr, **kargs):
        # try parse and
        self.parse_and(expr, None, kargs)

    def parse_not(self, expr, x, kargs):
        pass

    def parse_and(self, x1, x2, kargs):
        # check type of x1
        if isinstance(x1, str):
            expressions = x1.split('and')

            # check for length of expressions
            if len(expressions) > 1:
                x1 = self.parse_and(expressions[0],
                        string.join(expressions[1:]), kargs)

            if x1 == None:
                x1 = ''

        # check type of x2
        if isinstance(x2, str):
            expressions = x2.split('and')

            # check for length of expressions
            if len(expressions) > 1:
                x1 = self.parse_and(expressions[0],
                        string.join(expressions[1:]), kargs)

            if x2 == None:
                x2 = ''

        # evaluate
        if isinstance(x1, str):
            x1 = eval(x1, kargs)

        if isinstance(x2, str):
            x2 = eval(x2, kargs)

        if x2 == None:
            return x1

        else:
            return numpy.logical_and(x1, x2)

    def parse_or(self, x1, x2, kargs):
        pass

    def parse_xor(self, x1, x2, kargs):
        pass


if __name__ == '__main__':
    expr = 'X > 2 and Y > 4'

    X, Y = numpy.meshgrid(numpy.arange(0.0, 10.0, 1.0), numpy.arange(0.0, 10.0,
        1.0))

    # create parser
    parser = BooleanParser()
    print numpy.where(parser.parse(expr, X=X, Y=Y), 1.0, 0.0)
