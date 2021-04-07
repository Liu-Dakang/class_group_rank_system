import sqlite3
import xlwt

class Database:
    def __init__(self):
        self.class_db=sqlite3.connect('test.db')
        self.cur=self.class_db.cursor()
        print('database is on')
    def get_data(self,order):
        self.cur.execute(order)
        return self.cur.fetchall()
    def set_data(self,order):
        self.cur.execute(order)
        self.class_db.commit()
    def exit_db(self):
        self.class_db.close()
        print('database if off')
    def output_data(self,filepath):#导出数据文件
        #使用列表提取表格的名字
        table_name=[]
        #查询所有的表格名字
        self.cur.execute('select name from sqlite_master where type="table" order by name')

        results = self.cur.fetchall()

        for each in results:
            table_name.append(each[0])#存入每个表名

        work_book = xlwt.Workbook()#实例化excel操作的类
        for name in table_name:#对于每一个表的名字
            #查询表格下所有的数据
            self.cur.execute("select * from `%s`" % name)
            result = self.cur.fetchall()
            # print(result)
            fields = self.cur.description
            #按照表格名字进行sheet的创建
            sheet = work_book.add_sheet('%s' % name, cell_overwrite_ok=True)
            for field in range(0, len(fields)):#按照查询结果的顺序写入excel中
                sheet.write(0, field, fields[field][0])
            row = 1
            col = 0
            for row in range(1, len(result) + 1):
                for col in range(0, len(fields)):
                    sheet.write(row, col, u'%s' % result[row - 1][col])
        #保存在filepath路径当中
        work_book.save(r"%s.xls"%filepath)
Class_info=Database()






































































































