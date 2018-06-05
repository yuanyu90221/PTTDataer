
'''
wordcloud
'''

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from collections import Counter
from wordcloud import WordCloud,ImageColorGenerator
file_path = '/home/linsam/github/Crawler_and_Share'
import jieba.analyse

os.chdir(file_path)
sys.path.append(file_path)
import LoadPttData
jieba.set_dictionary("dict_tw.txt")
font = os.path.join( "/home/linsam/github/Crawler_and_Share/simfang.ttf")

alice_coloring = np.array(Image.open("/home/linsam/github/Crawler_and_Share/alice_color.png"))

class PTTWordCloud:
    def __init__(self,data_name,percent,var_name):
        #self.all_data_table_name = LoadPttData.all_data_table_name
        self.data_name = data_name
        self.LPD = LoadPttData.LoadPttData()
        self.percent = 1 - percent
        self.var_name = var_name
    def load_ptt_data(self):
        
        data_id = self.LPD.load(self.data_name,['id'])
        
        start = data_id['id'][ int( len(data_id)*self.percent ) ]
        end = data_id['id'][len(data_id)-1]
        self.data = self.LPD.load_by_id(self.data_name,
                                        self.var_name,
                                        start,
                                        end)
    def stop_words(self):
        #path = '/home/linsam/github/Crawler_and_Share/jieba/extra_dict/'
        #os.listdir()
        #for p in path:
        stopwords = pd.read_csv('stop_words.txt', 
                                index_col=False, 
                                quoting=3, 
                                sep="\t", 
                                names=['stopword'],
                                encoding='utf-8')  # quoting=3全不引用        
        self.stops = stopwords['stopword'].tolist()
        [self.stops.append(tex) for tex in ['\n','\\n','\u3000','','PTT'] ]
        stop = ['什麼','現在','這樣','覺得','還是','自己','沒有','我們','真的','一個','這麼','因為','']
        for tex in stop:
            self.stops.append(tex) 
            
    def get_topk_tags(self,var):
        self.new_data = []
        for da in self.data[var]:# var = 'clean_article'
            self.new_data.append( da )
        
        self.topk_tags = []
        for i in range(len(self.new_data)):
            print(str(i)+'/'+str(len(self.new_data)))
            tags = jieba.analyse.extract_tags(self.new_data[i])
            #seg_generator = jieba.cut(new_data[i])
            for tag in tags:
                self.topk_tags.append(tag)
                # Counter(self.topk_tags)
    def get_words(self):
        self.new_data = []
        for da in self.data[self.var_name]:
            self.new_data.append( da )
        data = ''
        for da in self.new_data:
            data = data + da
        
        cut_text = jieba.cut(data)
        self.words = (' '.join( set( cut_text )-set( self.stops ) ) )
    def work_wordcloud(self):
        123
    def main(self):
        self.load_ptt_data()
        self.stop_words()
        self.get_words()
        #
           
'''

self = PTTWordCloud('Salary',0.2,['clean_article','author'])
self.load_ptt_data()

Counter( self.data['author'] ).most_common()[:5]


self.data = self.data[ self.data['author'] == 'sumade' ]
self.stop_words()
self.get_words()
self.get_topk_tags('clean_article')

#------------------------------------------------------
self = PTTWordCloud('Salary',0.02,['clean_article'])
self.main()
self.get_topk_tags('clean_article')

'''

stop = ['什麼','現在','這樣','覺得','還是','自己','沒有','我們','真的','一個','這麼','因為','']
for tex in stop:
    self.stops.append(tex) 
    
cloud = WordCloud(
    font_path = font,#设置字体，不指定就会出现乱码
    background_color = 'white',#设置背景色
    max_words = 100,#允许最大词汇
    mask = alice_coloring,#词云形状
    stopwords = self.stops,# 使用内置的屏蔽词，
    
    max_font_size = 100#最大号字体
)

x = Counter(self.topk_tags)
x = dict(x)

cloud.generate_from_frequencies(x)

# create coloring from image
image_colors = ImageColorGenerator(alice_coloring)

plt.figure( figsize=(30,15) )
plt.imshow(cloud)












