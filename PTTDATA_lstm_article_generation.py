

from PTTData import Load as PTT
import numpy as np
import jieba
import re
import datetime
import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.callbacks import Callback
import pandas as pd
import random

article_amount = 10
maxlen = 20
step = 3
lstm_dimension = 128
lr = 0.01
batch_size = 128
epochs = 10
drop = 0.2

''' function '''
def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def auto_article_article(diversity,
                         sentence,n,
                         chars,maxlen,char_indices,
                         indices_char,model):
    #print('----- diversity:', diversity)
    generated = ''
    generated += ''.join( sentence )
    for i in range(n):
        #print('{}\{}'.format(i,n))
        x_pred = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
            x_pred[ 0, t, char_indices[char] ] = 1.

        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_char = indices_char[next_index]
        #print(next_char)
        generated += next_char
        #sentence2 = ''.join( sentence[1:] ) + next_char
        sentence = sentence[1:]
        sentence.append( next_char )
    #auto_article = generated + ''.join(sentence)
    #print('----------------------------------------------')
    #print(generated)
    #print('----------------------------------------------')
    return generated

def jieba_cut_word(article_amount,data):
    article_list = []
    for i in range(article_amount):
        if i%100 == 0 : print('{}/{}'.format(i,article_amount))
        tem = data['article'][i]
        
        # replace english
        r1 = '[a-zA-Z0-9’"#$%&\'()*+-./:;<=>?@★、…【】：「」《》“”‘’！[\\]^_`{|}~]+'
        tem = re.sub(r1, '', tem)
        if str( type(tem) ) != "<class 'NoneType'>" and tem != '' and tem != ' ':
            seg_list = jieba.cut(tem)  
            value = " ".join(seg_list)
            article_list.append(value)
    #article = " ".join(article_list).replace('\n','')
    article = " ".join(article_list).replace('\n','').replace('\\','').split(' ')
    print('corpus length:', len(article))
    return article

def word2int(article):
    chars = sorted(list(set(article)))
    print('total chars:', len(chars))
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))
    return char_indices,indices_char,chars

def get_sentences_and_next_chars(article,maxlen,step):
    sentences = []
    next_chars = []
    for i in range(0, len(article) - maxlen, step):
        sentences.append(article[i: i + maxlen])
        next_chars.append(article[i + maxlen])
    
    print('nb sequences:', len(sentences))
    return sentences,next_chars

def vectorization(sentences,maxlen,chars,char_indices,next_chars):
    x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
    y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            x[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]] = 1
    return x,y

def build_model(lstm_dimension ,lr,maxlen,chars,drop ):
    model = Sequential()
    #model.add(LSTM(128, input_shape=(maxlen, len(chars))))
    model.add(LSTM(
            lstm_dimension, input_shape=(maxlen, len(chars)),
            dropout=drop, recurrent_dropout=drop
            ))
    model.add(Dense(len(chars), activation='softmax'))
    # model.summary()
    optimizer = RMSprop(lr=lr)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    return model

def model_fit(model,x,y,batch_size = 1024,epochs = 40):
    s = datetime.datetime.now()
    log = Callback()
    his = model.fit(x, y,
                    batch_size = batch_size,
                    epochs = epochs,
                    verbose=1, 
                    callbacks=[log], 
                    validation_split=0.1, 
                    )
    t = datetime.datetime.now() - s
    t = str(t).split('.')[0]
    print('cost time {} '.format( t ) )# 21:34:00
    tem = his.history
    loss = str( tem['loss'][len(tem)] )[:5]
    val_loss = str( tem['val_loss'][len(tem)] )[:5]
    his_data = pd.DataFrame()
    his_data['loss'] = tem['loss']
    his_data['val_loss'] = tem['val_loss']
    return model,t,loss,val_loss,his_data

def auto_write_article(article,n,chars,maxlen,char_indices,indices_char,model):
    #n = 100
    start_index = random.randint(0, len(article) - maxlen - 1)
    sentence = article[start_index: start_index + 20]
    #print( 'input : {}'.format( ''.join(sentence) ) )
    diversity = [0.2, 0.5, 1.0, 1.2]
    ai_article = pd.DataFrame()
    ai_article['diversity'] = diversity
    _output = []
    for div in diversity:
        value = auto_article_article(div,sentence,n,
                                     chars,maxlen,char_indices,
                                     indices_char,model)
        _output.append(value)
    _input = ''.join(sentence) 
    
    ai_article['output'] = _output
    ai_article['input'] = _input
    
    return ai_article

#------------------------------------------------------------
''' main '''
print('load data')
data = PTT.LoadData(table = 'Japan_Travel',date = '2018-04-01',
                     select = 'article',article_type = '遊記')
print('cut word from article by jieba')
article = jieba_cut_word(article_amount,data)

print(' word to int, we will translates int to vectors')
char_indices,indices_char,chars = word2int(article)

# cut the text in semi-redundant sequences of maxlen characters
# perd next chars
print(' build sentences(x) and next_chars(y) ')
sentences,next_chars = get_sentences_and_next_chars(article,maxlen,step)

print('Vectorization, int to vectors')
x,y = vectorization(sentences,maxlen,chars,char_indices,next_chars)

# build the model: a single LSTM
print('Build model...')
model = build_model(lstm_dimension = lstm_dimension,
                         lr = lr,maxlen = maxlen,chars = chars,
                         drop = drop)
print('fit model...')
model,t,loss,val_loss,his_data = model_fit(model = model,
                         x = x,y = y,
                         batch_size = batch_size,
                         epochs = epochs)
print('loss : ')
print(his_data)
print('ai wrtie article')
ai_article = auto_write_article(
        article = article,n = 50,
        chars = chars,maxlen = maxlen,
        char_indices = char_indices,indices_char = indices_char,
        model = model)

for i in range(len(ai_article)):
    print('input : {}'.format( ai_article.loc[i,'input'] ))
    print('diversity : {}'.format( ai_article.loc[i,'diversity'] ))
    print('output : {}'.format( ai_article.loc[i,'output'] ))
    print('----------------------------------------------')

print('save model')
model.save('PTT_auto_article.h5' )


