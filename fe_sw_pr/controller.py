from view import View as vw
from database import Db
from model import Stock


class Controller:
    stock = None

    def __init__(self):
        self.db = Db()

    # 사용자에게 숫자만을 받는 함수
    def get_num(self):
        while True:
            try:
                num = int(input())
                return num
            except:
                vw.err_mesg(1)

    # 사용자에게 valid한 input을 받아오는 함수
    def get_valid_input(self, start_num, end_num):
        while True:
            sel_num = self.get_num()
            if start_num <= sel_num <= end_num:
                return sel_num
            else:
                vw.err_mesg(1)

    def req_id_info(self, grade_chk=False):  # 회원 정보 확인
        vw.req_id_info_menu(1)
        user_id = self.get_valid_input(190000000,202100000)

        vw.req_id_info_menu(2)
        password = input()  # password 입력받기

        if grade_chk:
            vw.req_id_info_menu(3)
            grade = self.get_valid_input(1, 6)

            return user_id, password, grade

        return user_id, password

    def init_menu_control(self):  # 초기 메뉴 제어

        vw.first_menu()  # 초기 메뉴 화면 표시

        sel = self.get_valid_input(1, 4)

        vw.second_menu(sel)

        if sel == 1:  # 로그인 기능 선택
            user_id, password = self.req_id_info()  # 회원 정보 입력 받기
            user_chk = self.db.user_chk(user_id, password)  # 회원 정보 확인
            if user_chk is False:  # 가입 되지 않은 회원 메시지 알림
                vw.err_mesg(2)
                vw.show_mesg(1)
                return 0
            master_chk = self.db.master_chk()
            if master_chk is False:
                vw.second_menu(sel, recall=1)  # 로그인 성공 메시지 알림
                return 1
            else:
                vw.master_menu(1, 1)
                return 100
        elif sel == 2:  # 회원가입 기능 선택
            user_id, password, grade = self.req_id_info(grade_chk=True)  # 회원 정보 입력 받기
            reg_chk = self.db.register(user_id, password, grade)  # 회원 가입 db 반영
            if reg_chk is False:  # 이미 가입된 학번이라는 메시지 표시
                vw.err_mesg(3)
                vw.show_mesg(2)
                return 0
            vw.second_menu(sel, recall=2)  # 회원 가입 완료 메시지 알림
            return 0
        elif sel == 3:  # 회원탈퇴 기능 선택
            user_id, password = self.req_id_info()  # 회원 정보 입력 받기
            del_chk = self.db.user_del(user_id, password)  # 회원 정보 확인
            if del_chk is False:  # 잘못된 회원정보 메시지 알림
                vw.err_mesg(2)
                vw.show_mesg(1)
                return 0
            vw.second_menu(sel, recall=3)  # 회원 탈퇴 완료 메시지 알림
            return 0
        elif sel == 4:  # 이전메뉴로 기능 선택
            return -1

    def stock_menu_control(self):  # 주식 메뉴 제어
        if self.db.authority != 1:  # 인가되지 않은 사용자의 기능 접근에 대한 차단
            vw.err_mesg(4)
            vw.show_mesg(3)
            exit()

        vw.stock_first_menu()   # 주식 첫 번째 메뉴 표시
        sel = self.get_valid_input(1, 3)

        if sel == 3:  # 이전메뉴로 기능 선택
            vw.show_mesg(1)
            return -1

        else:  # 이전 메뉴로 가지 않음
            codes = self.db.get_code()  # 주식 메뉴의 기능을 사용하기 위해 등록된 주식 코드와 학년 정보를 받아옴
            grade = self.db.get_grade()

            # 메뉴 실행 전 주식코드 설정
            if len(codes) == 0:  # 주식코드가 지정되어 있지 않은 경우
                vw.show_code_states(1)
                ssel = 0
            elif grade > len(codes):  # 주식코드를 더 지정할 수 있는 경우
                vw.show_code_states(2, codes, grade)
                ssel = self.get_valid_input(0, len(codes))

            else:  # 주식코드를 더 지정할 수 없는 경우
                vw.show_code_states(3, codes, grade)
                ssel = self.get_valid_input(0, len(codes))

            if ssel == 0:  # 주식코드를 새로 지정한다
                vw.insert_code_menu(called=1)
                market = self.get_valid_input(1, 2)
                vw.insert_code_menu(called=2)
                target_code = input()  # 코드 입력 받기
                if market == 1:  # 코드 포맷에 맞추기
                    target_code += ".KS"
                self.db.insert_code(target_code)  # 새로 지정한 주식 코드 DB에 반영
            else:  # 기존에 지정한 주식을 선택하는 경우
                target_code = codes[ssel - 1]  # 하나의 주식 코드를 지정한다

            self.stock = Stock(self.db.id, target_code)  # stock 모듈의 Stock 클래스의 기능을 사용하기 위해 객체 생성

            if sel == 1:  # 주식 데이터 파일 받는 기능 선택
                vw.stock_second_menu(1, 1)  # 해당 기능 선택에 대한 알림
                exist_chk = self.stock.get_stock_data()
                if exist_chk == -1:  # 이미 데이터 파일이 존재한 경우
                    vw.stock_second_menu(1, 3)  # 데이터가 존재하다고 알림
                    return 0
                vw.stock_second_menu(1, 2)  # 데이터 다운 완료 알림
                vw.show_mesg(1)
                return 0

            elif sel == 2:  # 예측 데이터 파일 받기 기능 선택
                vw.stock_second_menu(2, 1)
                date = self.get_num()  # 예측 기간 설정
                try:
                    vw.stock_second_menu(2, 2)  # 예측 데이터 파일을 받는다
                    self.stock.get_prices(date)
                except:  # 예측 데이터를 받기 위한 AI 모델이 만들어지지 않은 경우
                    try:
                        vw.stock_second_menu(2, 3)  # AI 모델이 없다 알림
                        self.stock.make_model()  # AI 모델을 만든다

                    except:  # 위의 AI 모델을 만들기 위한 주식데이터가 없는 경우
                        vw.stock_second_menu(2, 4)  # 주식 데이터가 없다 알림
                        self.stock.get_stock_data()  # 주식 데이터를 받아온다
                        self.stock.make_model()  # 받아온 주식 데이터로 AI 모델을 만든다

                    finally:  # 만들어진 AI 모델로 예측 데이터를 생성한다
                        vw.stock_second_menu(2, 2)
                        self.stock.get_prices(date)
            vw.stock_second_menu(2, 5)  # 예측 데이터가 생성되었다 알림
            return 1

    # 주식 예측 가격 메뉴 함수 제어
    def predicts_menu_control(self):
        vw.stock_third_menu()
        sel = self.get_num()
        if sel == 1:
            self.stock.show_plot()
        elif sel == 2:
            self.stock.show_csv_file()
        elif sel == 3:
            max_price, idx = self.stock.get_minmax_price(1)
            vw.stock_fourth_menu(1, self.stock.date, max_price, idx)
        elif sel == 4:
            min_price, idx = self.stock.get_minmax_price(2)
            vw.stock_fourth_menu(2, self.stock.date, min_price, idx)
        elif sel == 5:
            vw.show_mesg(1)
            return -1
        vw.show_mesg(1)
        return 0

    # 관리자 계정 메뉴 제어
    def master_menu_control(self):
        if self.db.master_ath is False:
            vw.err_mesg(4)
            exit()
        else:
            vw.master_menu(2, 1)
            sel = self.get_valid_input(1, 5)

            if sel == 1:
                vw.master_menu(1, 2)
                data_set = self.db.get_member_info()
                vw.master_menu(1, 3, data_set)
                return 0
            elif sel == 2:
                vw.master_menu(2, 2)
                req_id = self.get_num()
                del_chk = self.db.user_del(req_id)
                if del_chk:
                    vw.master_menu(2, 3)
                    return 0
                else:
                    vw.err_mesg(5)
                    return 0

            elif sel == 3:
                global upd_chk
                vw.master_menu(3, 2)
                req_id = self.get_num()
                vw.master_menu(3, 3)
                req_func = self.get_valid_input(1, 2)
                if req_func == 1:
                    vw.master_menu(1, 4)
                    req_grade = self.get_valid_input(1, 6)
                    upd_chk = self.db.update_info(req_func, req_id, req_grade)
                elif req_func == 2:
                    upd_chk = self.db.update_info(req_func, req_id)
                if upd_chk is False:
                    vw.err_mesg(5)
                elif upd_chk == 0:
                    vw.master_menu(2, 4)
                elif upd_chk == 1:
                    vw.master_menu(3, 4)
                elif upd_chk == -1:
                    vw.master_menu(4, 4)
                return 0

            elif sel == 4:
                return 1

            elif sel == 5:
                return -100
