# crfpp-template-generator

## A template generator for crf++.

The crf++ model requires users to write a template for its input features. The template can be quite flexible. For example, users can combine a feature with itself in the previous step, the subsequent step, or even several steps away.

For example, this is a template for word segmentater given by the official example of crf++:

> \# Unigram  
U00:%x[-2,0]  
U01:%x[-1,0]  
U02:%x[0,0]  
U03:%x[1,0]  
U04:%x[2,0]  
U05:%x[-2,0]/%x[-1,0]/%x[0,0]  
U06:%x[-1,0]/%x[0,0]/%x[1,0]  
U07:%x[0,0]/%x[1,0]/%x[2,0]  
U08:%x[-1,0]/%x[0,0]  
U09:%x[0,0]/%x[1,0]  
\# Bigram  
B  

For each character, we can generate a feature named U05, which is a combination of this character and the two characters before it. E.g., for this sentence 'thisisanapple', the U05 feature at step 3 ('s') is h/i/s. Similarly, the U06 feature at step 3 ('s') is i/s/i.

However, **it is extremely tedious and time consuming when we want to add some complex features such as 5-gram or 7-gram** (e.g., in english hashtag segmentation). Therefore, **this generator is designed to help you to easily config your template and add some comments for reference** to our model.

Let's say you have 25 additional features other than the character itself: a feature about whether the character is a digit, 9 features about the prefix of the word, 9 features about the suffix of the word, and 6 features about the transition of a bigram. It doesn't matter if you don't under stand the meaning of my features. Just take them as the names of features.

> 0: char
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

and you want to add 5-gram of features at position 11 (prefix11-b1) as new features to your crf++ model. Your template would be like this:

>U00:%x[-4,11]/%x[-3,11]/%x[-2,11]/%x[-1,11]/%x[0,11]  
U01:%x[-3,11]/%x[-2,11]/%x[-1,11]/%x[0,11]/%x[1,11]  
U02:%x[-2,11]/%x[-1,11]/%x[0,11]/%x[1,11]/%x[2,11]  
U03:%x[-1,11]/%x[0,11]/%x[1,11]/%x[2,11]/%x[3,11]  
U04:%x[0,11]/%x[1,11]/%x[2,11]/%x[3,11]/%x[4,11]  

Adding more complexity, assume you want to add 2\~5 n-grams for all features now, you need to manually config 100+ lines of texts, and it's hard to detect whether you made any mistake. With this generator, you only need to specify the columns (which are the feature positions) and the rows (which are the time steps) you want to iterate, and it will generate the template automatically for you.

	from generator import TemplateGenerator
	generator = TemplateGenerator(3) # the number of lines may be out of range 0~99, so initialize the index with 3 digits
	for k in range(2, 5+1):
        generator.add_n_gram(col_range= [1, 25], row_range = [0-k+1, 0+k-1], n = k) # add 2~5 n-gram for selected column range
    generator.add_n_gram(cols= [0, 2, 5, 8], row_range = [0-7+1, 0+7-1], n = 7) # add 7-gram for selected columns

You can also config the comments for each input feature, so that you can check the template easily.

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
    generator.update_map(feature_map)

Finally, you just need to run the get_template method and export the template.

	template = generator.get_template() 
	with open(output_file, mode = 'w') as f:
        f.write(template)

Full codes of these two hands-on examples are provided in [example.py](https://github.com/heretree/crfpp-template-generator/blob/master/example.py).

