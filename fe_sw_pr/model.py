import getpass
import os
import shutil
import time

import numpy as np
import pandas as pd
import tensorflow.keras.models as md
from matplotlib import pyplot as plt
from selenium import webdriver
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential


class Stock:

    def __init__(self, user_id, target_code, date=False):
        self.username = getpass.getuser()   # 사용자 윈도우 계정명 할당
        self.user_id = user_id
        self.target_code = target_code
        self.date = date
        self.path = 'C:\\Users\\' + self.username + '\\Downloads\\stock_data\\' + str(self.user_id)  # 파일들 기본 경로 설정
        self.downloads_path = self.path + "\\downloads"  # 다운 받아오는 파일 경로 설정
        self.models_path = self.path + "\\models"  # AI 모델 경로 설정
        self.predicts_path = self.path + "\\predicts"  # 예측 데이터파일 경로 설정

    def chk_dir(self):
        if os.path.isdir(self.path) is False:  # 기본 경로로 설정한 폴더 생성
            os.mkdir(self.path)

        if os.path.isdir(self.downloads_path) is False:  # 다운로드 파일 폴더 생성
            os.mkdir(self.downloads_path)

        if os.path.isdir(self.models_path) is False:  # AI 모델 폴더 생성
            os.mkdir(self.models_path)

        if os.path.isdir(self.predicts_path) is False:  # 예측 데이터파일 폴더 생성
            os.mkdir(self.predicts_path)

    def get_stock_data(self):   # 주식 데이터 파일 받아오기

        self.chk_dir()

        if os.path.isfile(self.downloads_path + "\\" + self.target_code + ".csv"):  # 주식 데이터 파일이 이미 있는 경우 기능 종료
            return -1

        # webdriver 객체 생성 및 설정

        options = webdriver.ChromeOptions()
        options.add_argument("window-size=1920x1080")
        options.add_argument("disable-gpu")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")

        prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2,
                                                            'plugins': 2, 'popups': 2,
                                                            'geolocation': 2, 'notifications': 2,
                                                            'auto_select_certificate': 2,
                                                            'fullscreen': 2,'mouselock': 2,
                                                            'mixed_script': 2, 'media_stream': 2,
                                                            'media_stream_mic': 2, 'media_stream_camera': 2,
                                                            'protocol_handlers': 2, 'ppapi_broker': 2,
                                                            'automatic_downloads': 2, 'midi_sysex': 2,
                                                            'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                            'metro_switch_to_desktop': 2,'protected_media_identifier': 2,
                                                            'app_banner': 2,'site_engagement': 2,
                                                            'durable_storage': 2}}
        options.add_experimental_option('prefs', prefs)

        driver = webdriver.Chrome("chromedriver.exe.", options=options)

        # target URL 설정
        url1 = "https://finance.yahoo.com/quote/"
        url2 = "/history?p="
        targetURL = url1 + self.target_code + url2 + self.target_code

        # 크롤링을 수행한다
        driver.get(targetURL)

        time.sleep(30)
        driver.find_element_by_xpath(
                '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div').click()
        time.sleep(15)
        driver.find_element_by_xpath('//*[@id="dropdown-menu"]/div/ul[2]/li[3]/button').click()
        time.sleep(15)
        driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button').click()
        time.sleep(20)

        driver.find_element_by_xpath(
            '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a').click()
        time.sleep(1)

        driver.quit()

        # 다운받은 파일을 지정된 경로로 옮긴다
        shutil.move(self.path[:-20] + self.target_code + '.csv', self.path + "\\downloads")

    def make_model(self):   # AI 모델 만들기, https://github.com/kairess/stock_crypto_price_prediction 참조

        self.chk_dir()

        # 모델을 만들기 위한 데이터 파일을 불러온다 (저희가 소스코드에 추가한 부분입니다.)
        data = pd.read_csv(self.downloads_path + "\\" + self.target_code + '.csv')
        data.head()

        high_prices = data['High'].values
        low_prices = data['Low'].values
        mid_prices = (high_prices + low_prices) / 2 # 중간 값 데이터를 할당한다

        # 결측값을 제거한다
        for idx in list(range(len(mid_prices))):
            if str(mid_prices[idx]) == "nan":
                mid_prices[idx] = mid_prices[idx - 1]

        # 윈도우 사이즈를 설정한다
        seq_len = 50
        sequence_length = seq_len + 1

        # 데이터를 윈도우 사이즈에 맞게 포맷팅한다
        result = []
        for index in range(len(mid_prices) - sequence_length):
            result.append(mid_prices[index: index + sequence_length])

        # 포맷팅된 데이터를 정규화 해준다
        normalized_data = []
        for window in result:
            normalized_window = [((float(p) / float(window[0])) - 1) for p in window]
            normalized_data.append(normalized_window)

        result = np.array(normalized_data)

        # 학습 데이터, 검증 데이터 지정한다
        row = int(round(result.shape[0] * 0.9))
        train = result[:row, :]
        np.random.shuffle(train)

        x_train = train[:, :-1]
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        y_train = train[:, -1]

        # 테스트용 데이터를 지정한다
        x_test = result[row:, :-1]
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        y_test = result[row:, -1]

        # 모델 구축
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(50, 1)))
        model.add(LSTM(64, return_sequences=False))
        model.add(Dense(1, activation='linear'))
        
        #모델 컴파일
        model.compile(loss='mse', optimizer='rmsprop')

        # 모델 학습
        model.fit(x_train, y_train,
                  validation_data=(x_test, y_test),
                  batch_size=10,
                  epochs=20)

        # 모델 저장을 위해 소스코드에서 추가하였습니다.
        if os.path.isdir(self.path + "\\models") is False:
            os.mkdir(self.path + "\\models")

        # 모델 저장
        model.save(self.models_path + "\\model_" + self.target_code + ".h5")

    def get_prices(self, date):     # 주가 예측 데이터 만들기
        self.date = date
        self.chk_dir()

        # AI 모델을 불러온다
        model = md.load_model(self.models_path + "\\model_" + self.target_code + ".h5")

        # 주식 데이터 파일을 불러온다
        data = pd.read_csv(self.downloads_path + "\\" + self.target_code + '.csv')
        data.head()

        high_prices = data['High'].values
        low_prices = data['Low'].values
        mid_prices = (high_prices + low_prices) / 2     # 중간값 데이터를 할당

        for num in list(range(date)):

            mid_prices = mid_prices[-50:]   # -50 거래일 간의 중간값 데이터를 할당
            norm = []

            for price in mid_prices:    # 데이터 정규화
                norm.append(float(price) / float(mid_prices[0]) - 1)

            # 예측 데이터 지정
            norm = np.array(norm)
            norm = np.reshape(norm, (1, norm.shape[0], 1))  # 정규화된 데이터 리포맷
            predict = model.predict(norm)   # 모델을 예측한다

            mid_prices = np.append(mid_prices, (float(predict[0][0]) + 1) * mid_prices[0])

        price_data = {'price': mid_prices[-date:]}

        idx = []
        for num in list(range(date)):
            idx.append("+" + str(num + 1) + "days")
        price_df = pd.DataFrame(price_data, index=idx)
        price_df.to_csv(self.predicts_path + "\\" + self.target_code + "_" + str(date) + ".csv")

    def show_plot(self):
        data = pd.read_csv(self.predicts_path + "\\" + self.target_code + "_" + str(self.date) + ".csv")
        fig = plt.figure(facecolor='white', figsize=(10, 5))
        ax = fig.add_subplot(111)
        prices = data['price'].values
        ax.plot(np.reshape(prices[:], (prices[:].shape[0], 1)), label='Prediction')
        ax.legend()
        plt.show()

    def show_csv_file(self):
        os.system('start excel.exe "%s%s_%s.csv"' % (self.predicts_path + "\\", self.target_code, str(self.date)))

    def get_minmax_price(self, sel):
        data = pd.read_csv(self.predicts_path + "\\" + self.target_code + "_" + str(self.date) + ".csv")
        prices = data['price'].values
        if sel == 1:
            price_max = prices.max()
            max_idx = prices.argmax()
            return price_max, max_idx

        if sel == 2:
            price_min = prices.min()
            min_idx = prices.argmin()
            return price_min, min_idx
