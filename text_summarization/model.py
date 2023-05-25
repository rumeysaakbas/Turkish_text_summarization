import pandas as pd #to read csv files
import random 
import numpy as np #handle operations on arrays easily
import nltk
from nltk import sent_tokenize
from collections import Counter
import os
import pandas as pd
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics


# csv dosyasından tüm satırları okuyarak bir tablo oluşturuyoruz
dataset = pd.read_csv("C:/Users/PC/Desktop/text_summarization_dataset/7all.csv", encoding='utf-8', delimiter=',', names=["cat", "text"])




# her kategoride kaç satır olduğunu hesaplıyoruz
cats = dataset.groupby("cat").size()




# Kelime frekanslarını buluyoruz (her kelimenin metinde kaç kez geçtiği)
all_words = []
for idx,rows in dataset.iterrows():
    text = rows.text
    all_words.extend(text.split(" "))
words_freq = Counter(all_words)




# stopwordleri okuyoruz
filesw = "C:/Users/PC/Desktop/text_summarization_dataset/stop-words.txt"
with open(filesw, "r") as file1:
    stopwords = file1.read()
    #print(FileContent)
#print(len(stopwords))





#string of all turkish characters 
turkishCharaters = "abcçdefgğhıijklmnoöprsştuüvyz_"
#function use the 'turkishCharaters' list to eliminate symbols and strange characters.
def RealWord(string):
    if not any(c not in turkishCharaters for c in string):
        return True
    else:
        return False




# Temizlemeye başlayalım!
# 1- 'words_freq' sözlüğündeki frekansı eşik değerinden büyük olan kelimeleri çıkaralım
# 2- Yukarıdaki araçları kullanarak kelimeleri ve karakterleri filtreleyelim.
#we will remove all words that has low frequency 
threshold = 30
words_freq = dict(filter(lambda x: x[1]>threshold, words_freq.items()))
#take all words from the dict
words = list(words_freq.keys())
#remove stop words.
filtered_words = [w for w in words if not w in stopwords]
#remove non turkish characters.
filtered_words = list(filter(RealWord, filtered_words))[1:]
#print("the number of words is",len(filtered_words),"word, after we cleaned it.")
#print("-"*50)
#print(filtered_words)





#Şimdi önceki word_freq kodumuza geri dönebilir ve temizlenmiş kelimelerimizin frekanslarını görebiliriz
#we just need to filter it with our new keys(filterd words)
new_freq = dict(filter(lambda x: x[0] in filtered_words, words_freq.items()))
#just sort words dict according to its frequencies 
new_freq = dict(sorted(new_freq.items(), key=lambda x: x[1], reverse=True))
#print(new_freq)




# Kelimeleri temizledik ve bunları "filtered_words" listesinde sakladık.Şimdi verisetinin tüm metinlerine TD algoritmasını uygulayacağız:
# Her bir metin için: < -- DÖNGÜ
# 1- İlk vektörü oluşturun [01,02,...0n] <===> filtered_words [w1,w2...Wn]
# 2- Metin kelimelerini döngüyle dolaşın. İlk vektörü ([0,0....0] ==> [1,3,0,0,5..1]) güncelleyin.
# 3- İlk vektörü all_vectors listesine kaydedin.
# Amaç, her kelimeyi metinde kaç kez geçtiğine karşılık gelen bir sayıyla değiştirmektir.

init_vector = [0]*len(filtered_words)





#[0,0,0....0] ==> [1,4,2....2]
def create_vector(text):
    words_of_text = text.split(" ")
    text_vector = [0]*len(init_vector)
    for word in words_of_text:
        if word in filtered_words:
            idx = filtered_words.index(word)
            text_vector[idx] += 1
    return text_vector
all_vectors = []
#loop through all texts
for idx,row in dataset.iterrows():
    text = dataset.loc[idx, "text"]
    all_vectors.append(create_vector(text))





# Tüm metinler için vektörler oluşturduk ve bunları "all_vectors" içinde grupladık. Şimdi "all_vectors" üzerinde NİTELİKLİ (SUPERVISED) makine öğrenimi modelini eğiteceğiz:
# Nitelikli, girdileri çıktılara eşleme anlamına gelir (X => Y). Girdilerimiz "all_vectors" olduğunu ve "dataset"e (CSV dosyasına) baktığımızda her satırın ("text", "cat") olduğunu görüyoruz, bu yüzden her satırın kategorisini etiket olarak alabilirsiniz.
# Bu durumda eşleme işlevi şöyle olacaktır: Her bir (vektor all_vectors içinde && ("text", "cat") dataset içinde ise):
# 1.model_dataset.add(vector, cat)
labels = dataset["cat"].tolist()
model_dataset = list(zip(all_vectors,labels))




# Şimdi "model_dataset"i karıştıracağız ve kümeleri eğitmek ve test etmek için böleceğiz
model_dataset_shuf = shuffle(model_dataset)
all_vectors_shuf,labels_shuf = zip(*model_dataset_shuf)

data_length = len(all_vectors)
train_x,train_y = all_vectors_shuf[:int(data_length*2/3)],labels_shuf[:int(data_length*2/3)]
test_x,test_y = all_vectors_shuf[int(data_length*2/3):],labels_shuf[int(data_length*2/3):]

print("total data size:",data_length)
print("Train data size:",len(train_x))
print("Test data size:",len(test_x))




# Eğitmeye hazırız!
# Sadece bir model seçmemiz gerekiyor, biz rastgele orman (random forest) modelini seçtik.

print ("Training the random forest...")
# Initialize a Random Forest classifier with 100 trees
forest = RandomForestClassifier(n_estimators = 100) 
# This may take a few minutes to run
forest = forest.fit( train_x, train_y )
print("training is finished.")




# Şimdi doğruluğuna bir göz atalım ve modelin verilerden bir şey öğrenip öğrenmediğini görelim.
def cal_acc(set_x,set_y):
    results = forest.predict(set_x)
    cnf_matrix = metrics.confusion_matrix(set_y, results)
    sim = 0
    for i in range(len(results)):
        if set_y[i] == results[i]:
            sim += 1
    return round(sim/len(results),2)
train_accuracy = cal_acc(train_x,train_y)
test_accuracy = cal_acc(test_x,test_y)

print("train accurcy:", train_accuracy)
print("test accurcy:", test_accuracy)

# Hem eğitim hem de test veri setleri üzerinde iyi bir doğruluk elde ettik. İnternetten aldığımız bir metinle denedik ve modelin doğru tahmin yaptığını gözlemledik.
# Artık metinlerin kategorisini tahmin eden bir modele sahibiz.