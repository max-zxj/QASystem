from py2neo import Graph,Node,Relationship
import pymysql

#计算新的权重
def calculate_weight(symptoms):
    weight = {}
    old_weight = {}
    n_symptoms = len(symptoms)
    #提取出每一个症状对应的disease数量
    connection = pymysql.connect(host='localhost', port=3306, \
                user="test", password='522279594', \
                db='zxj', charset='utf8') 
    if connection:                                                        
        print('>> 数据库连接成功.')
        #获取一个游标对象
        cursor = connection.cursor()
        try:
            sql ='select symptom_name,symptom_weight from symptom_disease where symptom_name in ({})'.format(','.join(["'%s'" % item for item in symptoms]))
            #执行SQL语句
            cursor.execute(sql)
            result = cursor.fetchall()

            #记录现有的权重
            for item in result:
                old_weight[item[0]] = (1.0/n_symptoms)/item[1]
        finally:
            # 步骤6：关闭数据库连接引用对象
            cursor.close()
            connection.close()
            print('>> 关闭数据库连接.')

    #计算新的weight
    all_weight = 0
    for item in symptoms:
        all_weight = all_weight + old_weight[item]
    for item in symptoms:
        weight[item] = 1.0/all_weight*old_weight[item]
    return weight

#得到每一个疾病有的症状对应标准的准确度
def get_weigth(weight,symptom):
    accuracy = 0
    for item in symptom:
        accuracy = accuracy + weight[item]

    return accuracy

#匹配疾病
def disease_match(node):   
    #统计其中出现的symptom，并舍弃重复的symptom
    symptom = []
    for item in node:
        if item[0] == 'sym':
            if item[1] in symptom:
                n=1
            else:
                symptom.append(item[1])

    #通过symptom查找疾病并且放入一个dic里面
    disease_dic = {}
    diseases = []
    # graph = Graph('http://localhost:7474',username='neo4j',password='522279594zaqwsx')
    graph = Graph('http://localhost:7474',auth=('neo4j','522279594zaqwsx'))
    for item in symptom:
        gql="MATCH (p1:Disease)-[k:has_symptom]->(p2:Symptom{name: '%s'}) RETURN p1.name"%item
        cursor=graph.run(gql)
        while cursor.forward():
            # 获取并打印当前的结果集
            record=cursor.current
            if record[0] in diseases:
                disease_dic[record[0]].append(item)
            else:
                disease_dic[record[0]] = [item]
                diseases.append(record[0])

    # print(disease_dic,diseases)

    #剔除不达标的疾病
    weight = calculate_weight(symptom)
    # symptom_num = len(symptom)
    new_disease_dic = {}
    new_diseases = []
    for item in disease_dic.items():
        if get_weigth(weight,item[1]) >=0.7:
            new_disease_dic[item[0]] = item[1]
            new_diseases.append(item[0])
    disease_dic = new_disease_dic
    diseases = new_diseases

    # print(disease_dic,diseases)

    #得到每一个疾病的症状以及weight
    weight_dic = {}
    connection = pymysql.connect(host='localhost', port=3306, \
                            user="test", password='522279594', \
                            db='zxj', charset='utf8')    
    if connection:                                                        
        print('>> 数据库连接成功.')
        #获取一个游标对象
        cursor = connection.cursor()
        sql ='select disease_name,disease_symptom,disease_symptom_weight from disease_symptom where disease_name in ({})'.format(','.join(["'%s'" % item for item in diseases]))
        #执行SQL语句
        cursor.execute(sql)
        result = cursor.fetchall()

        for item in result:
            weight_dic[item[0]] = [item[1],item[2]]

        # 步骤6：关闭数据库连接引用对象
        cursor.close()
        connection.close()
        print('>> 关闭数据库连接.')


    #统计每个出现的疾病的症状出现率，返回出现为50%以上的作为结果
    disease_result = []
    mix_rate = 0.5
    for item in diseases:
        key_dic = weight_dic[item][0].split('#')
        word_dic = weight_dic[item][1].split('#')
        word_dic = (float(i) for i in word_dic)
        item_dic = dict(zip(key_dic, word_dic))
        rate = get_weigth(item_dic,disease_dic[item]) 
        if rate == mix_rate:
            disease_result.append([rate,item])
        elif rate > mix_rate:
            disease_result = [[rate,item]]
            mix_rate = rate
       
    
    return disease_result
   

def symptom_result(node,relation):
    result = '根据提供的症状，没有找到相应的疾病'
    hint = ''
    if 19 in relation:
        diseases = disease_match(node)
        if len(diseases) != 0:
            result = '根据提供的症状，可能的疾病有：'
            for disease in diseases:
                result = result + disease[1] + ','
            hint = '因为系统判断准确性不高，建议您通过输入 “%s的症状有哪些?” 来查询症状以便更准确的判断。'%diseases[0][1]
    return result,hint
          


#测试函数可行性
# node = [['drug','将对方班级的'],['sym','气短'],['sym','胸闷憋气'],['sym','胸闷'],['food','shfdf']]
# relation = [1,2,19]
# result = disease_match(node)
# print(result)



