import os
import re
import gensim
import jieba

"""
# 把hanlp得到的专业名词加入词库，利用jieba重新分词
# 分词结果利用gensim包训练word2vec模型, 将单词转换到向量空间
# 实现按单词找最近邻单词、按单词对找最近邻单词对的功能
"""

def get_attr(attr):
    with open('attrs/%s.txt' % attr) as f:
        # 去掉结尾的换行符
        data = [line.strip() for line in f.readlines()]

    novels = data[::2]
    attrs = data[1::2]
    all_attrs = []
    novel_attrs = {k: v.split() for k, v in zip(novels, attrs)}
    for attr in attrs:
        all_attrs.extend(attr.split())
    return novel_attrs, all_attrs


def find_words_nn(words):
    print('与%s相近的人物'%words[0])
    n = 0
    for k, s in model.most_similar(positive=words, topn=100):
        if k in all_names and n <5:
            print (k, s)
            n += 1


def find_relationship(a, b, c, novelname):
    """
    返回 d
    a与b的关系，跟c与d的关系一样
    """
    for k,s in model.most_similar(positive=[c, b], negative=[a], topn=100):
        if k in novel_names[novelname]:
            print("给定“{}”与“{}”，“{}”和“{}”有类似的关系".format(a, b, c, k))


novel_names,all_names = get_attr('names')
file_names = os.listdir('./txt')
file_names = [x.strip('.txt') for x in file_names]
cuts_dir = './cuts'

wordlist = []
with open('./wordslist.txt') as f:
    for line in f:
        word = line.split()[0]
        wordlist.append(word)
    for word in list(set(wordlist)):
        jieba.add_word(word)

sentences = []

for novel in file_names:
    print ("处理：{}".format(novel))
    if os.path.exists('recut/{}.txt'.format(novel)):
        with open('recut/{}.txt'.format(novel),'r') as f2:
            text = f2.read()
            words = re.findall('[\u4E00-\u9FA5]{1,}',text)
            if len(words) > 0:
                sentences.append(words)
        continue
    with open('txt/{}.txt'.format(novel), encoding='GBK') as f:
        data = [line.strip() for line in f.readlines() if line.strip()]
    with open('recut/{}.txt'.format(novel),'w') as f2:
        for line in data:
            cuts = jieba.cut(line)
            text = '/'.join(cuts)

            words = re.findall('[\u4E00-\u9FA5]{1,}',text)
            f2.write('/'.join(words)+'/')
            if len(words) > 0:
                sentences.append(words)

model = gensim.models.Word2Vec(
    sentences, size=300, window=5, min_count=20, workers=8)
model.save('word2vec2.model')
#model = gensim.models.Word2Vec.load('word2vec2.model')

# 找最近邻单词
find_words_nn(['雪穗'])
find_words_nn(["加贺恭一郎", "加贺"])

# 查找相互关系
find_relationship("麻由子", "崇史", "雪穗", "白夜行")
