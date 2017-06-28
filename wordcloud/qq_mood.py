#coding:utf-8
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator,STOPWORDS
import jieba
import numpy as np
from PIL import Image

#读入背景图片
abel_mask = np.array(Image.open("qq.jpg"))

#读取要生成词云的文件
text_from_file_with_apath = open('mood.txt',encoding='utf-8').read()

#通过jieba分词进行分词并通过空格分隔
wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all = True)
stopwords = {'转载','内容','em','评语','uin','nick'}
seg_list = [i for i in wordlist_after_jieba if i not in stopwords]
wl_space_split = " ".join(seg_list)
#my_wordcloud = WordCloud().generate(wl_space_split) 默认构造函数
my_wordcloud = WordCloud(
            background_color='black',    # 设置背景颜色
            mask = abel_mask,        # 设置背景图片
            max_words = 250,            # 设置最大现实的字数
            stopwords = STOPWORDS,        # 设置停用词
            font_path = 'C:/Windows/fonts/simkai.ttf',# 设置字体格式，如不设置显示不了中文
            max_font_size = 42,            # 设置字体最大值
            random_state = 40,            # 设置有多少种随机生成状态，即有多少种配色方案
                scale=1.5,
            mode='RGBA',
            relative_scaling=0.6
                ).generate(wl_space_split)

# 根据图片生成词云颜色
#image_colors = ImageColorGenerator(abel_mask)
#my_wordcloud.recolor(color_func=image_colors)

# 以下代码显示图片
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()

my_wordcloud.to_file("cloud.jpg")