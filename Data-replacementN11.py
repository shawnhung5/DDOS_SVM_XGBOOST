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
    
def flag1(i):
    #print(i,row)
    c = 10#後10個封包
    s = data.iat[i,2]
    d = data.iat[i,3]        
    if '[SYN]' in data.iat[i,6]:
        x1 = 1
        for a in range(c):
            b = i+a+1
            if b < row:
                d1 = data.iat[b,3]
                if d1 == s:
                    if '[RST]' in data.iat[b,6]:
                        x2 = 1
                        for a1 in range(b-i-1):
                            if '[SYN, ACK]' in data.iat[b - a1,6]:
                                x2 +=1
                        if x2 ==1:
                            return(3)#RSTOS0
                        else:
                            return(1)#REJ
                    elif '[SYN, ACK]' in data.iat[b,6]:
                        x1 +=1
                        for a2 in range(c):
                            b1 = b+a2+1
                            if b1 < row:
                                d2 = data.iat[b1,3]
                                if d2 == d:
                                    if '[ACK]' in data.iat[b1,6]:
                                        for a3 in range(c):
                                            b2 = b1+a3+1
                                            if b2 < row:
                                                d3 = data.iat[b2,3]
                                                if '[RST]' in data.iat[b2,6]:
                                                    if d3 == d:
                                                        return(2)#RSTO
                                                    elif d3 == s:
                                                        return(4)#RSTR
                                            else:
                                                break
                                        return(6)#S1
                            else:
                                break
                        return(9)#SF
                elif d1 == d:
                    if '[ACK]' in data.iat[b,6]:
                        if x1 == 1:
                            return(7)#S2
                elif 'FIN' in data.iat[b,6]:
                    x3 = 1
                    for a4 in range(b-i-1):
                        d4 = data.iat[b-a4,3]
                        if d4 == s:    
                            if '[SYN, ACK]' in data.iat[b - a4,6]:
                                x3 +=1
                    if x3 ==1:
                        return(10)#SH
            else:
                break
        return(5)#S0
    elif '[FIN, ACK]' in data.iat[i,6]:
        x4 = 1
        for a5 in range(c):
            b3 = i+a5+1
            if b3 < row:
                d5 = data.iat[b3,3]
                if d5 == s:
                    if '[ACK]' in data.iat[b3,6]:
                        x4 +=1
            else:
                break
        if x4 == 1 :
            return(7)#S2
        return(9)#SF
    elif '[PSH, ACK]' in data.iat[i,6]:
        return(9)#SF
    elif '[SYN, ACK]' in data.iat[i,6]:
        for a6 in range(c):
            b4 = i+a6+1
            if b4 < row:
                d6 = data.iat[b4,3]
                if d6 == s:
                    if '[ACK]' in data.iat[b4,6]:
                        for a7 in range(c):
                            b5 = b4+a7+1
                            if b5 < row:
                                d7 = data.iat[b5,3]
                                if '[RST]' in data.iat[b5,6]:
                                    if d7 == s:
                                        return(2)#RSTO
                                    elif d7 == d:
                                        return(4)#RSTR
                            else:
                                break
                        return(6)#S1
            else:
                break
        return(9)#SF
    elif '[ACK]' in data.iat[i,6]:
        for a10 in range(c):
            b8 = i+a10+1
            if b8 < row:
                d10 = data.iat[b8,6]
                if '[RST]' in data.iat[b8,6]:
                    if d10 == d:
                        return(2)#RSTO
                    elif d10 == s:
                        return(4)#RSTR
            else:
                break
        q = 1
        q1 = 1
        q2 = 1
        for a8 in range(c+1):
            b6 = i-a8
            if b6 >= 0:
                d8 = data.iat[b6,3]
                if '[SYN]' in data.iat[b6,6]:
                    q+=1
                elif '[SYN, ACK]' in data.iat[b6,6]:
                    q1+=1
                    if d8 == s:
                        q2 +=1
        if q > 1:
            if q1 > 1 :
                if q2 == 1:
                    return(7)#S2
                return(9)#SF
        return(9)#SF
                    
    elif '[RST]' in data.iat[i,6]:
        p = 1
        p1 = 1
        for a9 in range(c+1):
            b7 = i-a9
            if b7 >= 0:
                d9 = data.iat[b7,3]
                if '[SYN]' in data.iat[b7,6]:
                    p+=1
                elif '[SYN, ACK]' in data.iat[b7,6]:
                    p1+=1
                elif '[ACK]' in data.iat[b7,6]:
                    if d9 == d:
                         return(2)#RSTO
                    elif d9 == s:
                         return(4)#RSTR
            else:
                break
        if p > 1:
            if p1 > 1 :
                return(1)#REJ
            else:
                return(3)#RSTOS0
        return(1)#REJ
    else:
        return(0)

def twos(i):#過去兩秒內
    serror_rate_c = 0#過去兩秒內，與當前連接具有相同目標主機，出現SYN錯誤的連接的百分比
    rerror_rate_c = 0#過去兩秒內，與當前連接具有相同目標主機，出現REJ錯誤的連接的百分比
    srv_serror_rate_c = 0#過去兩秒內，與當前連接具有相同服務，出現SYN錯誤的連接的百分比
    srv_rerror_rate_c = 0#過去兩秒內，與當前連接具有相同服務，出現REJ錯誤的連接的百分比
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
            f = flag_list[i-a]
            if d == d1:
                if f == 5:
                    serror_rate_c +=1
                    if p == p1:
                        srv_serror_rate_c +=1
                elif f == 6:
                    serror_rate_c +=1
                    if p == p1:
                        srv_serror_rate_c +=1
                elif f == 9:
                    serror_rate_c +=1
                    if p == p1:
                        srv_serror_rate_c +=1
                elif f == 2:
                    serror_rate_c +=1
                    if p == p1:
                        srv_serror_rate_c +=1
                elif f == 4:
                    serror_rate_c +=1
                    if p == p1:
                        srv_serror_rate_c +=1
                elif f == 1:
                    rerror_rate_c +=1
                    if p == p1:
                        srv_rerror_rate_c +=1
            elif p == p1:
                f = flag_list[i-a]
                if f == 5:
                    srv_serror_rate_c +=1
                elif f == 6:
                    srv_serror_rate_c +=1
                elif f == 9:
                    srv_serror_rate_c +=1
                elif f == 2:
                    srv_serror_rate_c +=1
                elif f == 4:
                    srv_serror_rate_c +=1
                elif f == 1:
                    srv_rerror_rate_c +=1
        a+=1
    a -=1
    if a == 0:
        return(0.0,0.0,0.0,0.0)
    else:
        return(round_v2(serror_rate_c/a,2),round_v2(rerror_rate_c/a,2),round_v2(srv_serror_rate_c/a,2),
               round_v2(srv_rerror_rate_c/a,2))

def b100(i):#前100連接
    dst_host_serror_rate_c = 0#前100連接，與當前連線有相同目標主機的連接中，出現SYN錯誤
    dst_host_rerror_rate_c = 0#前100連接，與當前連線有相同目標主機的連接中，出現SYN錯誤
    dst_host_srv_serror_rate_c = 0#前100連接，與當前連線有相同目標主機相同服務的連接中，出現SYN錯誤
    dst_host_srv_rerror_rate_c = 0#前100連接，與當前連線有相同目標主機相同服務的連接中，出現REJ錯誤
    a = 1
    d = data.iat[i,3]
    p = data.iat[i,4]
    while a < 101:
        if i-a < 0:
            break
        else:
            p1 = data.iat[i-a,4]
            d1 = data.iat[i-a,3]
            f = flag_list[i-a]
            if d == d1:
                if f == 5:
                    dst_host_serror_rate_c +=1
                    if p == p1:
                        dst_host_srv_serror_rate_c +=1
                elif f == 6:
                    dst_host_serror_rate_c +=1
                    if p == p1:
                        dst_host_srv_serror_rate_c +=1
                elif f == 9:
                    dst_host_serror_rate_c +=1
                    if p == p1:
                        dst_host_srv_serror_rate_c +=1
                elif f == 2:
                    dst_host_serror_rate_c +=1
                    if p == p1:
                        dst_host_srv_serror_rate_c +=1
                elif f == 4:
                    dst_host_serror_rate_c +=1
                    if p == p1:
                        dst_host_srv_serror_rate_c +=1
                elif f == 1:
                    dst_host_rerror_rate_c +=1
                    if p == p1:
                        dst_host_srv_rerror_rate_c +=1
        a+=1
    a -=1
    if a == 0:
        return(0.0,0.0,0.0,0.0)
    else:
        return(round_v2(dst_host_serror_rate_c/a,2),round_v2(dst_host_rerror_rate_c/a,2),
               round_v2(dst_host_srv_serror_rate_c/a,2),round_v2(dst_host_srv_rerror_rate_c/a,2))

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
flag_list = []
serror_rate_list = []
rerror_rate_list = []
srv_serror_rate_list = []
srv_rerror_rate_list = []
dst_host_serror_rate_list = []
dst_host_rerror_rate_list = []
dst_host_srv_serror_rate_list = []
dst_host_srv_rerror_rate_list = []
label_list = []


file_name = 'a-hping-30000-155-FO'
local_name = 'FO'
label_name = 'hping3'
#normal、hping3、slowloris-H、slow post-B、slow read-X

SaveFile_Name = file_name + 'N11.csv' 

data = pd.read_csv(local_name+"\\"+file_name + '.csv')
data = data.dropna()#移除缺失值
row = data.shape[0]
row = 500

print(data)

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
    
    flag_list.append(flag1(i))
    
    label_list.append(label_name)

for i in range(row):
    s1,r1,s2,r2=twos(i)
    serror_rate_list.append(s1)
    rerror_rate_list.append(r1)
    srv_serror_rate_list.append(s2)
    srv_rerror_rate_list.append(r2)

    print(i,b100(i))
    ds1,dr1,ds2,dr2=b100(i)
    dst_host_serror_rate_list.append(ds1)
    dst_host_rerror_rate_list.append(dr1)
    dst_host_srv_serror_rate_list.append(ds2)
    dst_host_srv_rerror_rate_list.append(dr2)

print(row)

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
flag = flag_list
serror_rate = serror_rate_list
rerror_rate = rerror_rate_list
srv_serror_rate = srv_serror_rate_list
srv_rerror_rate = srv_rerror_rate_list
dst_host_serror_rate = dst_host_serror_rate_list
dst_host_rerror_rate = dst_host_rerror_rate_list
dst_host_srv_serror_rate = dst_host_srv_serror_rate_list
dst_host_srv_rerror_rate = dst_host_srv_rerror_rate_list
label = label_list

DataSet = list(zip(protocol_type,count,srv_count,same_srv_rate,diff_srv_rate,srv_diff_host_rate,
                   dst_host_count,dst_host_srv_count,dst_host_same_srv_rate,dst_host_diff_srv_rate,
                   dst_host_same_src_port_rate,dst_host_srv_diff_host_rate,flag,serror_rate,rerror_rate,
                   srv_serror_rate,srv_rerror_rate,dst_host_serror_rate,dst_host_rerror_rate,
                   dst_host_srv_serror_rate,dst_host_srv_rerror_rate,label))

df = pd.DataFrame(data = DataSet ,columns=["protocol_type","count","srv_count","same_srv_rate","diff_srv_rate",
                                           "srv_diff_host_rate","dst_host_count","dst_host_srv_count",
                                           "dst_host_same_srv_rate","dst_host_diff_srv_rate",
                                           "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate",
                                           "flag","serror_rate","rerror_rate",
                                           "srv_serror_rate","srv_rerror_rate","dst_host_serror_rate",
                                           "dst_host_rerror_rate","dst_host_srv_serror_rate",
                                           "dst_host_srv_rerror_rate","label"])

print(df)

df.to_csv( "C:/Users/user/OneDrive/碩論/python-kdd99/ready\\"+SaveFile_Name, index=False)


    