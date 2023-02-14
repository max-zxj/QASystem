import pymysql

#没有用


connection = pymysql.connect(host='localhost', port=3306, \
                                user="test", password='522279594', \
                                db='zxj', charset='utf8')    
result = ''
if connection:                                                        
    print('>> 数据库连接成功.')

    #获取一个游标对象
    cursor = connection.cursor()
    
    #写sql语句
    sql = 'select disease from disease group by disease'
    try:
        #执行SQL语句
        cursor.execute(sql)
        #获取数据
        result = cursor.fetchall()
        #将数据写入txt文件中
        f=open('d:/我的生活/学习/毕业设计/分词软件/.vscode/jieba/userdict.txt', 'w')
        # f.write(str(result))
        # f.close()
        for w in result:
            for z in w:
                f.write(z+' die\n')
        f.close()
    except:
        print('mysql error')
    finally:
        # 步骤6：关闭数据库连接引用对象
        connection.close()
        print('>> 关闭数据库连接.')