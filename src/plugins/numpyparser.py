import numpy
import string


class NumpyParser:
    def __init__(self):
        # ellipse function
        def ellipse(x, y, rx, ry):
            return x ** 2 / rx ** 2 + y ** 2 / ry ** 2 < 1.0

        # define globals
        self.globals_ = {'sin': numpy.sin, 'cos': numpy.cos, 'exp': numpy.exp,
                'log': numpy.log, 'pi': numpy.pi, 'ellipse': ellipse}

    def parse(self, expr, **kargs):
        # not parsable callback
        def callback_not_parsable(x, kargs):
            raise ValueError('\"{}\" not parsable'.format(x))

        # not callback
        def callback_not(x, kargs):
            # parse not
            return self.unary_parser(x, 'not', numpy.logical_not,
                    callback_not_parsable, kargs)

        # and callback
        def callback_and(x, kargs):
            # parse and
            return self.binary_parser(x, None, 'and', numpy.logical_and,
                    callback_not, kargs)

        # or callback
        def callback_or(x, kargs):
            # parse or
            return self.binary_parser(x, None, 'or', numpy.logical_or,
                    callback_and, kargs)

        # try parse xor
        result = self.binary_parser(expr, None, 'xor', numpy.logical_xor,
                callback_or, kargs)

        # return result
        return result

    def binary_parser(self, x1, x2, keyword, function, callback, kargs):
        # check type of x1
        if isinstance(x1, str):
            expressions = x1.split(keyword)

            # check for length of expressions
            if len(expressions) > 1:
                x1 = self.binary_parser(string.strip(expressions[0]),
                        string.strip(string.join(expressions[1:], keyword)),
                        keyword, function, callback, kargs)

        # check type of x2
        if isinstance(x2, str):
            expressions = x2.split(keyword)

            # check for length of expressions
            if len(expressions) > 1:
                x2 = self.binary_parser(string.strip(expressions[0]),
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
                    x = eval(x, self.globals_, kargs)

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
        return result

    def unary_parser(self, x1, keyword, function, callback, kargs):
        # check type of x1
        if isinstance(x1, str):
            expressions = x1.split(keyword)

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
                    x = eval(x, self.globals_, kargs)
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
        result = function(x1)

        # return
        return result

if __name__ == '__main__':
    expr = 'sin(X) > 0.1'

    X, Y = numpy.meshgrid(numpy.arange(0.0, 1.0, 0.1),
            numpy.arange(0.0, 1.0, 0.1))

    # create parser
    parser = NumpyParser()
    print numpy.where(parser.parse(expr, X=X, Y=Y), 1.0, 0.0)
