class TemplateGenerator(object):
    def __init__(self, num_digits = 2):
        self.idx = -1
        self.num_digits = num_digits #number of digits in self.idx
        self.feature_map = {}
        self.template = {'unigram': ['# Unigram'], 'bigram': ['# Bigram', 'B']}
        self.output = ''
        return

    def generate_index(self):
        self.idx += 1
        if self.idx > int('9'*self.num_digits):
            raise Exception("The template index {} has been out of range {}-{}.".format(self.idx, 0, int('9'*self.num_digits)))
        idx = self.idx
        idx = str(idx).zfill(self.num_digits)
        return idx

    def update_map(self, new_map):
        self.feature_map = new_map
        return


    def generate_n_gram(self, col_range = None, row_range = [0, 0], n = 1, cols = None):
        """
        col_range: List of Int. Inclusive. Range of featrures are considered.
        row_range: List of Int. Inclusive. Range of time period among the current step. Consider
                the last and next time step if it's set to [-1, -1]
        n: Int. The number of characters of n-gram. Default 1.
        """
        if (row_range[1] - row_range[0] + 1) < n:
            raise Exception('Cannot find a {}-gram in range [{}, {}]'.format(n, row_range[0], row_range[1]))
        if (not col_range) and (not cols):
            raise Exception('Please specify col_range or cols to iterate.')
        if not cols:
            cols = range(col_range[0], col_range[1]+1)

        output = []
        for col in cols:
            for top_row in range(row_range[0], row_range[1]-n+2):
                gram_list = []
                for x in range(top_row, top_row+n):
                    gram_list.append('%x[{},{}]'.format(str(x), str(col)))
                line = 'U{}:'.format(self.generate_index()) + '/'.join(gram_list)
                if self.feature_map.get(col):
                    line += ' #NG{}:{}'.format(n, self.feature_map[col])
                output.append(line)
        return output

    def add_n_gram(self, col_range = None, row_range = [0, 0], n = 1, cols = None, to_unigram = True):
        if to_unigram:
            self.template['unigram'] += self.generate_n_gram(col_range, row_range, n, cols)
        else:
            self.template['bigram'] += self.generate_n_gram(col_range, row_range, n, cols)
        return

    def get_template(self):
        output = ''
        output += '\n'.join(x for x in self.template['unigram'])
        output += '\n\n'
        output += '\n'.join(x for x in self.template['bigram'])
        self.output = output
        return self.output



