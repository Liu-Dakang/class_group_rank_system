from PySide2 import QtCore, QtGui
from PySide2.QtCore import QTimer, QDateTime
from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
import sys,button_window
from data import Class_info
class Main_window:
    def __init__(self):

        self.main_ui=QUiLoader().load('ui/main_window.ui')
        #重新设置designer不能呈现的设置
        self.reset_ui()

        #创建定时器
        self.Timer=QTimer()
        #每隔500ms更新一次
        self.Timer.start(500)
        self.Timer.timeout.connect(self.show_time)
        #设置值日表
        self.get_clean_group()

        #初始化小组分数
        self.update_group_score()

        #初始化个人分数
        self.update_rank_person()
        #初始化标题
        self.set_sologen()
        #初始化组名
        self.update_group_name()

        '''信号槽'''
        #打开小组加分
        self.main_ui.group_btn.clicked.connect(self.show_group_ui)
        #打卡管理员登录
        self.main_ui.admin_btn.clicked.connect(self.show_admin_login_ui)
        #个人加分窗口
        self.main_ui.pushButton_2.clicked.connect(self.show_person_ui)
        self.main_ui.pushButton_4.clicked.connect(self.main_ui.close)
        '''
        功能函数
        '''

    def show_time(self):#显示时间
        self.main_ui.label_shijian.setText(QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss dddd'))

    def get_clean_group(self):#获取值日，设置值日人员
        #获取当前星期
        weekday=QDateTime.currentDateTime().toString('dddd')
        #通过数据库查询当前星期的值日学生
        clean_group=Class_info.get_data("select %s from clean" % weekday)
        #设置学生标签
        self.main_ui.label_79.setText(clean_group[0][0])
        self.main_ui.label_80.setText(clean_group[1][0])
        self.main_ui.label_81.setText(clean_group[2][0])
        self.main_ui.label_82.setText(clean_group[3][0])
        self.main_ui.label_83.setText(clean_group[4][0])
        self.main_ui.label_84.setText(clean_group[5][0])
        self.main_ui.label_85.setText(clean_group[6][0])
    def update_group_name(self):
        group_name=Class_info.get_data("select `group_name` from `group_slogan`")
        for i in range(12):
            self.name_group[i].setText(group_name[i][0])
    def update_group_score(self):#更新小组分数
        group_score=Class_info.get_data("select `sum_value` "
                                        "from `group_rank` "
                                        "group by `group_id`")
        #把分数装入label中
        for i in range(12):
            self.group_label_box[i].setText(str(group_score[i][0]))

    def update_rank_person(self):   #更新个人排名
        rank=Class_info.get_data("select `NAME`,`value` "
                                 "from `group_rank` "
                                 "order by `value` desc "
                                 "limit 10 ")
        #把分数装入label中
        for i in range(10):
            self.rang_person_box[i].setText(rank[i][0])
            self.rank_person_score[i].setText(str(rank[i][1]))

    def set_sologen(self):#设置最高分小组的口号
        #查询最高分得小组号
        index=Class_info.get_data("select distinct `group_id` "
                                  "from `group_rank` "
                                  "ORDER BY `sum_value` DESC LIMIT 1")[0][0]
        #获取最高分小组的口号
        silogen=Class_info.get_data("select `slogan` "
                                    "from `group_slogan` "
                                    "where `group_id`=%d"%index)[0][0]
        #设置口号的label
        self.main_ui.label_86.setText(silogen+'--第%d小组'%index)

    def show_group_ui(self):#显示小组加分界面
        self.group_login_window=button_window.Login_group()
        self.group_login_window.ui.exec_()
        # self.group_window=button_window.Group_window()
        # #等待退出
        # self.group_window.ui.exec_()
        #退出后更新小组和个人分数，以及组队的口号
        self.update_group_score()
        self.update_rank_person()
        self.set_sologen()

    def show_person_ui(self):#显示个人加分界面
        #加载界面窗口
        self.person_window=button_window.Personal_window()
        #显示界面，等待退出
        self.person_window.ui.exec_()


    def show_admin_login_ui(self):#显示管理员登录窗口
        self.login_window=button_window.Login_admin()
        self.login_window.ui.exec_()

    def reset_ui(self):#某些通过designer不能进行显示的设置
        #获取图片，装入label
        pixmap = QtGui.QPixmap("ui/pic/loge.png")
        self.main_ui.label_biaozhi.setPixmap(pixmap)
        pixmap = QtGui.QPixmap("ui/pic/title.png")
        self.main_ui.label_biaoti.setPixmap(pixmap)
        pixmap = QtGui.QPixmap("ui/pic/silogen.png")
        self.main_ui.label_biaoyu.setPixmap(pixmap)
        pixmap = QtGui.QPixmap("ui/pic/rank.png")
        self.main_ui.label_6.setPixmap(pixmap)
        gif=QtGui.QMovie('ui/pic/study.gif')
        self.main_ui.label_gif.setMovie(gif)
        gif.start()
        btn_style='''QPushButton{
        background-color: rgba(152, 152, 152, 180);
        font: 20pt "新宋体";
        border-radius:10px;
        }
        QPushButton::hover{
        background-color: rgba(255, 255, 255, 180);
        }'''
        #设置按键样式
        self.main_ui.group_btn.setStyleSheet(btn_style)
        self.main_ui.pushButton_2.setStyleSheet(btn_style)
        self.main_ui.admin_btn.setStyleSheet(btn_style)
        self.main_ui.pushButton_4.setStyleSheet(btn_style)
        #设置个人分数排名
        self.rang_person_box=[self.main_ui.rank_1,self.main_ui.rank_2,self.main_ui.rank_3,
                              self.main_ui.rank_4,self.main_ui.rank_5,self.main_ui.rank_6,
                              self.main_ui.rank_7,self.main_ui.rank_8,self.main_ui.rank_9,self.main_ui.rank_10]
        self.rank_person_score=[self.main_ui.label_17,self.main_ui.label_18,self.main_ui.label_19,
                                self.main_ui.label_20,self.main_ui.label_21,self.main_ui.label_22,
                                self.main_ui.label_23,self.main_ui.label_24,self.main_ui.label_25,self.main_ui.label_26]
        #设置小组分数组
        self.group_label_box=[self.main_ui.group_1_lab,self.main_ui.group_2_lab,self.main_ui.group_3_lab,
                            self.main_ui.group_4_lab,self.main_ui.group_5_lab,self.main_ui.group_6_lab,
                            self.main_ui.group_7_lab,self.main_ui.group_8_lab,self.main_ui.group_9_lab,
                            self.main_ui.group_10_lab,self.main_ui.group_11_lab,self.main_ui.group_12_lab]

        self.name_group=[self.main_ui.name_1,self.main_ui.name_2,self.main_ui.name_3,self.main_ui.name_4,
                                self.main_ui.name_5,self.main_ui.name_6,self.main_ui.name_7,self.main_ui.name_8,
                                self.main_ui.name_9,self.main_ui.name_10,self.main_ui.name_11,self.main_ui.name_12]

if __name__ == '__main__':
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)#高分辨率自适应
    app = QApplication(sys.argv)
    main_window=Main_window()
    main_window.main_ui.show()
    app.exec_()
    Class_info.exit_db()
    sys.exit()