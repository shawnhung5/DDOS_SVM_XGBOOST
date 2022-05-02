from sklearn import svm
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pickle
import time
from sklearn import metrics

def sss(i):
    h = int(i/3600)
    i = int(i%3600)
    m = int(i/60)
    s = int(i%60)
    return(h,m,s)

Savemodel='rbfModel-0-6-FO-280000N10-100.pickle'
#df_data=pd.read_csv('train-data/datab-0-5-FO-250000N24.csv')
df_data=pd.read_csv('train-data/datab-0-6-FO-280000N10.csv')

df_data = df_data.sample(n=len(df_data) ,random_state=75,replace=False, axis=0)#亂數
print(df_data)

df_data = df_data.dropna()#移除缺失值

X = df_data.drop(labels=['label'],axis=1).values 
# checked missing data
#print("checked missing data(NAN mount):",len(np.where(np.isnan(X))[0]))
print(X)

y=df_data['label'].values
print(y)


t1 = time.time()#開始時間

#使用高斯(RBF)核函數進行模型訓練
rbfModel=svm.SVC(kernel='rbf', gamma=0.4, C=1)
rbfModel.fit(X, y)
t2 = time.time()#訓練完成時間
t3 = t2-t1


predicted = rbfModel.predict(X)#預測結果
accuracy = rbfModel.score(X, y)#模型準確率
t4 = time.time()#測試完成時間
t5 = t4-t2
print('模型預測結果:',predicted)

true = []
for i in range(y.shape[0]):
  if y[i] == 'normal':
    true.append(2)
  elif y[i] == 'slowloris':
    true.append(1)
  elif y[i] == 'slow post':
    true.append(1)
  elif y[i] == 'slow read':
    true.append(1)
  elif y[i] == 'hping3':
    true.append(1)
  elif y[i] == 'icmp':
    true.append(1)
  elif y[i] == 'udp':
    true.append(1)

print('True:', true)

prediction = []
for i in range(predicted.shape[0]):
  if predicted[i] == 'normal':
    prediction.append(2)
  elif predicted[i] == 'slowloris':
    prediction.append(1)
  elif predicted[i] == 'slow post':
    prediction.append(1)
  elif predicted[i] == 'slow read':
    prediction.append(1)
  elif predicted[i] == 'hping3':
    prediction.append(1)
  elif predicted[i] == 'icmp':
    prediction.append(1)
  elif predicted[i] == 'udp':
    prediction.append(1)

print('Pred:', prediction)

Precision = metrics.precision_score(true, prediction)
Recall = metrics.recall_score(true, prediction)
F1 = metrics.f1_score(true, prediction)

print('accuracy: ', accuracy)
print('Precision:',Precision)
print('Recall:',Recall)
print('F1:',F1)


#存取模型
with open(Savemodel,'wb') as f:
    pickle.dump(rbfModel, f)

#顯示預測錯誤的結果
correct = []
miss = []
miss_list = []
correct_list = []
row = y.shape[0]
print('預測錯誤:')
for i in range(row):
    if y[i] != predicted[i]:
        correct.append(y[i])
        miss.append(predicted[i])
print('錯誤總數',len(miss))
for c in miss:
    if c in miss_list:
        i = 1
    else:
        miss_list.append(c)
for m in miss_list:
    print('錯誤:',m,miss.count(m))#預測錯誤label累計
print('--------------')
for c in correct:
    if c in correct_list:
        i = 1
    else:
        correct_list.append(c)
for m in correct_list:
    print('正確:',m,correct.count(m))#預測錯誤對應正確label累計

h,m,s=sss(t3)
h1,m1,s1=sss(t5)
print('訓練時間',h,'時',m,'分',s,'秒')
print('測試時間',h1,'時',m1,'分',s1,'秒')
print('資料總數',X.shape[0])
print('錯誤總數',len(miss))









