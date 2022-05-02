import pandas as pd

'''
#合併資料夾中的CSV檔
import os
Folder_Path = 'C:/Users/user/OneDrive/碩論/python-kdd99/merge'      #要拼接的資料夾及其完整路徑，注意不要包含中文
SaveFile_Path =  'C:/Users/user/OneDrive/碩論/python-kdd99'      #拼接後要儲存的檔案路徑
SaveFile_Name = 't50515253545562-FON-N12.csv'              #合併後要儲存的檔名

#修改當前工作目錄
os.chdir(Folder_Path)
#將該資料夾下的所有檔名存入一個列表
file_list = os.listdir()

#讀取第一個CSV檔案幷包含表頭
df = pd.read_csv(Folder_Path +'\\'+ file_list[0])   #編碼預設UTF-8，若亂碼自行更改

#將讀取的第一個CSV檔案寫入合併後的檔案儲存
df.to_csv(SaveFile_Path+'\\'+ SaveFile_Name,encoding='utf_8_sig',index=False)

#迴圈遍歷列表中各個CSV檔名，並追加到合併後的檔案
for i in range(1,len(file_list)):
    df = pd.read_csv(Folder_Path + '\\'+ file_list[i])
    df.to_csv(SaveFile_Path+'\\'+ SaveFile_Name,encoding="utf_8_sig",index=False, header=False, mode='a+')
'''
#亂數抽取資料集另存檔案
data = pd.read_csv('test-data/N12-24/t50515253545562-FON-N10.csv')

#df.sample(n=None, frac=None, replace=False, weights=None, random_state=None, axis=None)
#n = number of rows(optional, cannot be used with frac) 抽取的行数；
#frac = fraction/proportion(optional, cannot be used with n) 抽取的比例；
#replace = Allow or disallow sampling of the same row more than once (boolean, default False) 是否为有放回抽样；
#weights (str or ndarray-like, optional) 权重
#random_state (int to use as interval, or call np.random.get_state(), optional) 整数作为间隔，或者调用np.random.get_state()
#axis = extract row or column (0->row, 1->column) 抽取行还是列（0是行，1是列）
 
# random select 10% from dataset
sample = data.sample(n = 50000, random_state=75,replace=False, axis=0)
# export to csv file
sample.to_csv('r50515253545562-50000FON-N10.csv',encoding='utf_8_sig',index=False)



