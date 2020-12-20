from controller import Controller

cont = Controller()

flag = 0

while flag >= 0:
    if flag == 0:
        flag += cont.init_menu_control()
    elif flag == 100:
        flag += cont.master_menu_control()
    elif flag % 10 == 1:
        flag += cont.stock_menu_control()
    elif flag % 10 == 2:
        flag += cont.predicts_menu_control()
