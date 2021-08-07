#Importing modules
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from os import path
from os import environ
import sqlite3
import sys
from application_states import *
from constants import *
from database import *
from security import *

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

class Application(object):
    def __init__(self):
        self.state = ApplicationStates.MAIN_MENU #self.state = 1 as MAIN_MENU = 1

    def setupUi(self, MainWindow):
        #  Main window setup
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
        font = QtGui.QFont()
        font.setPointSize(14)
        MainWindow.setFont(font)
        MainWindow.setFocusPolicy(QtCore.Qt.ClickFocus)
        MainWindow.setStyleSheet("")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setMinimumSize(QtCore.QSize(SCREEN_WIDTH, SCREEN_HEIGHT))
        MainWindow.setMaximumSize(QtCore.QSize(SCREEN_WIDTH, SCREEN_HEIGHT))

        #  Central widget setup
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #  Header setup
        self.header = QLabel(self.centralwidget)
        font.setPointSize(20)
        self.header.setFont(font)
        self.header.setFocusPolicy(QtCore.Qt.NoFocus)
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setObjectName("header")

        #  ------------------Buttons setup------------------

        #  Sign up button
        self.sign_up_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.sign_up_button.setFont(font)
        self.sign_up_button.clicked.connect(self.sign_up)

        #  Log in button
        self.login_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.login_button.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.login_button.clicked.connect(self.login)

        #  Main menu button
        self.main_menu_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.main_menu_button.setFont(font)
        self.main_menu_button.hide()
        self.main_menu_button.clicked.connect(self.main_menu)

        #  Show password button
        self.show_hide_password_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.show_hide_password_button.setFont(font)
        self.show_hide_password_button.hide()
        self.show_hide_password_button.clicked.connect(self.show_password)

        #  Send info button
        self.send_data = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.send_data.setFont(font)
        self.send_data.hide()
        self.send_data.clicked.connect(self.send)

        #  List saved services button
        self.list_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.list_button.setFont(font)
        self.list_button.hide()
        self.list_button.clicked.connect(self.list)

        #  Add new service button
        self.add_service_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.add_service_button.setFont(font)
        self.add_service_button.hide()
        self.add_service_button.clicked.connect(self.add)

        #  Get data from service button
        self.get_data_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.get_data_button.setFont(font)
        self.get_data_button.hide()
        self.get_data_button.clicked.connect(self.get)

        #  Update service button
        self.update_service_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.update_service_button.setFont(font)
        self.update_service_button.hide()
        self.update_service_button.clicked.connect(self.update)

        #  Delete service button
        self.delete_service_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.delete_service_button.setFont(font)
        self.delete_service_button.hide()
        self.delete_service_button.clicked.connect(self.delete_service)

        #  Delete user button
        self.delete_user_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.delete_user_button.setFont(font)
        self.delete_user_button.hide()
        self.delete_user_button.clicked.connect(self.delete_user)

        #  Logoff user button
        self.logoff_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.logoff_button.setFont(font)
        self.logoff_button.hide()
        self.logoff_button.clicked.connect(self.logoff)

        #  Cancel operation button
        self.cancel_operation_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.cancel_operation_button.setFont(font)
        self.cancel_operation_button.hide()
        self.cancel_operation_button.clicked.connect(self.cancel)

        #  ------------------LineEdit----------------------

        #  Username
        self.username = QLineEdit(self.centralwidget)
        font.setPointSize(12)
        self.username.setFont(font)
        self.username.hide()
        self.username.setPlaceholderText('Username')

        #  Password
        self.password = QLineEdit(self.centralwidget)
        font.setPointSize(12)
        self.password.setFont(font)
        self.password.hide()
        self.password.setPlaceholderText('Password')

        #  New service name
        self.service_name = QLineEdit(self.centralwidget)
        self.service_name.setFont(font)
        self.service_name.hide()
        self.service_name.setPlaceholderText('Service Name/URL')

        #  ------------------Message box setup------------------

        #  Warning box
        self.warning = QMessageBox()
        self.warning.setWindowTitle('Warning!')
        self.warning.setIcon(QMessageBox.Warning)
        self.warning.hide()

        #  Information box
        self.info = QMessageBox()
        self.info.setWindowTitle('Info')
        self.info.setIcon(QMessageBox.Information)
        self.info.hide()

        #  Listing box
        self.listing = QMessageBox()
        self.listing.setWindowTitle('Services list')
        self.listing.setIcon(QMessageBox.Information)
        self.listing.hide()

        #  Delete user box
        self.delete_user = QMessageBox()
        self.delete_user.setWindowTitle('Careful!')
        self.delete_user.setIcon(QMessageBox.Critical)
        self.delete_user.setText('Are you sure you want to do this?\nOnce you delete your account , theres no getting it back.')
        self.delete_user.setStandardButtons(QMessageBox.Yes)
        self.delete_user.buttonClicked.connect(self.delete_user_confirmation)

        self.retranslateUi(MainWindow)
        self.main_menu()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #Set texts and titles
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "The Crypt"))
        MainWindow.setWindowIcon(QtGui.QIcon('lock.png'))
        self.header.setText(_translate("MainWindow", "MAIN MENU"))
        self.sign_up_button.setText(_translate("MainWindow", "Sign up"))
        self.login_button.setText(_translate("MainWindow", "Log in"))
        self.main_menu_button.setText(_translate('MainWindow', 'Menu'))
        self.show_hide_password_button.setText(
            _translate('MainWindow', 'Show Password'))
        self.send_data.setText(_translate('MainWindow', 'Send'))
        self.list_button.setText('List Services')
        self.add_service_button.setText('Add Service/URL')
        self.get_data_button.setText('Check Password')
        self.update_service_button.setText('Update Password')
        self.delete_service_button.setText('Delete Service')
        self.delete_user_button.setText('Delete Account')
        self.logoff_button.setText('Sign Out')
        self.cancel_operation_button.setText('Cancel')

    def reset_widgets(self):
        #  Hide everything
        self.login_button.hide()
        self.sign_up_button.hide()
        self.main_menu_button.hide()
        self.password.hide()
        self.username.hide()
        self.show_hide_password_button.hide()
        self.send_data.hide()
        self.list_button.hide()
        self.add_service_button.hide()
        self.get_data_button.hide()
        self.update_service_button.hide()
        self.delete_service_button.hide()
        self.delete_user_button.hide()
        self.logoff_button.hide()
        self.service_name.hide()
        self.cancel_operation_button.hide()

        #  Clear every QLineEdit
        self.password.clear()
        self.username.clear()
        self.service_name.clear()

#Reset every widget geometry according to the size of screen
        self.header.setGeometry(
            (SCREEN_WIDTH - HEADER_WIDTH) // 2, SCREEN_HEIGHT // 6, HEADER_WIDTH, HEADER_HEIGHT)
        self.sign_up_button.setGeometry(
            2 * SCREEN_WIDTH // 5 - MAIN_MENU_BUTTON_WIDTH,
            3 * (SCREEN_HEIGHT // 2 - BUTTON_HEIGHT) // 2,
            MAIN_MENU_BUTTON_WIDTH, BUTTON_HEIGHT)
        self.login_button.setGeometry(
            4 * SCREEN_WIDTH // 5 - MAIN_MENU_BUTTON_WIDTH,
            3 * (SCREEN_HEIGHT // 2 - BUTTON_HEIGHT) // 2,
            MAIN_MENU_BUTTON_WIDTH, BUTTON_HEIGHT)
        self.main_menu_button.setGeometry(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 4 * SCREEN_HEIGHT // 5, BUTTON_WIDTH, BUTTON_HEIGHT)
        show_hide_password_button_height = 4 * SCREEN_HEIGHT // 5 - SCREEN_HEIGHT // 10
        self.show_hide_password_button.setGeometry(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, show_hide_password_button_height,
            BUTTON_WIDTH, BUTTON_HEIGHT)
        send_data_button_height = show_hide_password_button_height - SCREEN_HEIGHT // 10
        self.send_data.setGeometry(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, send_data_button_height,
            BUTTON_WIDTH, BUTTON_HEIGHT)
        self.list_button.setGeometry(
            (SCREEN_WIDTH - 3 * USER_BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 3,
            USER_BUTTON_WIDTH, USER_BUTTON_HEIGHT)
        self.add_service_button.setGeometry(
            (SCREEN_WIDTH - USER_BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 3,
            USER_BUTTON_WIDTH, USER_BUTTON_HEIGHT)
        self.get_data_button.setGeometry(
            (SCREEN_WIDTH + USER_BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 3,
            USER_BUTTON_WIDTH, USER_BUTTON_HEIGHT)
        self.update_service_button.setGeometry(
            (SCREEN_WIDTH - 3 * USER_BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 2,
            USER_BUTTON_WIDTH, USER_BUTTON_HEIGHT)
        self.delete_service_button.setGeometry(
            (SCREEN_WIDTH - USER_BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 2,
            USER_BUTTON_WIDTH, USER_BUTTON_HEIGHT)
        self.delete_user_button.setGeometry(
            (SCREEN_WIDTH + USER_BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 2,
            USER_BUTTON_WIDTH, USER_BUTTON_HEIGHT)
        self.logoff_button.setGeometry(
            (SCREEN_WIDTH - 3 * USER_BUTTON_WIDTH) // 2, 2 * SCREEN_HEIGHT // 3,
            USER_BUTTON_WIDTH * 3, USER_BUTTON_HEIGHT)
        self.cancel_operation_button.setGeometry(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 9 * SCREEN_HEIGHT // 10 - BUTTON_HEIGHT,
            BUTTON_WIDTH, BUTTON_HEIGHT)
        self.username.setGeometry(
            (SCREEN_WIDTH - ENTRY_WIDTH) // 2,  2 * (SCREEN_HEIGHT - ENTRY_HEIGHT) // 5,
            ENTRY_WIDTH, ENTRY_HEIGHT)
        self.password.setGeometry(
            (SCREEN_WIDTH - ENTRY_WIDTH) // 2,  (SCREEN_HEIGHT - ENTRY_HEIGHT) // 2,
            ENTRY_WIDTH, ENTRY_HEIGHT)
        self.service_name.setGeometry(
            (SCREEN_WIDTH - ENTRY_WIDTH) // 2, 29 * (SCREEN_HEIGHT - ENTRY_HEIGHT) // 100,
            ENTRY_WIDTH, ENTRY_HEIGHT)
        self.listing.setGeometry(550, 300, 500, 500)

#  Hide passwords
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_shown = False

#Show sign up screen
    def sign_up(self):
        self.reset_widgets()
        self.main_menu_button.show()
        self.password.show()
        self.username.show()
        self.show_hide_password_button.show()
        self.send_data.show()
        self.state = ApplicationStates.SIGN_UP #self.state = 2 as SIGN_UP=2
        self.header.setText('Sign Up')

# Show login screen
    def login(self):
        self.reset_widgets()
        self.main_menu_button.show()
        self.password.show()
        self.username.show()
        self.show_hide_password_button.show()
        self.state = ApplicationStates.LOGIN #self.state = 3 as LOGIN=3
        self.send_data.show()
        self.header.setText('Login')

# Show main menu screen
    def main_menu(self):
        self.reset_widgets()
        self.login_button.show()
        self.sign_up_button.show()
        self.state = ApplicationStates.MAIN_MENU #self.state = 1 as MAIN_MENU = 1
        self.header.setText('Welcome to the Crypt')

#To toggle between show and hide password
    def show_password(self):
        if self.password_shown:
            self.password.setEchoMode(QLineEdit.Password)
            self.password.EchoMode() == QLineEdit.Password
            self.password_shown = False
            self.show_hide_password_button.setText('Show Password')
        else:
            self.password.setEchoMode(QLineEdit.Normal)
            self.password.EchoMode() == QLineEdit.Normal
            self.password_shown = True
            self.show_hide_password_button.setText('Hide Password')

#Data from QLineEdit
    def send(self):
        if self.state == ApplicationStates.SIGN_UP:
            self.provided_username = self.username.text()
            self.provided_password = self.password.text()

            #Checks for a empty username or password
            if self.provided_username == '' or self.provided_password == '':
                self.warning.setText('You must type in a username and a password!')
                self.warning.show()
                return

            # Checks for username 
            users_list = get_usernames_list()
            for name in users_list:
                if self.provided_username == name[0]:
                    self.warning.setText('Username alredy taken')
                    self.warning.show()
                    return

            else:
                key = generate_key()
                master_hashed = get_hash(self.provided_password)
                try:
                    add_user(self.provided_username, master_hashed, key)
                    self.info.setText('User registered successully')
                    self.info.show()
                    self.main_menu()
                except sqlite3.Error:
                    self.warning.setText(sqlite3.Error)
                    self.warning.show()

        elif self.state == ApplicationStates.LOGIN:

            self.provided_username = self.username.text()
            self.provided_password = self.password.text()

            if self.provided_username == '' or self.provided_password == '':
                self.warning.setText('You must type in a username and a password!')
                self.warning.show()
                return

            provided_hash = str(get_hash(self.provided_password))

            #  Checking if user exists
            users_list = get_usernames_list()

            for user in users_list:
                if self.provided_username == user[0]:
                    if provided_hash == get_master_hashed(self.provided_username):
                        accessed = True
                        break
                    else:
                        accessed = False
                        break
            else:
                accessed = None

            if accessed:
                self.reset_widgets()
                self.user_id = get_user_id(self.provided_username)
                self.user_key = get_key(self.user_id)
                self.header.setText(f'Welcome {self.provided_username}')
                self.list_button.show()
                self.add_service_button.show()
                self.get_data_button.show()
                self.update_service_button.show()
                self.delete_service_button.show()
                self.delete_user_button.show()
                self.logoff_button.show()

            elif accessed is False:
                self.warning.setText('Wrong username/password , please try again')
                self.warning.show()

            elif accessed is None:
                self.warning.setText('User not found , please register')
                self.warning.show()

        elif self.state == ApplicationStates.ADD_SERVICE:
            service_name = self.service_name.text()
            service_username = self.username.text()
            service_password = self.password.text()

            if service_name == '' or service_username == '' or service_password == '':
                self.warning.setText('All fields are required')
                self.warning.show()
                return

            else:
                services_list = list_saved_services(self.user_id)
                for service in services_list:
                    if service_name == service[0]:
                        self.warning.setText('Service/URL alredy present')
                        self.warning.show()
                        return

                else:
                    encrypted_password = encrypt_password(
                        self.user_key, service_password)
                    add_service(service_name, service_username,
                                encrypted_password, self.user_id)
                    self.info.setText('Service/URL added successfully')
                    self.info.show()
                    self.cancel()

        elif self.state == ApplicationStates.CHECK_SERVICE:
            service_name = self.service_name.text()

            if service_name == '':
                self.warning.setText('You must type in the service name/URL !')
                self.warning.show()
                return

            services_list = list_saved_services(self.user_id)

            for service in services_list:
                if service_name == service[0]:
                    service_exists = True
                    break
            else:
                service_exists = False

            if not service_exists:
                self.warning.setText('No such service/URL exists.')
                self.warning.show()

            else:
                username, password = check_data_from_service(
                    self.user_id, service_name)
                password = decrypt_password(self.user_key, password)
                self.info.setText(
                    f'Service: {service[0]}\nUsername: {username}\nPassword: {password}')
                self.info.show()
                self.cancel()

        elif self.state == ApplicationStates.UPDATE_SERVICE:
            service_name = self.service_name.text()
            username = self.username.text()
            password = self.password.text()

            if service_name == '' or (username == '' and password == ''):
                self.warning.setText(
                    'You must choose the service/URL name and at least one of the others!')
                self.warning.show()
                return

            services_list = list_saved_services(self.user_id)

            for name in services_list:
                if name[0] == service_name:
                    service_exists = True
                    break
            else:
                service_exists = False

            if not service_exists:
                self.warning.setText('This is not a registered service/URL')
                self.warning.show()

            else:
                if username == '':
                    encrypted_password = encrypt_password(
                        self.user_key, password)
                    update_service_password(
                        self.user_id, service_name, encrypted_password)

                elif password == '':
                    update_service_username(self.user_id, service_name, username)

                elif username != '' and password != '':
                    encrypted_password = encrypt_password(
                        self.user_key, password)
                    update_service_password(
                        self.user_id, service_name, encrypted_password)
                    update_service_username(
                        self.user_id, service_name, username)

                self.info.setText('Service Name / URL updated successfully!')
                self.info.show()
                self.cancel()

        elif self.state == ApplicationStates.DELETE_SERVICE:
            service_name = self.service_name.text()

            if service_name == '':
                self.warning.setText('You must type in the service name/URL !')
                self.warning.show()
                return

            services_list = list_saved_services(self.user_id)

            for service in services_list:
                if service_name == service[0]:
                    service_exists = True
                    break
            else:
                service_exists = False

            if not service_exists:
                self.warning.setText('This is not a registered service name / URL')
                self.warning.show()

            else:
                delete_service(self.user_id, service_name)
                self.info.setText(
                    f'{service_name} was deleted successfully!')
                self.info.show()
                self.cancel()
    #List of saved services yet
    def list(self):
        services_list = list_saved_services(self.user_id)
        if len(services_list) == 0:
            self.warning.setText('There are no services/URL yet')
            self.warning.show()
        else:
            text = ''
            for i in range(len(services_list)):
                text += f'Service {i + 1}: {services_list[i][0]}\n'
            self.listing.setText(text)
            self.listing.show()

    #Add new password and service
    def add(self):
        self.reset_widgets()
        self.header.setText('New Service/URL')
        self.show_hide_password_button.show()
        self.service_name.show()
        self.username.show()
        self.password.show()
        self.send_data.show()
        self.state = ApplicationStates.ADD_SERVICE #self.state = 4 as ADD_SERVICE = 4
        self.cancel_operation_button.show()

    # Show password checking screen
    def get(self):
        self.reset_widgets()
        #  Reset widgets geometry
        self.service_name.setGeometry(
            (SCREEN_WIDTH - ENTRY_WIDTH) // 2, (SCREEN_HEIGHT -
                                                ENTRY_HEIGHT) // 2, ENTRY_WIDTH, ENTRY_HEIGHT
        )
        self.cancel_operation_button.setGeometry(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 4 * SCREEN_HEIGHT // 5 - BUTTON_HEIGHT,
            BUTTON_WIDTH, BUTTON_HEIGHT)
        self.service_name.show()

        #  Reset app state
        self.state = ApplicationStates.CHECK_SERVICE #self.state = 5 as CHECK_SERVICE = 5

        #  Show widgets
        self.send_data.show()
        self.cancel_operation_button.show()
        self.header.setText('Password Checking')

    #Show service update screen
    def update(self):
        self.reset_widgets()
        self.header.setText('Update Password')
        self.show_hide_password_button.show()
        self.service_name.show()
        self.username.show()
        self.password.show()
        self.send_data.show()
        self.state = ApplicationStates.UPDATE_SERVICE #Sets self.state = 6 as UPDATE_SERVICE = 6
        self.cancel_operation_button.show()

    #Show delete service screen
    def delete_service(self):
        self.reset_widgets()
        #  Reset widgets geometry
        self.service_name.setGeometry(
            (SCREEN_WIDTH - ENTRY_WIDTH) // 2, (SCREEN_HEIGHT -
                                                ENTRY_HEIGHT) // 2, ENTRY_WIDTH, ENTRY_HEIGHT
        )
        self.cancel_operation_button.setGeometry(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 4 * SCREEN_HEIGHT // 5 - BUTTON_HEIGHT,
            BUTTON_WIDTH, BUTTON_HEIGHT)
        self.service_name.show()

        #  Reset app state
        self.state = ApplicationStates.DELETE_SERVICE #Sets self.state = 7 as DELETE_SERVICE = 7

        #  Show widgets
        self.send_data.show()
        self.cancel_operation_button.show()
        self.header.setText('Deleting Service/URL')
    
    #Shows delete user message
    def delete_user(self):
        self.delete_user.show()

    #Show delete user confirmation
    def delete_user_confirmation(self):
        delete_user(self.user_id)
        self.delete_user.hide()
        self.info.setText('User deleted successfully!')
        self.main_menu()
        self.user_id = None
        self.user_key = None

    # Sign out
    def logoff(self):
        self.main_menu()
        self.user_id = None
        self.user_key = None

   #Cancel a operation and return to choice menu
    def cancel(self):
        self.state = ApplicationStates.LOGIN #Sets self.state = 3 as LOGIN = 3
        self.reset_widgets()
        self.header.setText(f'Welcome {self.provided_username}')
        self.list_button.show()
        self.add_service_button.show()
        self.get_data_button.show()
        self.update_service_button.show()
        self.delete_service_button.show()
        self.delete_user_button.show()
        self.logoff_button.show()


if __name__ == "__main__":
    suppress_qt_warnings()
    if not path.exists('passwords.db'):
        create_database()
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Application()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
