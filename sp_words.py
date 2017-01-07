from jpype import *
import os
import re
from collections import Counter
startJVM('/opt/JAVA/jdk1.8.0_71/jre/lib/amd64/server/libjvm.so', "-Djava.class.path=./lib/hanlp-1.3.2-release/hanlp-1.3.2.jar:./lib/hanlp-1.3.2-release/")

"""
# 利用hanlp进行分词
# 因为hanlp的分词结果对人名地名分割效果较好，而jieba分词对整体分词效果较好，因此先用hanlp分词得到一些关键属性(人名地名等)
# 对所有的小说进行分词保存在cuts. 保存的是分词的原始结果，若需要得到单词的list可以用re.findall('[\u2E80-\u9FFF]{1,}',a)
# 并用正则表达式找出每本小说的有关属性保存在filters文件夹内
"""

# Initial hanlp
HanLP = JClass('com.hankcs.hanlp.HanLP')
segmentor = HanLP.newSegment().enableJapaneseNameRecognize(True)

# Cut words for given filename of .txt file, write result into out_dir and filter attributes to filter_dirs
def cut_words(filename, in_dir='./txt', out_dir='', filter_dirs=[''], reexs=[]):
    with open(os.path.join(in_dir, '%s.txt' % filename), encoding='GBK') as f:
        print("处理：%s" %filename)

        texts = f.read()

        cuts = segmentor.seg2sentence(texts).toString()
        with open(os.path.join(out_dir, '%s.txt' % filename), 'w') as fcut:
            fcut.write(cuts)

        filtered = []
        counters = []
        for p in reexs :
            t = re.findall(p,cuts)
            filtered.append(t)  #
            counters.append(Counter(t))

        # write each attribute into file
        for out_id,x in enumerate(counters):
            with open(os.path.join(filter_dirs[out_id], '%s.txt' % filename), 'w') as f2:
                for line in list(x.most_common(100)) :
                    idx = cuts.find(line[0])
                    f2.writelines(line[0].replace('/',' /')+' %d\t %s\n'%(line[1],cuts[idx-8:idx+len(line[0])+8]) )


file_names = os.listdir('./txt')
file_names = [x.strip('.txt') for x in file_names]
cut_dir = './cuts'
out_dirs = ['filters/names', 'filters/places', 'filters/times', 'filters/works']
for x in out_dirs :
    if not os.path.exists(x):
        os.makedirs(x)

for file_name in file_names :
    cut_words(file_name,out_dir=cut_dir,filter_dirs=out_dirs,
              reexs=['[\u2E80-\u9FFF]{1,}/nr',
                     '[\u2E80-\u9FFF]{1,}/ns',
                     '[\u2E80-\u9FFF]{1,}/t' ,
                     '[\u2E80-\u9FFF]{1,}/nn'])

