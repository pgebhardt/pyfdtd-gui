import numpy


class BooleanParser:
    def __init__(self):
        pass

    def parse(self, expression, **kargs):
        # split expression
        words = expression.split()

        # look for keywords
        count_and = words.count('and')
        count_or = words.count('or')
        count_xor = words.count('xor')

        # create x1
        x1 = ''
        for i in range(0, words.index('and')):
            x1 += words[i] + ' '

        # create x2
        x2 = ''
        for j in range(i + 2, len(words)):
            x2 += words[j] + ' '

        # return value
        return self.and_(eval(x1, kargs), eval(x2, kargs))

    # operators
    and_ = numpy.logical_and
    or_ = numpy.logical_or
    not_ = numpy.logical_not
    xor_ = numpy.logical_xor

if __name__ == '__main__':
    expr = 'X > 2 and Y > 4'

    X, Y = numpy.meshgrid(numpy.arange(0.0, 10.0, 1.0), numpy.arange(0.0, 10.0,
        1.0))

    # create parser
    parser = BooleanParser()
    print numpy.where(parser.parse(expr, X=X, Y=Y), 1.0, 0.0)
