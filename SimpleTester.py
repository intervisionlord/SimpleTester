from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QFileDialog
from yaml import full_load as loadyaml
from pathlib import Path as path
import sys
import gui

class MainApp(QMainWindow, gui.Ui_main_window):
    def __init__(self):
        super().__init__()
        reset_icon = QIcon(':/imgs/reset.png')
        open_icon = QIcon(':/imgs/open.png')
        window_icon = QIcon(':/imgs/flask.png')
        self.setupUi(self)
        self.setWindowTitle('Simple Tester')
        self.setWindowIcon(window_icon)
        self.btn_open.setIcon(open_icon)
        self.btn_reset.setIcon(reset_icon)
        self.testbody = 0
        self.question_number = 1
        self.result = 0
        self.questions_count = 0
        self.test_path = 0
        self.label_test_question.setWordWrap(True)
        self.btn_var1.clicked.connect(lambda: self.respond(self.btn_var1.text()))
        self.btn_var2.clicked.connect(lambda: self.respond(self.btn_var2.text()))
        self.btn_var3.clicked.connect(lambda: self.respond(self.btn_var3.text()))
        self.btn_var4.clicked.connect(lambda: self.respond(self.btn_var4.text()))
        
        self.btn_var1.setEnabled(False)
        self.btn_var2.setEnabled(False)
        self.btn_var3.setEnabled(False)
        self.btn_var4.setEnabled(False)
        
        self.btn_open.clicked.connect(self.open_dialog)
        self.btn_reset.clicked.connect(self.test_reset)
    
    def start_test(self):
        self.questions_count = len(self.testbody)
        test_question_block = self.testbody['q1']
        self.label_test_question.setText(test_question_block[0])
        self.btn_var1.setText(test_question_block[1])
        self.btn_var2.setText(test_question_block[2])
        self.btn_var3.setText(test_question_block[3])
        self.btn_var4.setText(test_question_block[4])
        
        self.btn_var1.setEnabled(True)
        self.btn_var2.setEnabled(True)
        self.btn_var3.setEnabled(True)
        self.btn_var4.setEnabled(True)
        
    def respond(self, variant):
        test_question_block = self.testbody[f'q{self.question_number}']
        if str(variant) == str(test_question_block[5]):
            self.result += 1
        self.next_question()
        
    def next_question(self):
        self.question_number += 1
        try:
            test_question_block = self.testbody[f'q{self.question_number}']
        except KeyError:
            self.btn_var1.setEnabled(False)
            self.btn_var2.setEnabled(False)
            self.btn_var3.setEnabled(False)
            self.btn_var4.setEnabled(False)
            
            print(self.questions_count)
            self.test_end()
            return

        self.label_test_question.setText(test_question_block[0])
        self.btn_var1.setText(test_question_block[1])
        self.btn_var2.setText(test_question_block[2])
        self.btn_var3.setText(test_question_block[3])
        self.btn_var4.setText(test_question_block[4])
    
    def load_test(self):
        with open(self.test_path, 'r', encoding = 'utf-8') as testfile:
            self.testbody = loadyaml(testfile)
        title = path(self.test_path).stem
        self.setWindowTitle(title)

        self.start_test()
    
    def test_reset(self):
        def reset_confirmed():
            self.question_number = 1
            self.result = 0
            self.questions_count = 0
            self.load_test()
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.setWindowTitle('Начать тест заново?')
        msg_box.setText('Тест начнется заново, с первого вопроса.\n' +
                        'Текущие результаты не будут сохранены.\n\n' +
                        'Вы уверены?')
        returnValue = msg_box.exec()
        if returnValue == QMessageBox.Ok:
            reset_confirmed()
    
    def test_end(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Результат теста')
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(f'Правильных ответов: {self.result} из {self.questions_count}')
        msg_box.exec_()
    
    def open_dialog(self):
        self.test_path = QFileDialog.getOpenFileName(self, 'Открыть файл теста', 'tests', '*.yaml')[0]
        if self.test_path != '':
            self.load_test()
        else:
            pass

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()