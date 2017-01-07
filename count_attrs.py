import os

"""
# 按属性统计词频, 将结果存入counts目录
"""
def count_attr(attr, filename, num=50):
    with open('attrs/%s.txt' % attr) as f:
        # 去掉结尾的换行符
        data = [line.strip() for line in f.readlines()]

    novels = data[::2]
    attrs = data[1::2]

    novel_attrs = {k: v.split() for k, v in zip(novels, attrs)}

    with open('txt/{}.txt'.format(filename), encoding='GBK') as f:
        data = f.read()
    count = []
    for attr in novel_attrs[filename]:
        count.append([attr, data.count(attr)])
    count.sort(key=lambda x: -x[1])

    numbers = [x[1] for x in count[:num]]
    names = [x[0] for x in count[:num]]


    return numbers, names

attrs = ['names', 'places', 'times', 'works']
file_names = os.listdir('./txt')
file_names = [x.strip('.txt') for x in file_names]
out_dirs = ['counts/' + x for x in attrs]
for x in out_dirs :
    if not os.path.exists(x):
        os.makedirs(x)
for filename in file_names:
    for i_attr, attr in enumerate(attrs) :
        n, names = count_attr(attr,filename)
        with open(os.path.join(out_dirs[i_attr], '%s.txt' % filename), 'w') as f2:
            for i in range(len(n)):
                f2.writelines('%s %d\n'%(names[i], n[i]))

