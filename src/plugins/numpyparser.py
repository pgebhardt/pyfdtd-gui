import numpy
import string


class BooleanParser:
    def __init__(self):
        pass

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

        # xor callback
        def callback_xor(x, kargs):
            # parse xor
            return self.binary_parser(x, None, 'xor', numpy.logical_xor,
                    callback_or, kargs)

        # try parse brackets
        result = self.bracket_parser(expr, callback_xor, kargs)

        # return result
        return result

    def bracket_parser(self, expr, callback, kargs):
        # check for opening bracket
        if string.find(expr, '(') != -1:
            print 'opening backet at pos: {}'.format(string.find(expr, '('))

        else:
            # call callback
            return callback(expr, kargs)

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
        result = function(x1)

        # return
        return result

if __name__ == '__main__':
    expr = 'X < 0.5'

    X, Y = numpy.meshgrid(numpy.arange(0.0, 1.0, 0.1), numpy.arange(0.0, 1.0,
        0.1))

    # create parser
    parser = BooleanParser()
    print numpy.where(parser.parse(expr, X=X, Y=Y), 1.0, 0.0)
