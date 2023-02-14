#获得句子中实体与属性

def get_relation(n_attri_list,n_attri_aux_list):
    relation = []
    if('rea' in n_attri_list):  #1=>病名(dis)+原因(rea)  
        relation.append(1)
    if('pre' in n_attri_list):  #2=>病名(dis)+预防(pre)    
        relation.append(2)
    if('con' in n_attri_list or ('simul' in n_attri_aux_list and 'disease' in n_attri_aux_list )):  #3=>病名(dis)+并发症(con | simul+disease)     
        relation.append(3)
    if('symt' in n_attri_list):  #4=>病名(dis)+症状(symt)   
        relation.append(4)
    if('time' in n_attri_aux_list and ('rat' in n_attri_aux_list or 'the' in n_attri_list)):  #5=>病名(dis)+治疗时间(rat|the+time)   
        relation.append(5)
    if('check' in n_attri_list):  #6=>病名(dis)+检查方法(check)   
        relation.append(6)
    if('the' in n_attri_list):  #7=>病名(dis)+治疗方法(the)   
        relation.append(7)
    if('peop' in n_attri_list):  #11=>病名(dis)+易感人群(peop)   
        relation.append(11)
    if('rat' in n_attri_aux_list and 'tio' in n_attri_aux_list ):  #12=>病名(dis)+治愈概率(rat+tio)   
        relation.append(12)
    if('isw' in n_attri_list):  #14=>病名(dis)+是什么(isw)   
        relation.append(14)


    if('not' in n_attri_aux_list and ('foo' in n_attri_aux_list or 'diet' in n_attri_aux_list)):  #8=>病名(dis)+忌吃食物(not+foo|diet)   
        relation.append(8)
    elif('foo' in n_attri_aux_list):  #9=>病名(dis)+宜吃食物(foo)   
        relation.append(9)
    elif('die' in n_attri_list):  #10=>病名(dis)+推荐食谱(diet)   
        relation.append(10)


    if('contain' in n_attri_aux_list and 'depart' in n_attri_list):  #18=>科室名(dep)+包含(contain)+科室(depart)     
        relation.append(18)
    elif('depart' in n_attri_list or 'department' in n_attri_list ):  #13=>病名(dis)+科室(depart+department)   
        relation.append(13)


    if('dru' in n_attri_aux_list and 'recommand' in n_attri_aux_list ):  #15=>病名(dis)+推荐药物(recomand+dru)   
        relation.append(15)
    elif('dru' in n_attri_aux_list):  #16=>病名(dis)+常用药物(drug)   
        relation.append(16)


    if('contain' in n_attri_aux_list and 'disease' in n_attri_aux_list):  #17=>科室名(dep)+包含(contain)+病(disease)  
        relation.append(17)
    elif('disease' in n_attri_aux_list):  #19=>药物（drug）/20检查（check）/21症状（sym）+疾病（disease）  
        relation.append(19)
    

    #以食物为实体的还没想好
    # if('contain' in n_attri_aux_list and 'disease' in n_attri_aux_list):  #22=>食物+有益于+疾病  
    #     relation.append(22)
  
    return relation



def entity_match_relation(entity,relation):
    result = 0
    #定义可以存在的关系
    disease_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    drug_lst = [19]
    depart_list = [17,18]
    sym_list = [19]
    check_list = [19]
    if entity[0] == 'sym' and relation in sym_list:
        result = 21
    if entity[0] == 'drug' and relation in drug_lst:
        result = 19
    if entity[0] == 'che' and relation in check_list:
        result = 20
    if entity[0] == 'dep' and relation in depart_list:
        result = relation 
    if entity[0] == 'dis' and relation in disease_list:
        result = relation   

    return result
