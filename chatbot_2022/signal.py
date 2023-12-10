import itchat as it
it.auto_login(hotReload=True)    #热启动，不需要多次扫码登录

it.login()
friends=it.get_friends(update=True)[0:]
print(type(friends))
#性别
dict_sex=dict()
dict_sex[0]=0#未知
dict_sex[1]=0#男
dict_sex[2]=0#女
#省份
dict_province=dict()
for user in friends:
    print()
    print('user.NickName:',user.NickName)
    print('user.Sex:', user.Sex)
    print('user.Province:', user.Province)
    print('user.City:', user.City)
    print('user.Signature:',user.Signature)
    dict_sex[user.Sex] = dict_sex[user.Sex] + 1
    if dict_province.keys().__contains__(user.Province):
        dict_province[user.Province]=dict_province[user.Province]+1
    else:
        dict_province[user.Province]=1
#性别统计结果
print()
print('none:',dict_sex[0])
print('male:',dict_sex[1])
print('female:',dict_sex[2])
#省份统计结果
print(dict_province)

#出去特殊字符
import re
siglist = []
for i in friends:
    signature = i["Signature"].strip().replace('span','').replace('class','').replace('emoji','').replace('\n','')
    rep = re.compile("1f\d+\w*|[<>/=]")
    signature = rep.sub("", signature)
    siglist.append(signature)
text = "".join(siglist)
#分词
import jieba
wordlist = jieba.cut(text, cut_all=True)
word_space_split = " ".join(wordlist)
print(word_space_split)
#绘制词云
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import PIL.Image as Image
coloring = np.array(Image.open("./老帅.jpeg"))#自定义词云的图片

my_wordcloud = WordCloud(background_color="white", max_words=1500,
                         mask=coloring, max_font_size=60, font_path='/Library/Fonts/Arial Unicode.ttf',random_state=42,scale=2).generate(word_space_split)#wget http://labfile.oss.aliyuncs.com/courses/756/DroidSansFallbackFull.ttf中文字符文件

image_colors = ImageColorGenerator(coloring)
plt.imshow(my_wordcloud.recolor(color_func=image_colors))
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()