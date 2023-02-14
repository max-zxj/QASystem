try:
    f = open("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_symptom1.txt", "r",encoding='utf-8')
    fnew = open("d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/dic/name_symptom.txt", "w",encoding='utf-8')
    entities = f.read().splitlines()
    for entity in entities:
        fnew.write(entity+' sym\n')
except IOError:
    print('警告：文件写入失败')
finally:
    f.close()
    fnew.close()



