def _colour():
    s = "hello, world"
    for i in range(0,201):
        a = f'\x1b[1;{i};3m%s-{s}\x1b[0m' % i
        print(a,[a])

    # print('\033[1;32;3m%s\033[0m' % s)
    # print('\033[1;33;3m%s\033[0m' % s)
    # print('\033[1;34;3m%s\033[0m' % s)
    # print('\033[1;35;3m%s\033[0m' % s)
    # print('\033[1;36;3m%s\033[0m' % s)
# _colour()

# aa = str(""\x1b[1;39;3m39\x1b[0m')
# print(aa)
# from colorama import init, Fore, Back, Style
# init(autoreset=True)

# text = str("\x1b[1;34;3m39\x1b[0m")
# print(text)

import fake_useragent

ua = fake_useragent.UserAgent()
user_agent = ua.random
print(user_agent)
