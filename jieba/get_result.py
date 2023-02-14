from py2neo import Graph,Node,Relationship


def get_result(entity,relation):
    return_answear = ''
    #连接neo4j数据库，输入地址、用户名、密码
#     graph = Graph('http://localhost:7474',username='neo4j',password='522279594zaqwsx')
    graph = Graph('http://localhost:7474',auth=('neo4j','522279594zaqwsx'))
    if relation == 1:
            gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.cause LIMIT 1"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+'的病因为：'
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 2:  #2=>病名(dis)+预防(pre) 
            gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.prevent LIMIT 1"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+'的预防措施有：'
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 3:  #3=>病名(dis)+并发症(con | simul+disease) 
            gql="MATCH (p1:Disease{ name:'%s'})-[k:acompany_with]->(p2:Disease) RETURN p2.name"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+'的并发症有：'
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]     
    if relation == 4:  #4=>病名(dis)+症状(symt)   
            gql="MATCH (p1:Disease{ name:'%s'})-[k:has_symptom]->(p2:Symptom) RETURN p2.name"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+"的症状有："
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 5:   #5=>病名(dis)+治疗时间(rat|the+time)  
            gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.cure_lasttime LIMIT 1"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+'的治疗时间为：'
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 6:   #6=>病名(dis)+检查方法(check)   
            gql="MATCH (p1:Disease{ name:'%s'})-[k:need_check]->(p2:Check) RETURN p2.name"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+"的检查方法有："
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 7:  #7=>病名(dis)+治疗方法(the)  
            gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.cure_way LIMIT 1"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+'的治疗方式为：'
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    for item in record[0]:
                            return_answear = return_answear + '  ' + item
    if relation == 8:   #8=>病名(dis)+忌吃食物(not+foo|diet)
            gql="MATCH (p1:Disease{ name:'%s'})-[k:no_eat]->(p2:Food) RETURN p2.name"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+"忌吃的食物有："
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 9:  #9=>病名(dis)+宜吃食物(foo) 
            gql="MATCH (p1:Disease{ name:'%s'})-[k:do_eat]->(p2:Food) RETURN p2.name"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+"推荐食物有："
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 10:  #10=>病名(dis)+推荐食谱(diet)   
            gql="MATCH (p1:Disease{ name:'%s'})-[k:recommand_eat]->(p2:Food) RETURN p2.name"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+"推荐食谱有："
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 11:  #11=>病名(dis)+易感人群(peop)   
            gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.easy_get LIMIT 1"%entity
            cursor=graph.run(gql)
            return_answear = entity+'的易感人群为：'
            # 循环向前移动游标
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 12:  #12=>病名(dis)+治愈概率(rat+tio)  
            gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.cured_prob LIMIT 1"%entity
            cursor=graph.run(gql)
            return_answear = entity+'的治愈概率为：'
            # 循环向前移动游标
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 13:  #13=>病名(dis)+科室(depart+department)  
            gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.cure_department LIMIT 1"%entity
            cursor=graph.run(gql)
            return_answear = entity+'所属科室为：'
            # 循环向前移动游标
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    for item in record[0]:
                            return_answear = return_answear + '  ' + item
    if relation == 14:  #14=>病名(dis)+是什么(isw)   
            gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.desc LIMIT 1"%entity
            cursor=graph.run(gql)
            return_answear = entity+'是：'
            # 循环向前移动游标
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 15:  #15=>病名(dis)+推荐药物(recomand+dru) 
            gql="MATCH (p1:Disease{ name:'%s'})-[k:recommand_drug]->(p2:Drug) RETURN p2.name"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+"推荐药物有："
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 16:  #16=>病名(dis)+常用药物(drug)  
            gql="MATCH (p1:Disease{ name:'%s'})-[k:common_drug]->(p2:Drug) RETURN p2.name"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+"常用药物有："
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 17:  #17=>科室名(dep)+包含(contain)+病(disease)  
            gql="MATCH (p1:Disease)-[k:belongs_to]->(p2:Department{ name:'%s'}) RETURN p1.name"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+"治疗的疾病有："
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 18:  #18=>科室名(dep)+包含(contain)+科室(depart) 
            gql="MATCH (p1:Disease)-[k:belongs_to]->(p2:Department{ name:'%s'}) RETURN p1.name"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+"包含的科室有："
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 19:  #19=>药物（drug）+疾病（disease）  
            gql="MATCH (p1:Disease)-[k:recommand_drug]->(p2:Drug{ name:'%s'}) RETURN p1.name"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear = entity+"能治疗的疾病有："
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
            gql="MATCH (p1:Disease)-[k:common_drug]->(p2:Drug{ name:'%s'}) RETURN p1.name"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    if relation == 20:  #20=>检查（check）+疾病（disease） 
            gql="MATCH (p1:Disease)-[k:need_check]->(p2:Check{ name:'%s'}) RETURN p1.name"%entity
            cursor=graph.run(gql)
            # 循环向前移动游标
            return_answear=entity+"需要的检查有："
            while cursor.forward():
                    # 获取并打印当前的结果集
                    record=cursor.current
                    return_answear = return_answear + '  ' + record[0]
    # if relation == 22:
    #         gql="MATCH (p1:Disease{ name:'%s'}) RETURN p1.cause LIMIT 1"%entity
    #         cursor=graph.run(gql)
    #         # 循环向前移动游标
    #         while cursor.forward():
    #                 # 获取并打印当前的结果集
    #                 record=cursor.current
    #                 print(entity+'的病因是：',record)

    return '—— ### ——' + return_answear 