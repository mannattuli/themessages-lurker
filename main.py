from lxml import html
import requests
import os
import random
from termcolor import colored

link = 'https://themessages.herokuapp.com/'

banner = '''

████╗████████╗██╗░░██╗███████╗███╗░░░███╗███████╗░██████╗░██████╗░█████╗░░██████╗░███████╗░██████╗████╗
██╔═╝╚══██╔══╝██║░░██║██╔════╝████╗░████║██╔════╝██╔════╝██╔════╝██╔══██╗██╔════╝░██╔════╝██╔════╝╚═██║
██║░░░░░██║░░░███████║█████╗░░██╔████╔██║█████╗░░╚█████╗░╚█████╗░███████║██║░░██╗░█████╗░░╚█████╗░░░██║
██║░░░░░██║░░░██╔══██║██╔══╝░░██║╚██╔╝██║██╔══╝░░░╚═══██╗░╚═══██╗██╔══██║██║░░╚██╗██╔══╝░░░╚═══██╗░░██║
████╗░░░██║░░░██║░░██║███████╗██║░╚═╝░██║███████╗██████╔╝██████╔╝██║░░██║╚██████╔╝███████╗██████╔╝████║
╚═══╝░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═════╝░╚═════╝░╚═╝░░╚═╝░╚═════╝░╚══════╝╚═════╝░╚═══╝
'''

colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']

index_post = 2
index_reply = 0

def homepage():
    clear_screen()

    home = requests.get(link)
    tree = html.fromstring(home.content)

    global boards_nav
    boards_nav = tree.xpath('/html/body/nav/div/div/a/text()')
    boards_nav_a = tree.xpath('/html/body/nav/div/div/a/@href')

    print(colored(banner, 'yellow', attrs=['bold']))
    print('\n\n\n')
    print_nav(boards_nav)
    global usr_input
    usr_input = input('\n>> ')

    if usr_input.isnumeric():
        if int(usr_input) > 2:
            homepage()
        else:
            clear_screen()
            print('loading post...')
            new_page = requests.get(link + boards_nav_a[int(usr_input)])
            clear_screen()
            global new_tree
            new_tree = html.fromstring(new_page.content)
            print_posts(new_tree, boards_nav[int(usr_input)])
    else:
        homepage()

def print_nav(xpath):
    for i in range(len(xpath)):
        randomNum = random.randint(0, 5)
        board_name = xpath[i].replace(' ', '')
        print(colored(f'({i}){board_name}', f'{colors[int(randomNum)]}', attrs=['bold']), end=' ')

def print_posts(tree, board):
    clear_screen()

    global post_id
    post_id = tree.xpath(f'/html/body/div[3]/div[{index_post}]/div[1]/text()')
    title = tree.xpath(f'/html/body/div[3]/div[{index_post}]/div[2]/a/text()')
    username = tree.xpath(f'/html/body/div[3]/div[{index_post}]/div[3]/a/text()')
    post_time = tree.xpath(f'/html/body/div[3]/div[{index_post}]/div[3]/time/text()')
    post = tree.xpath(f'/html/body/div[3]/div[{index_post}]/div[4]/text()')
    board = board.replace(' ', '')

    print(colored(f'{board}', 'red', attrs=['bold']) + '\n')

    posts = tree.xpath('/html/body/div[3]/div')
    
    text = ''
    
    for element in username:
        text += str(colored(element, 'magenta', attrs=['bold']) + '  ')

    for element in post_time:
        text += str(colored(element, attrs=['bold']) + '  ')

    for element in post_id:
        # global post_id
        post_id = int(element)
        text += str(colored('No.'+element, 'red', attrs=['bold']))
    
    print(colored(text))

    for element in title:
        print(colored(element, 'cyan', attrs=['bold']))

    for element in post:
        print(colored(element, 'green', attrs=['bold']))

    print('\n0 - View the replies\n1 - View next post')

    view_next = input('\n>> ')

    if int(view_next) == 1:
        next_post()
    elif int(view_next) == 0:
        next_reply()

def print_replies(tree):
    reply_username = tree.xpath(f'/html/body/div[5]/div/div[{index_reply}]/span/a/text()')
    reply_time = tree.xpath(f'/html/body/div[5]/div/div[{index_reply}]/div[2]/text()')
    reply_body = tree.xpath(f'/html/body/div[5]/div/div[{index_reply}]/div[3]/text()')

    text = ''
    for element in reply_username:
        text += str(colored(element, 'magenta', attrs=['bold']) + '  ')

    for element in reply_time:
        text += str(colored(element, attrs=['bold']) + '  ')

    print('\n'+str(text))

    for element in reply_body:
        print(colored(element, 'green', attrs=['bold']))

    print('\n0 - View the next reply\n1 - View next post')

    view_next = input('\n>> ')

    if int(view_next) == 1:
        next_post()
    elif int(view_next) == 0:
        next_reply()

def next_post():
    global index_post
    index_post += 1
    print_posts(new_tree, boards_nav[int(usr_input)])

def next_reply():
    global index_reply
    index_reply += 1
    new_page_reply = requests.get(link + '/void/' + str(post_id))
    new_tree_reply = html.fromstring(new_page_reply.content)
    print_replies(new_tree_reply)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    homepage()