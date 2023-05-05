import jieba
import wordcloud
import matplotlib.pyplot as plt

# plt.rcParams['font.sans-serif'] = ['FangSong'] # 步骤一（替换sans-serif字体）
# plt.rcParams['axes.unicode_minus'] = False   # 步骤二（解决坐标轴负数的负号显示问题）


with open('/home/cidi/Documents/第一党支部 党务工作/20221215-年度组织生活会日/2022年12月-组织生活会会前征求意见-收集完成/wordcloud.txt', 'r') as f:
    words = f.read()

word_list = jieba.lcut(words)   # 结巴词库切分词
word_list = [word for word in word_list if len(word.strip())>1]#清洗一个字的词
word_clean=" ".join(word_list)
import imageio
# mask=imageio.imread(r'kobe.jpg')
wc = wordcloud.WordCloud(font_path='/home/cidi/Downloads/simsun/SIMSUN.ttf',
                        width=800, height=400,
                        background_color = "white",#指定背景颜色
                        max_words = 200,  # 词云显示的最大词数
                        max_font_size = 255  #指定最大字号
                        )
                        # mask = mask) #指定模板
wc = wc.generate(word_clean)##生成词云
plt.imshow(wc)
plt.axis("off")
plt.show()
"""Wordcloud详细参数设置
def __init__(self, font_path=None, width=400, height=200, margin=2,
    ranks_only=None, prefer_horizontal=.9, mask=None, scale=1,
    color_func=None, max_words=200, min_font_size=4,
    stopwords=None, random_state=None, background_color='black',
    max_font_size=None, font_step=1, mode="RGB",
    relative_scaling='auto', regexp=None, collocations=True,
    colormap=None, normalize_plurals=True, contour_width=0,
    contour_color='black', repeat=False,
    include_numbers=False, min_word_length=0):
"""