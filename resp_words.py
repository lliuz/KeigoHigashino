import os

"""
# 在filters的基础上人肉过滤错误属性, 放在refiltered目录下
# 把所有属性制成自定义词库./wordslist.txt，为准备重新分词进一步提高分词性能
# 把所有属性整理按作品名写入attrs目录
"""

def process(words_f, in_dir='./txt', out_file='./attrs.txt', ):
    file_names = os.listdir(in_dir)
    file_names = [x.strip('.txt') for x in file_names]
    for file_name in file_names :
        print("处理：%s" %file_name)
        f = open(os.path.join(in_dir, '%s.txt' % file_name))
        f2 = open(os.path.join(out_file), 'a')
        f2.writelines(file_name+'\n')
        for line in  f:
            line = line.strip()
            if len(line) > 0:
                t = line.split(' /')
                if len(t)<2:
                    print(t)
                f2.writelines(t[0]+' ')
                words_f.writelines('%s %s %d\n'%(t[0],t[1].split(' ')[0],999))
            else :
                break
        f2.writelines('\n')

attrs = ['names', 'places', 'times', 'works']
in_dirs = ['refiltered/' + x for x in attrs]
words_file = './wordslist.txt'
words_f = open(os.path.join(words_file), 'a')
for in_dir in in_dirs:
    process(words_f, in_dir=in_dir, out_file='attrs/%s.txt'%in_dir.split('/')[1])




