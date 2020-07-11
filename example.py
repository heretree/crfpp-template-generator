import os
import sys
import argparse
from codecs import open
from generator import TemplateGenerator


def generate_seg(output_file):
    """
    #   Assume we want to generate the template of CRF++'s official example 'seg'

    #     # Unigram
    #     U00:%x[-2,0]
    #     U01:%x[-1,0]
    #     U02:%x[0,0]
    #     U03:%x[1,0]
    #     U04:%x[2,0]
    #     U05:%x[-2,0]/%x[-1,0]/%x[0,0]
    #     U06:%x[-1,0]/%x[0,0]/%x[1,0]
    #     U07:%x[0,0]/%x[1,0]/%x[2,0]
    #     U08:%x[-1,0]/%x[0,0]
    #     U09:%x[0,0]/%x[1,0]

    #     # Bigram
    #     B
    """

    

    ### print out the template
    generator = TemplateGenerator()
    line_list = []
    line_list += generator.generate_n_gram(cols = [0], row_range = [-2, 2], n = 1) # U00~U04
    line_list += generator.generate_n_gram(cols = [0], row_range = [-2, 2], n = 3) # U05~U07
    line_list += generator.generate_n_gram(cols = [0], row_range = [-1, 1], n = 2) # U08~U09
    print('\n'.join(line for line in line_list))

    ### output template file
    generator = TemplateGenerator()
    generator.add_n_gram(cols = [0], row_range = [-2, 2], n = 1)
    generator.add_n_gram(cols = [0], row_range = [-2, 2], n = 3)
    generator.add_n_gram(cols = [0], row_range = [-1, 1], n = 2)
    template = generator.get_template()
    with open(output_file, mode = 'w') as f:
        f.write(template)
    return 


def generate_template_with_comment(output_file):
    """

        Sometimes we have too many features and the combinations of features are too complecated that we need some comments for reference.
        It can be achieved by config a feature map in this generator. 
        In the example below, we show a model with 25 features:

        0: char
        1: is_digit
        2: suffix1-b1
        3: suffix1-b2
        4: suffix1-b3
        5: suffix2-b1
        6: suffix2-b2
        7: suffix2-b3
        8: suffix3-b1
        9: suffix3-b2
        10: suffix3-b3
        11: prefix1-b1
        12: prefix1-b2
        13: prefix1-b3
        14: prefix2-b1
        15: prefix2-b2
        16: prefix2-b3
        17: prefix3-b1
        18: prefix3-b2
        19: prefix3-b3
        20: transition1-b1
        21: transition1-b2
        22: transition1-b3
        23: transition2-b1
        24: transition2-b2
        25: transition2-b3

        and we also want to add some variations of these features to the template. E.g., for the 11th feature prefix1-b1, we want to 
        combine it with it's previous step and subsequent step to be %x[-1, 11]/%x[0, 11]/%x[1, 11]
    """

    generator = TemplateGenerator(3) # the number of lines may be out of range 0~99, so initialize the index with 3 digits

    # define your own comment map
    feature_map = {}
    feature_map[0] = 'char'
    feature_map[1] = 'is_digit'
    idx = 1
    for mode in ['suffix', 'prefix', 'transition']:
        for length in range(1, 3+1):
            for bar in range(1, 3+1):
                if (mode == 'transition') & (length == 3):
                    continue
                idx += 1
                feature_map[idx] = '{}{}-b{}'.format(mode, length, bar)
    
    # print out the map for checking
    for idx in sorted(feature_map.keys()):
        print('{}: {}'.format(idx, feature_map[idx]))
    # update the feature map
    generator.update_map(feature_map)

    # config your template
    generator.add_n_gram(col_range = [0, 1], row_range = [-2, 2], n = 1) # add unigram by range of column
    
    cols = [2, 5, 8, 11, 14, 17, 20, 23]
    generator.add_n_gram(cols = cols, row_range = [0, 0], n = 1) # add unigram of selected columns
    
    for k in range(2, 5+1):
        generator.add_n_gram(cols = cols, row_range = [0-k+1, 0+k-1], n = k) # add 2~5 n-gram of selected columns

    template = generator.get_template()
    
    with open(output_file, mode = 'w') as f:
        f.write(template)

    return

def main():
    parser = argparse.ArgumentParser(description='Test.', \
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--output_folder", help="output_folder")
    args = parser.parse_args()
    generate_seg(args.output_folder + '/template_seg')
    generate_template_with_comment(args.output_folder + '/template_customized')
    return 0

if __name__ == '__main__':
    sys.exit(main())