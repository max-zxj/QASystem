from get_relation import entity_match_relation

def get_word(entity,relation):
    hint = ''
    if relation == 1:  #1=>病名(dis)+原因(rea)  
        hint = '如：%s的病因是什么？'%entity
    if relation == 2:  #2=>病名(dis)+预防(pre)    
        hint = '如：%s应该如何预防？'%entity
    if relation == 3:  #3=>病名(dis)+并发症(con | simul+disease)     
        hint = '如：%s的并发症有哪些？'%entity
    if relation == 4:  #4=>病名(dis)+症状(symt)   
        hint = '如：%s的症状有什么？'%entity
    if relation == 5:  #5=>病名(dis)+治疗时间(rat|the+time)   
        hint = '如：%s的治疗时间是多长？'%entity
    if relation == 6:  #6=>病名(dis)+检查方法(check)   
        hint = '如：%s的检查方法是什么？'%entity
    if relation == 7:  #7=>病名(dis)+治疗方法(the)   
        hint = '如：%s的治疗方法是什么？'%entity
    if relation == 11:  #11=>病名(dis)+易感人群(peop)   
        hint = '如：%s的易感人群有哪些？'%entity
    if relation == 12:  #12=>病名(dis)+治愈概率(rat+tio)   
        hint = '如：%s的治愈概率是多少？'%entity
    if relation == 14:  #14=>病名(dis)+是什么(isw)   
        hint = '如：%s的是什么？'%entity
    if relation == 8:  #8=>病名(dis)+忌吃食物(not+foo|diet)   
        hint = '如：%s的治病原因是什么？'%entity
    if relation == 9:  #9=>病名(dis)+宜吃食物(foo)   
        hint = '如：%s有什么忌吃食物？'%entity
    if relation == 10:  #10=>病名(dis)+推荐食谱(diet)   
        hint = '如：%s有什么推荐食谱？'%entity
    if relation == 18:  #18=>科室名(dep)+包含(contain)+科室(depart)     
        hint = '如：%s下面包含哪些科室？'%entity
    if relation == 13:  #13=>病名(dis)+科室(depart+department)   
        hint = '如：%s在哪个科室看？'%entity
    if relation == 15:  #15=>病名(dis)+推荐药物(recomand+dru)   
        hint = '如：%s有什么推荐药物？'%entity
    if relation == 16:  #16=>病名(dis)+常用药物(drug)   
        hint = '如：%s有什么常用药物？'%entity
    if relation == 17:  #17=>科室名(dep)+包含(contain)+病(disease)  
        hint = '如：%s能治疗哪些疾病？'%entity
    if relation == 19:  #19=>药物（drug）+疾病（disease）  
        hint = '如：%s能治疗那些疾病？'%entity
    if relation == 20:  #19=>20检查（check）+疾病（disease）  
        hint = '如：%s能检查那些疾病？'%entity

    return hint




def get_hint(entity_list,relation):
    hint = ''
    #先遍历实体再遍历属性
    for item in entity_list:
        for item_r in relation:
            relation_one = entity_match_relation(item,item_r)
            if relation_one != 0:
                hint = get_word(item[1],relation_one)
                return hint
    
    return hint




