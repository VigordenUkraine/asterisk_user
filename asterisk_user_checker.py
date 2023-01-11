from PyQt5.QtWidgets import QTabWidget,QWidget,QHBoxLayout,QVBoxLayout,QPushButton,QTextEdit,QLabel,QLineEdit,QApplication,QFileDialog
from PyQt5 import QtCore
from paramiko import SSHClient
import paramiko
import sys,os


class MainProgram(QWidget):
    def __init__(self):
        super().__init__()
        self.save_path=''
        self.displayUI()


    def displayUI(self):
        self.setWindowTitle('Asterisk actie user_checker')
        self.resize(1000,600)
        hbox=QHBoxLayout()



        ip_label=QLabel('SHH IP:')
        self.ip_input=QLineEdit('194.247.12.27')

        port_label = QLabel('Port:')
        self.port_input = QLineEdit('8222')

        user_label = QLabel('User:')
        self.user_input = QLineEdit('admin_a1')

        password_label = QLabel('Password:')
        self.password_input = QLineEdit('XXXXXXXXXXXX')
        self.password_input.setEchoMode(QLineEdit.Password)






        hbox.addWidget(ip_label)
        hbox.addWidget(self.ip_input)

        hbox.addWidget(port_label)
        hbox.addWidget(self.port_input)

        hbox.addWidget(user_label)
        hbox.addWidget(self.user_input)

        hbox.addWidget(password_label)
        hbox.addWidget(self.password_input)


        hbox_bottom=QHBoxLayout()

        username_label=QLabel('Username:')
        self.username=QLineEdit()
        hbox_bottom.addWidget(username_label)
        hbox_bottom.addWidget(self.username)

        vbox=QVBoxLayout(self)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_bottom)
        vbox.addWidget(QLabel('Результат:'))

        self.result_text=QTextEdit()
        vbox.addWidget(self.result_text)



        self.start_button=QPushButton('Проверить')
        self.start_button.setEnabled(True)
        self.start_button.clicked.connect(self.handler)



        vbox.addWidget(self.start_button)

        self.setLayout(vbox)
        self.show()

    def handler(self):

        ssh_client = SSHClient()
        host = str(self.ip_input.text())
        port = int(self.port_input.text())
        username = str(self.user_input.text())
        password = str(self.password_input.text())



        try:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=host, port=port, username=username, password=password)

            command="sudo asterisk -rx 'sip show peers' | grep "+self.username.text()+" | awk '{print $6}'"

            #stdin, stdout, stderr = ssh_client.exec_command("sudo asterisk -rx 'sip show peers' | grep {} | awk '{print $6}'".format(str(self.username.text())))
            stdin, stdout, stderr = ssh_client.exec_command(command)
            data = stdout.read()
            data = data.decode('utf-8').strip('\n')

            #print(data)
            if data=='OK':
                self.result_text.setText('Пользователь активен')
            else:
                self.result_text.setText('Пользователь не активен')
        except Exception:
            pass


if __name__=='__main__':
    app = QApplication(sys.argv)
    window=MainProgram()

    sys.exit(app.exec_())