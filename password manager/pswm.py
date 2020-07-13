import random
import string
import json
import smtplib


def start():
    print('''
    what will you like to do
    enter psw 'NAME' to retrieve the psw:
    enter 'NEW' to generate a unique an secure password
    enter 'ALL' to print all your passwords    
    ''')
    action = input('>>>\n').casefold()

    def main_vault(action):
        
        if action == 'name':
            pass
        elif action == 'new':
            length = int(input('enter password length\n'))
            name = input(
                'input the name to be associated with your password\n')
            generator = PswGenerator(length)
            generator.gen()
        elif action == 'all':
            pass
        else:
            print('i dont understand that')
            start()

    main_vault(action)


class PswGenerator(object):

    upper_case = string.ascii_uppercase
    lower_case = string.ascii_lowercase
    numbers = string.digits
    symbols = string.punctuation
    psw_pool = upper_case + lower_case + numbers + symbols

    def __init__(self, pswlen):
        self.pswlen = pswlen

    def gen(self):
        ls = [i for i in PswGenerator.psw_pool]
        random.shuffle(ls)
        psw = ''.join(random.sample(ls, self.pswlen))
        tmp = psw
        return tmp


def first_time_psw():
    with open('master.json', 'r') as file:
        master_key = json.load(file)
        if master_key['name']:
            print('you already have a key')
            main()
        else:
            print('please set psw manager master key')
            a = input('enter a new password\n')
            b = input('enter password again\n')
            if a != b:
                print('check your details and try again')
                first_time_psw()
            else:
                data = {'name': a}
                with open('master.json', 'w') as file:
                    json.dump(data, file)
                print('master key created succesfully')
                def next_action():
                    print("type 'next' to continue")
                    print("type 'quit' to exit")
                    action = input('>>>\n').casefold()
                    if action == 'next':
                        start()
                    elif action == 'quit':
                        print('thank you')
                        quit()
                    else:
                        next_action()
                next_action()


def master_key_reset():
    print('enter your email')
    input('>>>')
    pass


def wrong_key():
    print("wrong key try again or type 'RESET' to recover")
    welcome = input('>>>\n')
    if welcome == 'reset' or welcome == 'RESET':
        master_key_reset()
    else:
        authentication(welcome)


def authentication(welcome):
    key = welcome
    with open('master.json', 'r') as file:
        master_key = json.load(file)

        try:
            if master_key['name'] == key:
                print('logged in successfully')
                start()
            else:
                wrong_key()
        except KeyError:
            first_time_psw()


def main():
    # check if it is first time user
    if True:
        name = input('enter your first name\n >>>')
        email = input('enter your email')
    else:
        print('''
        welcome to your python password manager
        you dont have to recycle password anymore
        **********************
        enter your master key:
        **********************
        enter 'NONE' to create one:
        enter 'RESET' to reset key:

        ''')
        welcome = input('>>>\n').casefold()
        if welcome == 'none':
            first_time_psw()
        elif welcome == 'reset':
            master_key_reset()
        else:
            authentication(welcome)


if __name__ == ('__main__'):
    main()



# however am not done i am meant to
# generate email powered password reset
# build a GUI for it
# transfer the passwords to a database rather than a json file
# package it into a executable
