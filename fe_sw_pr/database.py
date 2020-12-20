import pymysql


class Db:

    def __init__(self):
        self.authority = False
        self.id = ""
        self.host = "localhost"
        self.user = "root"
        self.password = "root"
        self.db = "main_db"
        self.master_ath = False

    def connect(self):  # 데이터베이스 연걸
        conn = pymysql.connect(host=self.host, user=self.user,
                               password=self.password, db=self.db)
        curs = conn.cursor()
        return conn, curs

    # 회원 등록 DB 반영
    def register(self, user_id, password, grade):

        conn, curs = self.connect()  # DB에 연결

        sql = "SELECT id FROM user"
        curs.execute(sql)
        rows = curs.fetchall()
        for row in rows:
            if row[0] == user_id:
                conn.close()
                return False

        sql = "insert into `main_db`.`user` (id, password, grade) values (%s, %s, %s)"  # 회원 정보 삽입

        curs.execute(sql, (user_id, password, grade))
        conn.commit()  # 트랜잭션 반영

        conn.close()
        return True

    def user_chk(self, user_id, password):  # 회원 정보 확인
        conn, curs = self.connect()

        sql = "select password from user where id=%s"
        curs.execute(sql, user_id)
        val = curs.fetchone()
        if val is None:
            conn.close()
            return False
        val = val[0]

        if password == val:  # 회원이 맞는 경우
            self.authority = True
            self.id = user_id
            conn.close()
            return True

        else:  # 회원이 아닌 경우
            conn.close()
            return False

    def user_del(self, user_id, password=""):  # 회원 탈퇴
        if self.master_ath is not True and password == "":
            return False
        conn, curs = self.connect()  # DB 연결
        sql = "select * from user"
        curs.execute(sql)
        rows = curs.fetchall()

        if rows is None:  # 회원정보가 하나도 입력이 안되어있는 경우 회원 탈퇴 불가능
            conn.close()
            return False

        for row in rows:
            idVal = row[0]
            passwordVal = row[1]

            if user_id == idVal:
                if self.master_ath:
                    sql = "DELETE FROM user WHERE id = %s"
                    curs.execute(sql, user_id)
                    conn.commit()
                    conn.close()
                    return True
                elif password == passwordVal:
                    sql = "delete from user where id=%s AND password=%s"  # DB에 회원 정보 삭제
                    curs.execute(sql, (user_id, password))
                    conn.commit()  # 트랜잭션 반영
                    conn.close()
                    return True
        conn.close()
        return False    # 입력 받은 정보가 올바르지 않은 경우 삭제 불가능

    def insert_code(self, code):  # 주식 코드 삽입
        conn, curs = self.connect()
        sql = "insert into `main_db`.`order` (user_id, stock_code) values (%s, %s)"
        curs.execute(sql, (self.id, code))
        conn.commit()
        conn.close()

    def get_code(self):  # DB 상 회원에게 등록된 주식 코드 얻어오기
        conn, curs = self.connect()
        sql = "SELECT stock_code FROM main_db.order WHERE user_id = %s"
        curs.execute(sql, self.id)
        rows = curs.fetchall()
        codes = []
        if rows is None:  # 등록된 코드가 없는 경우
            return codes

        for row in rows:  # 등록된 코드 리스트에 추가
            codes.append(row[0])
        conn.close()

        return codes  # 등록된 코드 정보 반환

    def get_grade(self):  # 회원의 학년 정보 가져오기
        conn, curs = self.connect()
        sql = "SELECT grade FROM user WHERE id = %s"
        curs.execute(sql, self.id)
        grade = curs.fetchone()
        grade = grade[0]
        return grade

    def master_chk(self):
        conn, curs = self.connect()
        if self.authority:
            sql = "SELECT master_account FROM user WHERE id = %s"
            curs.execute(sql, self.id)
            is_master = curs.fetchone()
            is_master = is_master[0]

            if is_master is None or is_master == 0:
                return False
            else:
                self.master_ath = True
                return True

    def get_member_info(self):
        conn, curs = self.connect()
        sql = "SELECT * FROM user"
        curs.execute(sql)
        data_set = curs.fetchall()
        conn.close()
        return data_set

    def update_info(self, sel, user_id, new_val=""):
        conn, curs = self.connect()

        sql = "SELECT id FROM user"
        curs.execute(sql)
        rows = curs.fetchall()
        for row in rows:
            if user_id == row[0]:
                if sel == 1:
                    sql = "UPDATE USER SET grade = %s WHERE id = %s"
                    curs.execute(sql, (new_val, user_id))
                    flag = 0
                elif sel == 2:
                    sql = "SELECT master_account FROM user WHERE id = %s"
                    curs.execute(sql, user_id)
                    row = curs.fetchone()
                    if row[0] == 1:
                        new_master_account = 0
                        flag = -1
                    else:
                        new_master_account = 1
                        flag = 1
                    sql = "UPDATE USER SET master_account = %s WHERE id = %s"
                    curs.execute(sql, (new_master_account, user_id))
                conn.commit()
                conn.close()
                return flag
        return False
