import jieba
import jieba.posseg as pseg
from py2neo import Graph,Node,Relationship
from match import search

#要删掉

#引入自定实体义词典
jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_department.txt")
jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_check.txt")
jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_disease.txt")
jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_drug.txt")
jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_food.txt")
jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_producer.txt")
# jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_symptom.txt")

#引入自定义的属性词典
jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/attribute.txt")
jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/attribute_aux.txt")

entityList= ['dep','che','dis','drug','food','pro','sym']
attriList = ['rea','pre','isw','con','symt','check','the','depart','department','peop']
attri_auxList = ['simiul','disease','time','not','diet','foo','rat','tio','recommend','common','dru','contain']

#创建停用词表
#stopwords = [line.strip() for line in open('d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/cn_stopwords.txt',encoding='UTF-8').readlines()]

#分词
str1 = "单性肺爱酸粒细胞浸润症应该如何治疗？"
words = pseg.cut(str1)

n_entity = 0
n_attri = 0
n_attri_aux = 0
n_entity_word = []
n_entity_flag = []
n_attri_list = []
n_attri_aux_list = []
node=[]
for w in words:
    #寻找实体
    if w.flag in entityList:
            n_entity=n_entity+1
            node.append([w.flag,w.word])
            n_entity_flag.append(w.flag)
            n_entity_word.append(w.word)
    #寻找属性        
    if w.flag in attriList:
            n_attri=n_attri+1
            node.append([w.flag,w.word])  
            n_attri_list.append(w.flag)
    #寻找辅助属性        
    if w.flag in attri_auxList:
            n_attri_aux=n_attri_aux+1
            node.append([w.flag,w.word])  
            n_attri_aux_list.append(w.flag)


#实体矫正
if n_entity == 0:
        result = search(str1)
        print()
        if len(result) == 1:
                n_entity = 1
                node.append(result[0])
                n_entity_flag.append(result[0][0])
                n_entity_word.append(result[0][1])
#输出尝试
# print(n_entity)
# print(n_entity_word,n_attri_aux_list,n_attri_list,n_entity_flag)

#提取关系
entity = ''
relation = 0
if(n_entity==1 and 'dis' in n_entity_flag):  #关于疾病的问题
        if('rea' in n_attri_list):  #1=>病名(dis)+原因(rea)  
                entity = n_entity_word[0]
                relation =1
        elif('pre' in n_attri_list):  #2=>病名(dis)+预防(pre)    
                entity = n_entity_word[0]
                relation =2
        elif('con' in n_attri_list or ('simul' in n_attri_aux_list and 'disease' in n_attri_aux_list )):  #3=>病名(dis)+并发症(con | simul+disease)     
                entity = n_entity_word[0]
                relation =3
        elif('symt' in n_attri_list):  #4=>病名(dis)+症状(symt)   
                entity = n_entity_word[0]
                relation =4
        elif('time' in n_attri_aux_list and ('rat' in n_attri_aux_list or 'the' in n_attri_list)):  #5=>病名(dis)+治疗时间(rat|the+time)   
                entity = n_entity_word[0]
                relation =5
        elif('check' in n_attri_list):  #6=>病名(dis)+检查方法(check)   
                entity = n_entity_word[0]
                relation =6
        elif('the' in n_attri_list):  #7=>病名(dis)+治疗方法(the)   
                entity = n_entity_word[0]
                relation =7
        elif('not' in n_attri_aux_list and ('foo' in n_attri_aux_list or 'diet' in n_attri_aux_list)):  #8=>病名(dis)+忌吃食物(not+foo|diet)   
                entity = n_entity_word[0]
                relation =8
        elif('foo' in n_attri_aux_list):  #9=>病名(dis)+宜吃食物(foo)   
                entity = n_entity_word[0]
                relation =9
        elif('die' in n_attri_list):  #10=>病名(dis)+推荐食谱(diet)   
                entity = n_entity_word[0]
                relation =10
        elif('peop' in n_attri_list):  #11=>病名(dis)+易感人群(peop)   
                entity = n_entity_word[0]
                relation =11
        elif('rat' in n_attri_aux_list and 'tio' in n_attri_aux_list ):  #12=>病名(dis)+治愈概率(rat+tio)   
                entity = n_entity_word[0]
                relation =12
        elif('depart' in n_attri_list or 'department' in n_attri_list ):  #13=>病名(dis)+科室(depart+department)   
                entity = n_entity_word[0]
                relation =13
        elif('isw' in n_attri_list):  #14=>病名(dis)+是什么(isw)   
                entity = n_entity_word[0]
                relation =14
        elif('dru' in n_attri_aux_list and 'recommand' in n_attri_aux_list ):  #15=>病名(dis)+推荐药物(recomand+dru)   
                entity = n_entity_word[0]
                relation =15
        elif('dru' in n_attri_aux_list):  #16=>病名(dis)+常用药物(drug)   
                entity = n_entity_word[0]
                relation =16
if(n_entity==1 and 'dep' in n_entity_flag):  #关于科室的问题
        if('contain' in n_attri_aux_list and 'disease' in n_attri_aux_list):  #17=>科室名(dep)+包含(contain)+病(disease)  
                entity = n_entity_word[0]
                relation =17
        elif('contain' in n_attri_aux_list and 'depart' in n_attri_list):  #18=>科室名(dep)+包含(contain)+科室(depart)     
                entity = n_entity_word[0]
                relation =18
if(n_entity==1 and 'drug' in n_entity_flag):  #关于药物的问题
        if('disease' in n_attri_aux_list):  #19=>药物（drug）+疾病（disease）  
                entity = n_entity_word[0]
                relation =19
if(n_entity==1 and 'check' in n_entity_flag):  #关于检查的问题
        if('disease' in n_attri_aux_list):  #20=>检查（check）+疾病（disease）  
                entity = n_entity_word[0]
                relation =20
# if(n_entity==1 or 'food' in n_entity_flag):  #关于食物的问题(要改)
#         if('contain' in n_attri_aux_list and 'disease' in n_attri_aux_list):  #21=>食物+有益于+疾病  
#                 entity = n_entity_word[0]
#                 relation =21  
#         elif('isw' in n_attri_list):  #22=>病名(dis)+是什么(isw)   
#                 entity = n_entity_word[0]
#                 relation =22                                                

#输出测试
# print(entity,relation)


##连接neo4j数据库，输入地址、用户名、密码
# graph = Graph('http://localhost:7474',username='neo4j',password='522279594zaqwsx')
graph = Graph('http://localhost:7474',auth=('neo4j','522279594zaqwsx'))
sql = ''
gql="MATCH (p1:Disease{ name:'%s'})-[k:belongs_to]->(p2:Department) RETURN p2.name LIMIT 1"%entity
if relation == 1:
        gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.cause LIMIT 1"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(entity+'的病因是：',record)
if relation == 2:  #2=>病名(dis)+预防(pre) 
        gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.prevent LIMIT 1"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(entity+'的预防措施是：',record)
if relation == 3:  #3=>病名(dis)+并发症(con | simul+disease) 
        gql="MATCH (p1:Disease{ name:'%s'})-[k:acompany_with]->(p2:Disease) RETURN p2.name"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        print(entity+"的并发症有：")
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(record)      
if relation == 4:  #4=>病名(dis)+症状(symt)   
        gql="MATCH (p1:Disease{ name:'%s'})-[k:has_symptom]->(p2:Symptom) RETURN p2.name"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        print(entity+"的症状有：")
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(record)
if relation == 5:   #5=>病名(dis)+治疗时间(rat|the+time)  
        gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.cure_lasttime LIMIT 1"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(entity+'的治愈时间是：',record)
if relation == 6:   #6=>病名(dis)+检查方法(check)   
        gql="MATCH (p1:Disease{ name:'%s'})-[k:need_check]->(p2:Check) RETURN p2.name"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        print(entity+"的检查方法有：")
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(record)
if relation == 7:  #7=>病名(dis)+治疗方法(the)  
        gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.cure_way LIMIT 1"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(entity+'的治疗方式有：',record)
if relation == 8:   #8=>病名(dis)+忌吃食物(not+foo|diet)
        gql="MATCH (p1:Disease{ name:'%s'})-[k:no_eat]->(p2:Food) RETURN p2.name"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        print(entity+"忌吃的食物有：")
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(record)
if relation == 9:  #9=>病名(dis)+宜吃食物(foo) 
        gql="MATCH (p1:Disease{ name:'%s'})-[k:do_eat]->(p2:Food) RETURN p2.name"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        print(entity+"推荐食物有：")
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(record)
if relation == 10:  #10=>病名(dis)+推荐食谱(diet)   
        gql="MATCH (p1:Disease{ name:'%s'})-[k:recommand_eat]->(p2:Food) RETURN p2.name"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        print(entity+"推荐食谱有：")
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(record)
if relation == 11:  #11=>病名(dis)+易感人群(peop)   
        gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.easy_get LIMIT 1"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(entity+'的易感人群是：',record)
if relation == 12:  #12=>病名(dis)+治愈概率(rat+tio)  
        gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.cured_prob LIMIT 1"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(entity+'的治愈概率是：',record)
if relation == 13:  #13=>病名(dis)+科室(depart+department)  
        gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.cure_department LIMIT 1"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(entity+'所在科室为：',record)
if relation == 14:  #14=>病名(dis)+是什么(isw)   
        gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.desc LIMIT 1"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(entity+'是：',record)
if relation == 15:  #15=>病名(dis)+推荐药物(recomand+dru) 
        gql="MATCH (p1:Disease{ name:'%s'})-[k:recommand_drug]->(p2:Drug) RETURN p2.name"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        print(entity+"推荐药物有：")
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(record)
if relation == 16:  #16=>病名(dis)+常用药物(drug)  
        gql="MATCH (p1:Disease{ name:'%s'})-[k:common_drug]->(p2:Drug) RETURN p2.name"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        print(entity+"常用药物有：")
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(record)
if relation == 17:  #17=>科室名(dep)+包含(contain)+病(disease)  
        gql="MATCH (p1:Disease)-[k:belongs_to]->(p2:Department{ name:'%s'}) RETURN p1.name"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        print(entity+"治疗的疾病有：")
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(record)
if relation == 18:  #18=>科室名(dep)+包含(contain)+科室(depart) 
        gql="MATCH (p1:Disease)-[k:belongs_to]->(p2:Department{ name:'%s'}) RETURN p1.name"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        print(entity+"包含的科室有：")
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(record)
if relation == 19:  #19=>药物（drug）+疾病（disease）  
        gql="MATCH (p1:Disease)-[k:recommand_drug]->(p2:Drug{ name:'%s'}) RETURN p1.name"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        print(entity+"能治疗的疾病有：")
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(record)
        gql="MATCH (p1:Disease)-[k:common_drug]->(p2:Drug{ name:'%s'}) RETURN p1.name"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(record)
if relation == 20:  #20=>检查（check）+疾病（disease） 
        gql="MATCH (p1:Disease)-[k:need_check]->(p2:Check{ name:'%s'}) RETURN p1.name"%entity
        cursor=graph.run(gql)
        # 循环向前移动游标
        print(entity+"需要的检查有：")
        while cursor.forward():
                # 获取并打印当前的结果集
                record=cursor.current
                print(record)
# if relation == 21:
#         gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.cause LIMIT 1"%entity
#         cursor=graph.run(gql)
#         # 循环向前移动游标
#         while cursor.forward():
#                 # 获取并打印当前的结果集
#                 record=cursor.current
#                 print(entity+'的病因是：',record)  
# if relation == 22:
#         gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.cause LIMIT 1"%entity
#         cursor=graph.run(gql)
#         # 循环向前移动游标
#         while cursor.forward():
#                 # 获取并打印当前的结果集
#                 record=cursor.current
#                 print(entity+'的病因是：',record)
elif relation == 0:
        print("没有识别出语义，请用更加官方的话语提问。")
