import jieba
import jieba.posseg as pseg
from match_entity import search_entity
from symptom_result import symptom_result
from get_relation import get_relation,entity_match_relation
from get_result import get_result
from get_hint import get_hint

def get_answear(str1):
        #输出的东西
        result =  "没有识别出语义，请用更加官方的话语提问。"
        hint = ''

        #引入自定实体义词典
        jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_department.txt")
        jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_check.txt")
        jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_disease.txt")
        jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_drug.txt")
        jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_food.txt")
        jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_symptom.txt")

        #引入自定义的属性词典
        jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/attribute.txt")
        jieba.load_userdict("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/attribute_aux.txt")

        #实体与属性的标识
        entityList = ['dep','che','dis','drug','food','sym']
        attriList = ['rea','pre','isw','con','symt','check','the','depart','department','peop']
        attri_auxList = ['simiul','disease','time','not','diet','foo','rat','tio','recommend','common','dru','contain']

        #分词
        words = pseg.cut(str1)
        
        #提取关键词
        n_entity = 0
        entity_list = []
        n_entity_word = []
        n_entity_flag = []
        n_attri_list = []
        n_attri_aux_list = []
        node = []
        for w in words:
                # print(w)
                 #寻找实体
                if w.flag in entityList:
                        n_entity=n_entity+1
                        n_entity_flag.append(w.flag)
                        n_entity_word.append(w.word)
                        entity_list.append([w.flag,w.word])
                        node.append([w.flag,w.word])
                #寻找属性        
                if w.flag in attriList: 
                        n_attri_list.append(w.flag)
                        node.append([w.flag,w.word])
                #寻找辅助属性        
                if w.flag in attri_auxList:
                        n_attri_aux_list.append(w.flag)
                        node.append([w.flag,w.word])

        #进行关系提取
        relation = get_relation(n_attri_list,n_attri_aux_list)
        

        #分支1（关于症状推出疾病）
        if 'sym' in n_entity_flag:
                result,hint = symptom_result(str1,entity_list,relation)
                return result,hint    #分支1输出

        #实体矫正，只匹配drug，disease和check
        if n_entity == 0:
                entity_result = search_entity(str1)
                if len(entity_result) == 0:
                        result = '输入的名词不完整或者错误，请核对是否正确'
                        hint = ''
                        return result,hint   #没有实体输出
                elif len(entity_result) == 1:
                        n_entity = 1
                        n_entity_flag.append(entity_result[0][0])
                        n_entity_word.append(entity_result[0][1])
                        entity_list = entity_result
                elif len(entity_result) > 1:
                        result = '输入的名词不完整或者错误，请核对是否正确'
                        hint = '根据您的输入，匹配度最高的名词有：'
                        for item in entity_result:
                                hint = hint + item[1] + ','
                        return result,hint   #匹配多个实体，通过输出确定

                        
        #输出尝试
        # print(n_entity)
        # print(n_entity_word,n_attri_aux_list,n_attri_list,n_entity_flag)


        #分支3（有实体有属性）
        g_result = ''
        if len(relation) == 1:   #只有一个属性的时候
                for item in entity_list:
                        relation_one = entity_match_relation(item,relation[0])
                        if relation_one != 0:
                                g_result = g_result + get_result(item[1],relation_one)
                
                if len(g_result) > 1:
                        result = g_result
                        hint = ''
        elif n_entity == 1:      #只有一个实体的时候
                for item in relation:
                        relation_one = entity_match_relation(entity_list[0],item)
                        if relation_one != 0:
                                g_result = g_result + get_result(entity_list[0][1],relation_one)
                
                if len(g_result) > 1:
                        result = g_result
                        hint = ''
        else:    #有多个属性和实体的时候
                #重新初始化参数
                n_entity = 0
                entity_list = []
                n_entity_word = []
                n_entity_flag = []
                n_attri_list = []
                n_attri_aux_list = []
                #切分node形成新的属性
                for item in node:
                        #每次以实体属性开头
                        if item[0] in entityList:
                                if n_entity == 0:   #是开头的情况
                                        n_entity= 1
                                        n_entity_flag.append(item[0])
                                        n_entity_word.append(item[1])
                                        entity_list.append([item[0],item[1]])
                                else:    #不是开头的情况
                                        # print(entity_list,n_attri_list,n_attri_aux_list)
                                        #寻找上一个的结果
                                        relation = get_relation(n_attri_list,n_attri_aux_list)
                                        for item_re in relation:
                                                relation_one = entity_match_relation(entity_list[0],item_re)
                                                if relation_one != 0:
                                                        g_result = g_result + get_result(entity_list[0][1],relation_one)
                                        
                                        #初始化参数开始本次寻找
                                        n_entity = 0
                                        entity_list = []
                                        n_entity_word = []
                                        n_entity_flag = []
                                        n_attri_list = []
                                        n_attri_aux_list = []

                                        #将信息存入
                                        n_entity= 1
                                        n_entity_flag.append(item[0])
                                        n_entity_word.append(item[1])
                                        entity_list.append([item[0],item[1]])
                        #找到属性并且已有一个实体       
                        if item[0] in attriList and n_entity == 1: 
                                n_attri_list.append(item[0])
                        #寻找辅助属性并且已有一个实体        
                        if item[0] in attri_auxList and n_entity == 1:
                                n_attri_aux_list.append(item[0])

                #处理最后一次情况
                if n_entity == 1:    #不是开头的情况
                        # print(entity_list,n_attri_list,n_attri_aux_list)
                        #寻找上一个的结果
                        relation = get_relation(n_attri_list,n_attri_aux_list)
                        for item_re in relation:
                                relation_one = entity_match_relation(entity_list[0],item_re)
                                if relation_one != 0:
                                        g_result = g_result + get_result(entity_list[0][1],relation_one)
                        

                #判断有没有找到答案
                if len(g_result) > 1:
                        result = g_result
                        hint = ''
                else:
                        result = '请一次只问一个问题'
                        #获取hint
                        hint = get_hint(entity_list,relation)

        return result,hint   #分支3的输出



       