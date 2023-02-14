from py2neo import Graph,Node,Relationship
import pymysql


graph = Graph('http://localhost:7474',username='neo4j',password='522279594zaqwsx')


#得到所有症状
all_symptom = []
gql="MATCH (p1:Symptom) RETURN p1.name"
cursor=graph.run(gql)
while cursor.forward():
    # 获取并打印当前的结果集
    record=cursor.current
    all_symptom.append([[record[0]]])


#得到每一个症状对应的疾病以及总数
n = 0
for symptom in all_symptom:
    disease = []
    gql="MATCH (p1:Disease)-[k:has_symptom]->(p2:Symptom{name: '%s'}) RETURN p1.name"%symptom[0][0]
    cursor=graph.run(gql)
    # 循环向前移动游标
    while cursor.forward():
        # 获取并打印当前的结果集
        record=cursor.current
        disease.append(record[0])
    all_symptom[n].append(disease)
    n = n + 1

# print(all_symptom)

#存入数据库中
connection = pymysql.connect(host='localhost', port=3306, \
                            user="test", password='522279594', \
                            db='zxj', charset='utf8')    
if connection:                                                        
    print('>> 数据库连接成功.')
    #获取一个游标对象
    cursor = connection.cursor()
    #将所有数据写入数据库
    for symptom in all_symptom:
        #数据获得
        symptom_weight = len(symptom[1])
        symptom_name = symptom[0][0]
        #执行SQL语句
        cursor.execute("INSERT INTO symptom_disease(symptom_name,symptom_weight) VALUES (%s,%s)",(symptom_name,symptom_weight))
    
    #提交
    connection.commit()

    # 步骤6：关闭数据库连接引用对象
    cursor.close()
    connection.close()
    print('>> 关闭数据库连接.')








