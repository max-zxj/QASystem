#进行实体匹配，只匹配drug，disease和check
import re 
import heapq

#提取公共子串
def str_int(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
        #print(s1,s2)
    length = len(s1)
    result = []
    for step in range(length,0 ,-1):
        for start in range(0,length-step+1):
            flag = True
            tmp = s1[start:start+step]
            if s2.find(tmp)>-1 :# 第一次找到,后面要接着找 
                result.append(tmp)
                flag = True
                newstart = start+1
                newstep = step
                while flag:   # 已经找到最长子串,接下来就是判断后面是否还有相同长度的字符串 
                    if newstart+ step >length:  # 大于字符串总长了,退出循环
                        break
                    newtmp = s1[newstart:newstart+newstep] 
                    if s2.find(newtmp)>-1:
                        result.append(newtmp)
                        newstart+=1
                        flag = True
                    else:
                        newstart +=1
                        flag = True    
                return result
            else:
                continue


#计算相似度
def match(str1,str2):
    answear = str_int(str1,str2)
    common_str = ''
    result = [0,'',0]
    if answear == None:
        return result
    else:
        common_str = answear[0]

    if 0.5*len(str2)<=len(common_str):
        #找到话语中公共字符串的位置
        starts = [each.start() for each in re.finditer(common_str, str1)] 
        ends = [start + len(common_str) - 1 for start in starts]
        span = [(start, end) for start, end in zip(starts, ends)]

        #找到实体中公共字符换的位置
        start_2 = [each.start() for each in re.finditer(common_str, str2)]  
        end_2 = [start + len(common_str) - 1 for start in start_2]

        #输出测试
        # print(start_2,end_2)
        # print(starts,'ppp',ends,'ppp',len(span))

        #开始匹配
        now= 0  #当前匹配的位置
        start2 = start_2[0]  #实体的开始
        end2 = end_2[0]  #实体的结束
        alleviation = 1  #偏离差
        match = 0 #当前匹配到的实体位置
        ratio = 1/len(str2)  #每匹配一个高处的概率
        rate = ratio * len(common_str)
        rates = []
        for (start1,end1) in span:
            #设置参数值
            start2 = start_2[0]  #实体的开始
            end2 = end_2[0]  #实体的结束
            alleviation = 1  #偏离差
            ratio = 1/len(str2)  #每匹配一个高处的概率
            rate = ratio * len(common_str)
            #先遍历前面的
            now = start1 - 1
            match = start2 - 1
            while(now >= 0 and match >= 0):
                if(str1[now] == str2[match]):
                    rate = rate + ratio 
                    match = match -1
                    now = now - 1
                elif(now - 1 >= 0 and str1[now-1] == str2[match]):
                    now = now - 2
                    alleviation = alleviation + 1
                    match = match -1
                    rate = rate + ratio / alleviation
                elif(match - 1 >= 0 and str1[now] == str2[match - 1]):
                    now = now - 1
                    alleviation = alleviation * 2
                    match = match - 2
                    rate = rate + ratio 
                else:
                    now = now - 1
                    alleviation = alleviation * 2
                    match = match -1
            #再遍历后面
            now = end1 + 1
            match = end2 + 1
            while(now <= len(str1)-1 and match <= len(str2) - 1):
                if(str1[now] == str2[match]):
                    rate = rate + ratio 
                    now = now + 1
                    match = match + 1
                elif(now + 1 <= len(str1) - 1 and str1[now + 1] == str2[match]):
                    now = now + 2
                    alleviation = alleviation + 1
                    match = match + 1
                    rate = rate + ratio / alleviation
                else:
                    now = now + 1
                    alleviation = alleviation * 2
                    match = match + 1
            rates.append(rate)

        #找到最大的相似度
        t = heapq.nlargest(1, rates)[0]  
        if t >= 0.75 :
            result = [1,str2,t]    
        else:
            result = [0,str2,t]  

    #输出测试
    # print(rates)
    # print([str2,t])

    return result


def search_txt(txt_path,str1):
    rates_entity = []   #存放匹配成功的实体以及它的相似度
    result = []
    try:
        f = open(txt_path, "r",encoding='utf-8')
        entities = f.read().splitlines()
        for entity in entities:
            t = match(str1,entity)
            if t[0] == 1:
                rates_entity.append([t[1],t[2]])
        
        #找到最大相似度的所有实体
        if rates_entity != None:
            r = 0
            for [entity,rate] in rates_entity:
                if r < rate:
                    r = rate
            for [entity,rate] in rates_entity:
                if r == rate:
                    result.append([entity,rate])
    except IOError:
        print('警告：文件读取失败')
    finally:
        f.close()
    return result



#全局匹配
def search_entity(str1):
    rate = 0
    result = []
    disease_entity = search_txt("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_disease1.txt",str1)
    drug_entity = search_txt("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_drug1.txt",str1)
    check_entity = search_txt("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_check1.txt",str1)
    if len(disease_entity) != 0:
        rate = disease_entity[0][1]
        for item in disease_entity:
            result.append(['dis',item[0]])
    if len(drug_entity) and drug_entity[0][1] > rate:
        rate = drug_entity[0][1]
        result = []
        for item in disease_entity:
            result.append('drug',[item[0]])
    if len(drug_entity) and drug_entity[0][1] == rate:
        for item in drug_entity:
            result.append('drug',[item[0]])
    if len(check_entity) and check_entity[0][1]>rate:
        rate = check_entity[0][1]
        result = []
        for item in disease_entity:
            result.append(['che',item[0]])
    if len(check_entity) and check_entity[0][1] == rate:
        for item in check_entity:
            result.append(['che',item[0]])

    return result


