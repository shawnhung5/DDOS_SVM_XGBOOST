import pandas as pd
import numpy as np

def round_v2(num, decimal):
    num = np.round(num, decimal)
    num = float(num)
    return num

def protocol_type1(a):
    if a == 'TCP':
        return(0)
    elif 'TLSv' in str(a):
        return(0)
    elif a == 'Modbus/TCP':
        return(0)
    elif 'HTTP' in str(a):
        return(0)
    elif a == 'UDP':
        return(1)
    elif a == 'NBNS':
        return(1)
    elif a == 'MDNS':
        return(1)
    elif a == 'NTP':
        return(1)
    elif a == 'DHCP':
        return(1)
    elif a == 'DNS':
        return(1)
    elif 'ICMP' in str(a):
        return(2)
    else:
        return(3)

def SPort_1(i):
    if data.iat[i,4] == "TCP":
        p = data.iat[i,6]
        c = p.find('>')
        t = p[c-3]
        port = []
        while t.isdigit():
            c = c - 1
            if c == 1:
                break
            else:    
                port.append(t)
                t = p[c-3]
        port.reverse()
        return("".join(port))
    else:
        return(0)
    
def twos_host(i):
    count_c = 0#過去兩秒內，與當前連線有相同目標主機的連線數
    same_srv_rate_c = 0#過去兩秒內，與當前連接具有相同目標主機和相同服務的連接的百分比
    diff_srv_rate_c = 0#過去兩秒內，與當前連接具有相同目標主機和不同服務的連接的百分比
    a = 1
    ta = 0
    d = data.iat[i,3]
    p = data.iat[i,4]
    t = data.iat[i,1]
    while ta < 2:
        if i-a < 0:
            break
        else:    
            t1 = data.iat[i-a,1]
            ta = abs(t - t1)
            d1 = data.iat[i-a,3]
            p1 = data.iat[i-a,4]
            if d == d1:
                count_c +=1
                if p == p1:
                    same_srv_rate_c +=1
                elif p != p1:
                    diff_srv_rate_c +=1
        a+=1
    a -=1
    if count_c >= 511:
      count_c = 511
    if a == 0:
        return(0,0.0,0.0)
    else:
        return(count_c,round_v2(same_srv_rate_c/a,2),round_v2(diff_srv_rate_c/a,2))
    
def twos_srv(i):
    srv_count_c = 0#過去兩秒內，與當前連接具有相同服務的連接數
    srv_diff_host_rate_c = 0#過去兩秒內，與當前連接具有相同服務和不同目標主機的連接的百分比
    a = 1
    ta = 0
    d = data.iat[i,3]
    p = data.iat[i,4]
    t = data.iat[i,1]
    while ta < 2:
        if i-a < 0:
            break
        else:    
            t1 = data.iat[i-a,1]
            ta = abs(t - t1)
            d1 = data.iat[i-a,3]
            p1 = data.iat[i-a,4]
            if p == p1:
                srv_count_c +=1
                if d != d1:
                    srv_diff_host_rate_c +=1
        a+=1
    a -=1
    if srv_count_c >= 511:
      srv_count_c = 511
    if a == 0:
        return(0,0.0)
    else:
        return(srv_count_c,round_v2(srv_diff_host_rate_c/a,2))

def dst_host_count1(i):#前100連接，與當前連線有相同目標主機的連線數
    c = 0
    a = 1
    d = data.iat[i,3]
    while a < 101:
        if i-a < 0:
            break
        else:
            d1 = data.iat[i-a,3]
            if d == d1:
                c += 1
        a+=1
    return(c)

def dst_host_srv_count1(i):#前100連接，與當前連線有相同目標主機與相同服務的連線數
    c = 0
    a = 1
    d = data.iat[i,3]
    p = data.iat[i,4]
    while a < 101:
        if i-a < 0:
            break
        else:
            p1 = data.iat[i-a,4]
            d1 = data.iat[i-a,3]
            if d == d1:
              if p == p1:
                c += 1
        a+=1
    return(c)

def dst_host_same_srv_rate1(i):#前100連接，與當前連線，具有相同目標主機相同服務的連線所佔的百分比
    c = 0
    a = 1
    d = data.iat[i,3]
    p = data.iat[i,4]
    while a < 101:
        if i-a < 0:
            break
        else:
            d1 = data.iat[i-a,3]
            p1 = data.iat[i-a,4]
            if d == d1:
                if p == p1:
                    c += 1
        a+=1
    a -=1
    if a == 0:
        return(0)
    else:
        return(round_v2(c/a,2))

def dst_host_diff_srv_rate1(i):#前100連接，與當前連線，具有相同目標主機不同服務的連線所佔的百分比
    c = 0
    a = 1
    d = data.iat[i,3]
    p = data.iat[i,4]
    while a < 101:
        if i-a < 0:
            break
        else:
            d1 = data.iat[i-a,3]
            p1 = data.iat[i-a,4]
            if d == d1:
                if p != p1:
                    c += 1
        a+=1
    a -=1
    if a == 0:
        return(0)
    else:
        return(round_v2(c/a,2))
    
def dst_host_same_src_port_rate1(i):#前100連接，與當前連線，具有相同目標主機相同源端口的連線所佔的百分比
    c = 0
    a = 1
    d = data.iat[i,3]
    sp = SPort_1(i)
    while a < 101:
        if i-a < 0:
            break
        else:
            d1 = data.iat[i-a,3]
            sp1 = SPort_1(i-a)
            if d == d1:
                if sp == sp1:
                    c += 1
        a+=1
    a -=1
    if a == 0:
        return(0)
    else:
        return(round_v2(c/a,2))
    
def dst_host_srv_diff_host_rate1(i):#前100連接，與當前連線，具有相同目標主機相同服務不同源主機的連線所佔的百分比
    c = 0
    a = 1
    d = data.iat[i,3]
    s = data.iat[i,2]
    p = data.iat[i,4]
    while a < 101:
        if i-a < 0:
            break
        else:
            d1 = data.iat[i-a,3]
            s1 = data.iat[i-a,2]
            p1 = data.iat[i-a,4]
            if d == d1:
                if p == p1:
                    if s != s1:
                        c += 1
        a+=1
    a -=1
    if a == 0:
        return(0)
    else:
        return(round_v2(c/a,2))

def NT_1(i):
    now = data.iat[i,2]
    if i == row-1:
        return(0)
    else:
        next1 = data.iat[i+1,2]
        c1 = i+1
        while now != next1:
            c1 = c1+1
            if c1 == row:
                return(0)
                break
            else:
                next1 = data.iat[c1,2]
        if c1 != row:
            return(round_v2(data.iat[c1,1]-data.iat[i,1],7))
        
def PT_1(i):
    now = data.iat[i,2]
    if i == 0:
        return(0)
    else:
        previous = data.iat[i-1,2]
        c2 = i-1
        while now != previous:
            c2 =c2 -1
            if c2 < 0:
                return(0)
                break
            else:
                previous = data.iat[c2,2]
        if c2 >= 0:
            return(round_v2(data.iat[i,1]-data.iat[c2,1],7))

def DPort_1(i):
    if data.iat[i,4] == "TCP":
        p = data.iat[i,6]
        c = p.find('>')
        t = p[c+3]
        port = []
        while t.isdigit():
            c = c + 1
            port.append(t)
            t = p[c+3]
        return("".join(port))
    elif data.iat[i,4] == "Modbus/TCP":
        return(502)
    else:
        return(0)

def Win_1(i):
    if "Win=" in data.iat[i,6]:
        p = data.iat[i,6]
        c = p.find('Win=')
        t = p[c+4]
        Win = []
        while t.isdigit():
            c = c + 1
            Win.append(t)
            t = p[c+4]
        return("".join(Win))
    else:
        return(0)
    
def len_1(i):
    if "Len=" in data.iat[i,6]:
        p = data.iat[i,6]
        c = p.find('Len=')
        t = p[c+4]
        L = []
        l = len(p)
        while c+3 < l-1:
            t = p[c+4]
            c = c + 1
            if t.isdigit():     
                L.append(t)
            else:
                break
        return("".join(L))
    else:
        return(0)
 
def TSC_1(i):
    if data.iat[i,4] == 'TCP':    
        if "TSval=" in data.iat[i,6]:
            p = data.iat[i,6]
            c = p.find('TSval=')
            t = p[c+6]
            Tsval = []
            while t.isdigit():
                c = c + 1
                Tsval.append(t)
                t = p[c+6]
            Ts = int("".join(Tsval))
            now = data.iat[i,2]
            if i == row-1:
                return(0)
            else:
                next1 = 0
                c1 = i
                while now != next1:
                    c1 = c1+1
                    if c1 == row:
                        return(0)
                        break
                    else:
                        if "TSval=" in data.iat[c1,6]:
                            next1 = data.iat[c1,2]
                p = data.iat[c1,6]
                c = p.find('TSval=')
                t = p[c+6]
                Tsval = []
                while t.isdigit():
                    c = c + 1
                    Tsval.append(t)
                    t = p[c+6]
                TsN = int("".join(Tsval))
                if c1 != row:
                    return(round_v2(TsN-Ts,7))
        else:
            return(0)
    else:
        return(0)

protocol_type_list = []
count_list = []
srv_count_list = []
same_srv_rate_list = []
diff_srv_rate_list = []
srv_diff_host_rate_list = []
dst_host_count_list = []
dst_host_srv_count_list = []
dst_host_same_srv_rate_list = []
dst_host_diff_srv_rate_list = []
dst_host_same_src_port_rate_list = []
dst_host_srv_diff_host_rate_list = []
PT_list = []
NT_list = []
DPort_list = []
Win_list = []
Len_list = []
TSC_list = []
label_list = []


file_name = 'a-icmprq-30000-155-FO1'
local_name = 'FO'
label_name = 'icmp'
#normal、hping3、slowloris-H、slow post-B、slow read-X

SaveFile_Name = file_name + 'N12.csv' 

data = pd.read_csv(local_name+"\\"+file_name + '.csv')
data = data.dropna()#移除缺失值
row = data.shape[0]
#row = 500

print(data)
print(row)

for i in range(row):
    protocol_type_list.append(protocol_type1(data.iat[i,4]))
    
    print(i,twos_host(i))
    c1,ss,ds=twos_host(i)
    sc,sd=twos_srv(i)
    
    count_list.append(c1)

    srv_count_list.append(sc)
    
    same_srv_rate_list.append(ss)
    
    diff_srv_rate_list.append(ds)
    
    srv_diff_host_rate_list.append(sd)

    dst_host_count_list.append(dst_host_count1(i))

    dst_host_srv_count_list.append(dst_host_srv_count1(i))
    
    dst_host_same_srv_rate_list.append(dst_host_same_srv_rate1(i))

    dst_host_diff_srv_rate_list.append(dst_host_diff_srv_rate1(i))

    dst_host_same_src_port_rate_list.append(dst_host_same_src_port_rate1(i))
    
    dst_host_srv_diff_host_rate_list.append(dst_host_srv_diff_host_rate1(i))
    
    PT_list.append(PT_1(i))
    NT_list.append(NT_1(i))

    DPort_list.append(DPort_1(i))
    
    Win_list.append(Win_1(i))
    
    Len_list.append(len_1(i))
    
    TSC_list.append(TSC_1(i))
    
    label_list.append(label_name)


protocol_type = protocol_type_list
count = count_list
srv_count = srv_count_list
same_srv_rate = same_srv_rate_list
diff_srv_rate = diff_srv_rate_list
srv_diff_host_rate = srv_diff_host_rate_list
dst_host_count = dst_host_count_list
dst_host_srv_count = dst_host_srv_count_list
dst_host_same_srv_rate = dst_host_same_srv_rate_list
dst_host_diff_srv_rate = dst_host_diff_srv_rate_list
dst_host_same_src_port_rate = dst_host_same_src_port_rate_list
dst_host_srv_diff_host_rate = dst_host_srv_diff_host_rate_list
PT = PT_list
NT = NT_list
DPort = DPort_list
Win = Win_list
Len = Len_list
TSC = TSC_list
label = label_list

DataSet = list(zip(protocol_type,count,srv_count,same_srv_rate,diff_srv_rate,srv_diff_host_rate,
                   dst_host_count,dst_host_srv_count,dst_host_same_srv_rate,dst_host_diff_srv_rate,
                   dst_host_same_src_port_rate,dst_host_srv_diff_host_rate,PT,NT,DPort,
                   Win,Len,TSC,label))

df = pd.DataFrame(data = DataSet ,columns=["protocol_type","count","srv_count","same_srv_rate","diff_srv_rate",
                                           "srv_diff_host_rate","dst_host_count","dst_host_srv_count",
                                           "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
                                           "dst_host_srv_diff_host_rate","PT","NT","DPort",
                                           "Win","Len","TSC","label"])

print(df)

df.to_csv( "C:/Users/user/OneDrive/碩論/python-kdd99/ready\\"+SaveFile_Name, index=False)


    








