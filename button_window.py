from PySide2 import QtGui
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QFileDialog,QLineEdit
from data import Class_info
class Group_window:
    def __init__(self):
        #加载小组加分界面
        self.ui = QUiLoader().load('ui/group.ui')
        '''
        信号槽
        '''
        self.ui.group_id_box.activated.connect(self.get_group_name)  # 选中组号的时候添加组员名字
        self.ui.ok_btn.clicked.connect(self.send_data)#确定按键按下后传送数据到数据库

    def get_group_name(self):
        # 根据组号回去组员名单
        group_name = Class_info.get_data("select Name "
                                         "from group_rank "
                                         "where group_id=%s"
                                         % self.ui.group_id_box.currentText())
        self.ui.name_box.clear()  # 清空combox
        for i in range(len(group_name)):  # 逐个添加组员名字
            self.ui.name_box.addItem(group_name[i][0])

    def send_data(self):
        # 获取当前名字和分数
        data = [self.ui.name_box.currentText(),
                int(self.ui.score_box.currentText())]
        # print(data)
        # 根据姓名设置个人的分数
        Class_info.set_data("update group_rank "
                            "set `value`=`value`+%d "
                            "where`NAME`='%s'" % (data[1], data[0]))
        # 计算当前的小组的总分，如果是NULL就设置成0
        group_sum_value = Class_info.get_data("select sum(ifnull(value,0)) "
                                              "from group_rank "
                                              "where `group_id`=%s"
                                              % self.ui.group_id_box.currentText())
        Class_info.set_data("update `group_rank` set `sum_value`=%d where `group_id`=%s"
                            %(group_sum_value[0][0],self.ui.group_id_box.currentText()))
        #设置加分提示
        self.ui.label_5.setText('提示：'+data[0]+' '+str(data[1])+'分！！')


class Login_admin:#登录界面
    def __init__(self):
        self.ui=QUiLoader().load('ui/login.ui')
        #设置密码隐藏

        self.ui.lineEdit.setEchoMode(QLineEdit.Password)
        '''
        信号槽
        '''
        # 确认按键
        self.ui.pushButton_4.clicked.connect(self.check_user)
        # 取消按键
        self.ui.pushButton_3.clicked.connect(self.ui.close)

    def check_user(self):#检查密码是否正确
        #获取用户名
        name=self.ui.comboBox_6.currentText()
        #获取密码
        password=int(self.ui.lineEdit.text())
        #获取真实密码
        real_password=Class_info.get_data("select `password` "
                                          "from `user` "
                                          "where `name`='%s'" % name)[0][0]
        #比较密码正确与否
        if password==real_password:#如果密码正确的话
            #关闭当前窗口
            self.ui.close()
            #打开管理员窗口
            self.show_admin_ui()
        else:#如果密码错误
            self.ui.label.setText('提示：密码错误')


    def show_admin_ui(self):#显示登录界面
        self.admin_window=Admin_window()
        self.admin_window.ui.exec_()
        pass

class Login_group:#登录界面
    def __init__(self):
        self.ui=QUiLoader().load('ui/login.ui')
        #设置密码隐藏

        self.ui.lineEdit.setEchoMode(QLineEdit.Password)
        '''
        信号槽
        '''
        # 确认按键
        self.ui.pushButton_4.clicked.connect(self.check_user)
        # 取消按键
        self.ui.pushButton_3.clicked.connect(self.ui.close)

    def check_user(self):#检查密码是否正确
        #获取用户名
        name=self.ui.comboBox_6.currentText()
        #获取密码
        password=int(self.ui.lineEdit.text())
        #获取真实密码
        real_password=Class_info.get_data("select `password` "
                                          "from `user` "
                                          "where `name`='%s'" % name)[0][0]
        #比较密码正确与否
        if password==real_password:#如果密码正确的话
            #关闭当前窗口
            self.ui.close()
            #打开管理员窗口
            self.show_admin_ui()

        else:#如果密码错误
            self.ui.label.setText('提示：密码错误')


    def show_admin_ui(self):#显示登录界面
        self.group_window=Group_window()
        self.group_window.ui.exec_()
        pass

class Admin_window:
    def __init__(self):
        #加载界面
        self.ui=QUiLoader().load('ui/admin.ui')
        pixmap = QtGui.QPixmap("ui/pic/qrcode.png")
        self.ui.label_2.setPixmap(pixmap)
        '''
        信号槽
        '''
        self.ui.save_btn.clicked.connect(self.save_file)
        self.ui.pushButton_2.clicked.connect(self.show_slogan)
        self.ui.pushButton.clicked.connect(self.reset_group_score)
        self.ui.btn_set_group_id.clicked.connect(self.show_change_group)


    def save_file(self):#保存文件
        file_path,_ = QFileDialog.getSaveFileName(None, "save file", "./",'.xls')
        Class_info.output_data(file_path)

    def show_slogan(self):
        self.slogan=Slogan_window()
        self.slogan.ui.exec_()
    def reset_group_score(self):#重置小组以及个人分数
        order='update `group_rank` set `value`=0'
        Class_info.set_data(order)
        order='update `group_rank` set `sum_value`=0'
        Class_info.set_data(order)
        self.ui.label_3.setText('提示：已重置，请重启。')
    def show_change_group(self):
        self.group_id_ui=Group_id()
        self.group_id_ui.ui.exec_()
        pass

class Personal_window:
    def __init__(self):
        self.ui=QUiLoader().load('ui/personal.ui')
        #装入学号
        for i in range(1,49):
            self.ui.stuid_box.addItem(str(i))
        '''
        信号槽
        '''
        self.ui.stuid_box.activated.connect(self.show_name)#当选中学号时，label显示对应学号的名字
        self.ui.pushButton_4.clicked.connect(self.send_data)

    def show_name(self):
        name=Class_info.get_data("select `name` from `personal_rank` where `ID`=%d" %int(self.ui.stuid_box.currentText()))[0][0]
        self.ui.name_label.setText(name)
    def send_data(self):
        data=[self.ui.event_box.currentText(),self.ui.stuid_box.currentText(),self.ui.comboBox_8.currentText()]


        self.ui.label.setText('提示：'+self.ui.name_label.text()+data[0]+'-'+data[2]+'分！')

class Slogan_window:
    def __init__(self):
        self.ui=QUiLoader().load('ui/slogan.ui')

        '''
        信号槽函数
        '''
        self.ui.comboBox.activated.connect(self.show_old_slogan_name)#显示旧口号
        self.ui.pushButton.clicked.connect(self.change_slogan)#修改口号
        self.ui.pushButton_2.clicked.connect(self.ui.close)#关闭窗口

    def show_old_slogan_name(self):
        self.index=int(self.ui.comboBox.currentText())
        old_slogan_name=Class_info.get_data("select `slogan`,`group_name` from `group_slogan` where `group_id`=%d"%self.index)[0]
        self.ui.label_3.setText(old_slogan_name[0])
        self.ui.label_8.setText(old_slogan_name[1])
    def change_slogan(self):
        new_slogan=self.ui.lineEdit.text()
        Class_info.set_data("update `group_slogan` set `slogan`='%s' where `group_id`=%d"%(new_slogan,self.index))
        self.ui.label_5.setText("提示：已修改！请重启系统。")
    def change_name(self):
        new_name=self.ui.lineEdit_2.text()
        Class_info.set_data("update `group_slogan` set `group_name`='%s' where `group_id`=%d"%(new_name,self.index))
        self.ui.label_9.setText("提示：已修改！请重启系统。")

class Group_id:
    def __init__(self):
        self.ui=QUiLoader().load('ui/change_group_id.ui')
        self.ui.pushButton.clicked.connect(self.change_id)
        self.ui.comboBox.activated.connect(self.get_group_name)  # 选中组号的时候添加组员名字
        self.ui.pushButton_2.clicked.connect(self.ui.close)#关闭窗口



    def change_id(self):
        new_id=self.ui.comboBox_3.currentText() #获得新的组号
        name=self.ui.comboBox_2.currentText()
        order='update `group_rank` set `group_id`=%d where `name`="%s"'%(int(new_id),name)
        Class_info.set_data(order)
        self.ui.label_4.setText('提示：已修改！')
        pass
    def get_group_name(self):
        # 根据组号回去组员名单
        group_name = Class_info.get_data("select Name "
                                         "from group_rank "
                                         "where group_id=%s"
                                         % self.ui.comboBox.currentText())
        self.ui.comboBox_2.clear()  # 清空combox
        for i in range(4):  # 逐个添加组员名字
            self.ui.comboBox_2.addItem(group_name[i][0])

