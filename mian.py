from PySide2.QtWidgets import QApplication
from PySide2 import QtCore, QtWidgets
from PySide2.QtGui import QIcon
from Ui_main import Ui_Form
import config
import view


class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui = Ui_Form()
        # 初始化界面
        self.ui.setupUi(self)
        select_province = list(config.map.keys())
        select_province.insert(0, '请选择') # 在列表内位置0插入一个请选择
        # print(list(config.map.keys()))
        # print(select_province)

        # 设置赌徒按钮文字
        self.ui.map_Button.setText('地区平均气温')
        self.ui.tl_bar_Box.addItems(['请选择', '各地区最低温', '各地区最高温'])
        # self.tl_bar_Box = self.ui.tl_bar_Box.currentText()
        
        self.ui.province_Box.addItems(select_province)
        self.ui.wordcloud_line_Box.addItems(['请选择', '气温折线图', '词云天气'])


        self.ui.map_Button.clicked.connect(self.show_map)
        self.ui.tl_bar_Box.currentIndexChanged.connect(self.show_tl_bar)
        # self.ui.province_Box.currentIndexChanged.connect(self.get_provinceBox_text)
        self.ui.wordcloud_line_Box.currentIndexChanged.connect(self.show_wordcloud_line)
        # 使用界面定义的控件，也是从ui里面访问  
        # self.ui.webview.setHtml(view.wordCloud('安徽'))

    def show_map(self):
        # self.ui.webview.clearFocus
        # self.ui.webview.clearMask
        self.ui.webview.setHtml(view.map_view())
    
    def show_tl_bar(self):
        self.tl_bar_text = self.ui.tl_bar_Box.currentText()
        if self.tl_bar_text == '各地区最低温':
            self.ui.webview.setHtml(view.tl_bar_min())

        elif self.tl_bar_text == '各地区最高温':
            self.ui.webview.setHtml(view.tl_bar_max())
        else:pass
    
    def show_wordcloud_line(self):

        if self.ui.province_Box.currentText() == '请选择':
            print(self.ui.province_Box.currentText())
            self.ui.webview.setHtml('请重新选择')

        else:
            province_text = self.ui.province_Box.currentText()
            if self.ui.wordcloud_line_Box.currentText() == '气温折线图':
                self.ui.webview.setHtml(view.line_view(province_text))

            elif self.ui.wordcloud_line_Box.currentText() == '词云天气':
                self.ui.webview.setHtml(view.wordCloud(province_text))

            elif self.ui.wordcloud_line_Box.currentText() == '请选择':
                self.ui.webview.setHtml('请重新选择')


app = QApplication([])
app.setWindowIcon(QIcon('view_icon.png'))
mainw = MainWindow()
mainw.setWindowTitle('可视化小助手')

# 禁止最大化按钮（只显示最小化按钮和关闭按钮）
mainw.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)

# 禁止拉伸窗口大小
mainw.setFixedSize(mainw.width(), mainw.height())
mainw.show()
app.exec_()