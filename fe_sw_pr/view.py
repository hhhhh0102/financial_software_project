class View:

    def __init__(self):
        pass

    @staticmethod
    def err_mesg(sel):
        if sel == 1:
            print("\n잘못 입력하였습니다")
        if sel == 2:
            print("\n가입되지 않은 학번이거나, 잘못된 비밀번호입니다")
        if sel == 3:
            print("\n이미 가입되어있는 학번입니다")
        if sel == 4:
            print("\n잘못된 접근입니다")
        if sel == 5:
            print("\n가입되지 않은 학번입니다")

    @staticmethod
    def show_mesg(sel):
        if sel == 1:
            print("이전화면으로 돌아갑니다")
        elif sel == 2:
            print("초기화면으로 돌아갑니다")
        elif sel == 3:
            print("프로그램을 종료합니다")

    @staticmethod
    def first_menu():
        print("\n--------------메뉴-------------")
        print("| 1. 로그인                    |")
        print("| 2. 회원가입                  |")
        print("| 3. 회원탈퇴                  |")
        print("| 4. 종료                      |")
        print("-------------------------------\n")
        print("메뉴를 선택해주세요")

    @staticmethod
    def req_id_info_menu(sel):
        if sel == 1:
            print("학번을 입력해주세요  ")
        if sel == 2:
            print("비밀번호를 입력해주세요  ")
        if sel == 3:
            print("학년을 입력해주세요  ")

    @staticmethod
    def second_menu(sel, recall=False):

        if not recall:
            if sel == 1:
                print("\n-------------로그인-------------")
            elif sel == 2:
                print("\n------------회원가입------------")
            elif sel == 3:
                print("\n------------회원탈퇴------------")
            elif sel == 4:
                View.show_mesg(3)


        elif recall == 1:
            print("\n-----------------------------------")
            print("|          인증되었습니다          |")
            print("-----------------------------------\n")
        elif recall == 2:
            print("\n-----------------------------------")
            print("|     회원가입이 완료되었습니다    |")
            print("-----------------------------------\n")
            View.show_mesg(2)
        elif recall == 3:
            print("\n-----------------------------------")
            print("|    회원탈퇴가 완료되었습니다    |")
            print("-----------------------------------\n")
            View.show_mesg(2)

    @staticmethod
    def stock_first_menu():
        print("\n---------------메뉴---------------")
        print("| 1. 주식 데이터 파일 받기        |")
        print("| 2. 주식 가격 예측 데이터 받기   |")
        print("| 3. 이전 메뉴로                  |")
        print("----------------------------------\n")
        print("메뉴를 선택해주세요")

    def stock_second_menu(sel, called):
        if sel == 1:
            if called == 1:
                print("\n-----------------------------------------")
                print("해당 주식의 데이터파일을 받겠습니다")
                print("-----------------------------------------\n")
            elif called == 2:
                print("\n------------------------------------------")
                print("데이터파일을 성공적으로 다운 받았습니다")
                print("------------------------------------------\n")
            elif called == 3:
                print("\n--------------------------------")
                print("데이터파일이 이미 존재합니다")
                print("--------------------------------\n")
                View.show_mesg(1)
        elif sel == 2:
            if called == 1:
                print("며칠 간의 데이터를 원하십니까? (예) 30일 <30 입력>")
            elif called == 2:
                print("\n해당 주식 가격의 예측 데이터를 만들겠습니다")
            elif called == 3:
                print("\n해당 주식의 가격 예측을 위한 모델 파일이 없습니다")
                print("\n모델을 만들겠습니다")
            elif called == 4:
                print("\n해당 주식의 데이터 파일이 없습니다")
                print("\n해당 주식의 데이터 파일을 먼저 다운받겠습니다.")
            elif called == 5:
                print("\n예측 데이터를 성공적으로 만들었습니다")

    @staticmethod
    def stock_third_menu():
        print("\n------------------메뉴-------------------")
        print("| 1. 예측 데이터 그래프로 보기           |")
        print("| 2. 예측 데이터 엑셀 파일로 보기        |")
        print("| 3. 기간내 전고점 데이터 보기           |")
        print("| 4. 기간내 전저점 데이터 보기           |")
        print("| 5. 이전 메뉴로 돌아가기                |")
        print("-----------------------------------------\n")
        print("메뉴를 선택해주세요")

    @staticmethod
    def stock_fourth_menu(sel, date, price, idx):
        if sel == 1:
            print("\n-------------------------------------------------------------")
            print("+%d 거래일간 전고점은 +%d 거래일로 가격은 %d 입니다" % (date, idx + 1, price))
            print("-------------------------------------------------------------\n")
        if sel == 2:
            print("\n-------------------------------------------------------------")
            print("+%d 거래일간 전저점은 +%d 거래일로 가격은 %d 입니다" % (date, idx + 1, price))
            print("-------------------------------------------------------------\n")

    @staticmethod
    def show_code_states(sel, codes=None, grade=False):
        if codes is None:
            codes = []
        if sel == 1:
            print("\n등록된 주식 종목이 없습니다")
            print("\n주식코드를 추가하겠습니다")

        else:
            print("\n------------------------------------------------------------------------------------")
            print("|                           등록된 주식 종목은 %d개입니다                           |" % (len(codes)))
            if sel == 2:
                print("------------------------------------------------------------------------------------")
                print("|                  %d개의 주식 종목을 추가로 등록할 수 있습니다                     |" % (grade - len(codes)))
                print("------------------------------------------------------------------------------------")
                print("| 주식 코드를 선택해 주세요 (1 ~ %d), 주식코드를 추가로 등록하려면 0을 입력해주세요 |"
                      % (len(codes)))
            elif sel == 3:
                print("------------------------------------------------------------------------------------")
                print("|                        주식 코드를 선택해 주세요 (1 ~ %d)                         |" % (len(codes)))
                print("------------------------------------------------------------------------------------")
            for num in list(range(len(codes))):
                print("| %d번 째 주식코드 : %s" % (num + 1, codes[num]))
            print("------------------------------------------------------------------------------------")

    @staticmethod
    def insert_code_menu(called):
        if called == 1:
            print("시장을 선택해주세요")
            print("1.코스피, 2.미국 주식")
        if called == 2:
            print("주식 코드를 입력해주세요")

    @staticmethod
    def master_menu(sel, called, data_set=False):
        if called == 1:
            if sel == 1:
                print("관리자 계정으로 로그인 되었습니다")
            elif sel == 2:
                print("\n-----------------관리자 메뉴-----------------")
                print("| 1. 회원정보 열람                           |")
                print("| 2. 회원 삭제                               |")
                print("| 3. 회원 정보 변경                          |")
                print("| 4. 서비스 이용                             |")
                print("| 5. 이전 메뉴로                             |")
                print("---------------------------------------------\n")

                print("\n 메뉴를 선택해주세요")
        if called == 2:
            if sel == 1:
                print("회원 데이터를 출력하겠습니다")
            elif sel == 2:
                print("\n----------------------------------------------")
                print("             회원 삭제메뉴입니다")
                print("----------------------------------------------\n")
                print("\n삭제할 회원의 학번을 입력해주세요")
            elif sel == 3:
                print("\n----------------------------------------------")
                print("           회원 정보 변경 메뉴입니다")
                print("----------------------------------------------\n")
                print("\n정보를 변경할 회원의 학번을 입력해주세요")
            elif sel == 4:
                View.show_mesg(1)

        if called == 3:
            if sel == 1:
                data_set = list(data_set)
                data_set.insert(0, ("id", "password", "grade", "master authority"))
                for data in data_set:
                    for val in data:
                        if val is not str:
                            val = str(val)
                        print(val.rjust(20), end='\t')
                    print()
            elif sel == 2:
                print("\n----------------------------------------------")
                print("          회원 삭제가 완료되었습니다")
                print("----------------------------------------------\n")

            elif sel == 3:
                print("\n----------------------------------------------")
                print("| 어떤 정보를 변경하시겠습니까?               |")
                print("|---------------------------------------------|")
                print("| 1. 학년 정보                                |")
                print("| 2. 권한 정보                                |")
                print("----------------------------------------------\n")

        if called == 4:
            if sel == 1:
                print("학년 정보를 새로 입력해주세요")
            elif sel == 2:
                print("해당 회원의 학년 정보가 변경되었습니다")
            elif sel == 3:
                print("해당 회원은 관리자 권한을 얻었습니다")
            elif sel == 4:
                print("해당 회원의 관리자 권한이 회수되었습니다")