import doToot
import readToots


def main_menu():
    print('*************')
    print('1. do Toot')
    print('2. read toots')
    print('3. EXIT')
    print('*************')
    user_choice = input('> choice: ')

    if user_choice == '1':
        doToot.do_toot()
    elif user_choice == '2':
        readToots.read_toots()
    elif user_choice == '3':
        return False

    return True


if __name__ == '__main__':
    keep_running = True
    while keep_running:
        keep_running = main_menu()

