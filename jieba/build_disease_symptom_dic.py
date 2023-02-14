from py2neo import Graph,Node,Relationship
import pymysql

#计算新的权重
def calculate_weight(symptoms):
    weight = []
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
            for item in symptoms:   
                #执行SQL语句
                cursor.execute('select symptom_weight from symptom_disease where symptom_name = %s',item)
                result = cursor.fetchall()
                old_weight[item] = (1.0/n_symptoms)/result[0][0]

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
        n = 1.0/all_weight*old_weight[item]
        weight.append(round(n,4))
    return weight

# print(calculate_weight(['气短','胸闷']))

# graph = Graph('http://localhost:7474',username='neo4j',password='522279594zaqwsx')auth=("neo4j","password")
graph = Graph('http://localhost:7474',auth=('neo4j','522279594zaqwsx'))

#得到所有疾病
all_disease = []
gql="MATCH (p1:Disease) RETURN p1.name"
cursor=graph.run(gql)
while cursor.forward():
    # 获取并打印当前的结果集
    record=cursor.current
    all_disease.append([[record[0]]])


#得到每一个疾病的病症
n = 0
for disease in all_disease:
    symptom = []
    gql="MATCH (p1:Disease{name: '%s'})-[k:has_symptom]->(p2:Symptom) RETURN p2.name"%disease[0][0]
    cursor=graph.run(gql)
    # 循环向前移动游标
    while cursor.forward():
        # 获取并打印当前的结果集
        record=cursor.current
        symptom.append(record[0])
    all_disease[n].append(symptom)
    n = n + 1


#存入数据库中
connection = pymysql.connect(host='localhost', port=3306, \
                            user="test", password='522279594', \
                            db='zxj', charset='utf8')    
if connection:                                                        
    print('>> 数据库连接成功.')
    #获取一个游标对象
    cursor = connection.cursor()
    #将所有数据写入数据库
    for disease in all_disease:
        #数据获得
        symptom_num = len(disease[1])
        disease_name = disease[0][0]
        disease_symptom ='#'.join(disease[1])
        disease_symptom_weight = '#'.join(str(i) for i in calculate_weight(disease[1]))
        #执行SQL语句
        cursor.execute("INSERT INTO disease_symptom(disease_name,disease_symptom,symptom_num,disease_symptom_weight) VALUES (%s,%s,%s,%s)",(disease_name,disease_symptom,symptom_num,disease_symptom_weight))

    #提交
    connection.commit()
         
    # 步骤6：关闭数据库连接引用对象
    cursor.close()
    connection.close()
    print('>> 关闭数据库连接.')





