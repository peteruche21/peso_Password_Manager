import random
import string
import requests
import hashlib
from send_email import Emailing
from models import ActionDB


def start():
    print('''
    what will you like to do
    enter psw 'NAME' to retrieve the psw:
    enter 'NEW' to generate a unique an secure password
    enter 'ALL' to print all your passwords    
    ''')
    action = input('>>>\n').casefold()

    def main_vault(action):

        if action != 'new' or action != 'all':
            try:
                requested_password = ActionDB().one_psw(action)
                print(requested_password)
            except Exception:
                print('i dont understand that')
                start()

        elif action == 'new':
            length = int(input('enter password length\n'))
            name = input(
                'input the name to be associated with your password\n')
            generator = PswGenerator(length)
            new_password = generator.gen()
            ActionDB().new_psw(name, new_password)

        elif action == 'all':
            all_passwords = ActionDB().all_psw()
            for item in all_passwords:
                print(item)

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


def pwnge_api(query):
    response = requests.get('https://api.pwnedpasswords.com/range/' + query)
    if response.status_code != 200:
        print(f'error fetching data {query} check status code')
    return response


def get_psw_leak_count(hashes, hashtocheck):
    hashes = (lines.split(':') for lines in hashes)
    for h, leak_count in hashes:
        if h == hashtocheck:
            return leak_count
    return 0


def check_pwnge(password):
    hashed_psw = hashlib.sha1(password.encode('UTF-8')).hexdigest().upper()
    head, tail = hashed_psw[:5], hashed_psw[5:]
    response = pwnge_api(head).text.splitlines()
    return get_psw_leak_count(response, tail)


def first_time_psw():
    try:
        master_key = ActionDB().custom_action('SELECT ID', 1)
        if master_key:
            print('you already have a key')
            main()
    except Exception:
        print('please set up ypur psw manager master key')
        password = input('enter a new password\n>>> ')
        password_again = input('enter password again\n>>> ')
        if password != password_again:
            print('check your details and try again')
            first_time_psw()
        else:

            ActionDB().master_key(password, username, email_address)
            print('master key created succesfully')

            def next_action():
                print("type 'next' to continue")
                print("type 'quit' to exit")
                action = input('>>>').casefold()

                if action == 'next':
                    start()
                elif action == 'quit':
                    print('thank you')
                    quit()
                else:
                    next_action()

            next_action()


def one_time_login():
    print('enter your one time password')
    one_time_psw = input('>>>\n')
    saved_reset_key = ActionDB().custom_action('SELECT VALUE', 3)
    if one_time_psw == saved_reset_key:

        def create_new_master_key():
            new_master_key = input('enter your new master key\n>>>')
            new_master_key_match = input(
                'enter your new master key again\n>>>')
            if new_master_key == new_master_key_match:
                ActionDB().update_master(new_master_key)
                print('master key changed sucessfully.\nloging in....\n\n\n')
                authentication(new_master_key)
            else:
                print('key mismatch')
                create_new_master_key()

        create_new_master_key()
    else:
        print('wrong!!!')
        one_time_login()


def master_key_reset():
    print('enter your email')
    email = input('>>>\n')
    db = ActionDB()
    one_time_password = PswGenerator(16).gen()
    get_reset_key_and_email = db.one_time_psw(one_time_password)
    name = db.custom_action('SELECT NAME', 2)

    if get_reset_key_and_email[1] == email:
        try:
            Emailing().send(email, one_time_password, name)
        except Exception:
            print(
                'an error occured while sending an email\ntry again in 30 seconds'
            )
            quit()
        one_time_login()
    else:
        print('email not associated with your password manager')
        master_key_reset()


def wrong_key():
    print("wrong key try again or type 'RESET' to recover")
    entry = input('>>>\n')
    if entry == 'reset'.casefold():
        master_key_reset()
    else:
        authentication(entry)


def authentication(password):
    key = password
    try:
        master_key = ActionDB().custom_action('SELECT VALUE', 1)
        if master_key == key:
            print('logged in successfully')
            start()
        else:
            wrong_key()
    except Exception:
        first_time_psw()


def credential():
    name = input('please enter your firstname\n>>>')
    email = input('please enter your email\n>>>')
    global username
    global email_address
    username = name
    email_address = email
    return name, email


def main():
    # check if it is first time user
    user = 'User'
    try:
        name = ActionDB().custom_action('SELECT NAME', 2)
        if name:
            user = name
    except Exception:
        user = credential()[0]

    print(f'''
        welcome {user}, to your python password manager
        you dont have to recycle password anymore
        **********************
        enter your master key:
        **********************
        enter 'NONE' to create one:
        enter 'RESET' to reset key:

        ''')
    first_input = input('>>>\n')
    if first_input.casefold() == 'none':
        first_time_psw()
    elif first_input.casefold() == 'reset':
        master_key_reset()
    else:
        authentication(first_input)


if __name__ == '__main__':
    main()

# however am not done i am meant to

# comment the code for readability
# build a GUI for it
# create a toast notifier to show compromised password names
# add a 'security check completed' voice relay when pwnage check is completed
# package it into a executable
