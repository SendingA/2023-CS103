import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import jieba

font_path = 'C:\Windows\Fonts\simfang.ttf'  # simplified Chinese font path in Windows
with open('stop_words_CN.txt', 'r', encoding='utf-8') as file:  # add Chinese stop words
    stop_words = [line.strip() for line in file.readlines()]

stopwords = set(STOPWORDS)
stopwords.update(stop_words)


# 准备文本数据
def wordcloud(other_stop_words, text, save_path):
    # text = "Hello Hello World World World World World World World World World World World Hi I"
#     text = '''要将一段文字以柱状图的形式可视化出现频率最多的五个词，你可以按照以下步骤进行操作：\\
#
# 文字预处理：首先，你需要对给定的文字进行预处理。这包括去除标点符号、特殊字符和多余的空格，并将所有的字母转换为小写（如果适用）。\\
#
# 分词：将文字分割成单词或词组。对于中文，你可以使用中文分词工具，如结巴分词或哈工大LTP。对于英文，可以使用空格或标点符号进行分割。
#
# 统计词频：统计每个词在文字中出现的频率。你可以使用字典（或哈希表）来记录每个词及其对应的频率。
#
# 选择频率最高的五个词：根据词频从高到低对词进行排序，并选择出现频率最高的五个词。
#
# 可视化：使用柱状图库（如Matplotlib）或数据可视化工具来绘制柱状图。将频率最高的五个词作为水平轴，将它们的出现频率作为垂直轴，通过柱状图形式展示出来。
# Hello Hello World World World World World World World World World World World'''
    # 创建词云对象
    list1 = jieba.lcut(text)
    # print(list1)
    sentence = " ".join(list1)
    stopwords.update(other_stop_words)
    # print(sentence)
    wordcloud = WordCloud(font_path=font_path, width=800, height=400, background_color='white', stopwords=stopwords).generate(sentence)

    # 绘制词云图
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(save_path)

    # 显示图形
    plt.show()


# wordcloud([],'', '')
