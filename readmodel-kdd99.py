import pandas as pd
import pickle
import time
from sklearn import metrics

def sss(i):
    h = int(i/3600)
    i = int(i%3600)
    m = int(i/60)
    s = int(i%60)
    return(h,m,s)


data1 = 'test-data/r/N10~22/r50515253545562-50000FO-N10.csv'
model1 = 'model/N10~24/rbfModel-0-6-FO-280000N10-100.pickle'

df_data=pd.read_csv(data1)

test_data = df_data.drop(labels=['label'],axis=1).values # 移除Species (因為字母不參與訓練)
y=df_data['label'].values
print(y)

t1 = time.time()#開始時間

with open(model1,'rb') as f:
    Model = pickle.load(f)
    pred = Model.predict(test_data)
    score1 = Model.score(test_data,y)
print('predict:',pred)
print('score:',score1)

print("===========")
row = df_data.shape[0]
print('資料總數',row)

print('model',model1)
print('data1',data1)

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

#print('True:', true)

prediction = []
for i in range(pred.shape[0]):
  if pred[i] == 'normal':
    prediction.append(2)
  elif pred[i] == 'slowloris':
    prediction.append(1)
  elif pred[i] == 'slow post':
    prediction.append(1)
  elif pred[i] == 'slow read':
    prediction.append(1)
  elif pred[i] == 'hping3':
    prediction.append(1)
  elif pred[i] == 'icmp':
    prediction.append(1)
  elif pred[i] == 'udp':
    prediction.append(1)

#print('Pred:', prediction)

Precision = metrics.precision_score(true, prediction)
Recall = metrics.recall_score(true, prediction)
F1 = metrics.f1_score(true, prediction)

print('accuracy: ', score1)
print('Precision:',Precision)
print('Recall:',Recall)
print('F1:',F1)


#顯示預測錯誤的結果
correct = []
miss = []
miss_list = []
correct_list = []
row = y.shape[0]
print('預測錯誤:')
for i in range(row):
    if y[i] != pred[i]:
        correct.append(y[i])
        miss.append(pred[i])
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
    
t2 = time.time()#完成時間
t3 = t2-t1
h,m,s=sss(t3)
print(h,'時',m,'分',s,'秒')

