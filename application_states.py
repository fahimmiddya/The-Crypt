#Application states refer to the different states/windows the user is in. Ex : Main Menu is one state and upon clicking the sign up button we are directed to the signup window which is the another state.
#Similarly upon clicking a button we are redirected to different windows aka states of the app.
#The GUI file upon executing a state , sets a variable called 'self.state' to be that state number. Ex: Upon executing MAIN_MENU , self.state is set to be 1.
import enum
class ApplicationStates(enum.Enum):
    MAIN_MENU = 1
    SIGN_UP = 2
    LOGIN = 3
    ADD_SERVICE = 4
    CHECK_SERVICE = 5
    UPDATE_SERVICE = 6
    DELETE_SERVICE = 7
