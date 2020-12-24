import pandas as pd


class preprocess:

    def __init__(self):
        self.targets = []
        self.sentences = []
        self.label_dict = dict()
        self.index_to_ner = dict()

    def preprocessing(self):
        # dataset 불러오기
        train = pd.read_csv("train_data", names=['src', 'tar'], sep="\t")
        train = train.reset_index()
        train['src'] = train['src'].str.replace("．", ".", regex=False)
        train.loc[train['src'] == '.']

        # 한글, 영어 이외의 단어 모두 제거
        train['src'] = train['src'].astype(str)
        train['tar'] = train['tar'].astype(str)

        train['src'] = train['src'].str.replace(r'[^ㄱ-ㅣ가-힣0-9a-zA-Z.]+', "", regex=True)

        # 데이터 리스트 형태로 변환
        data = [list(x) for x in train[['index', 'src', 'tar']].to_numpy()]

        # 라벨 추출 후 딕셔너리 형태로 변환
        label = train['tar'].unique().tolist()
        self.label_dict = {word: i for i, word in enumerate(label)}
        self.label_dict.update({"[PAD]": len(self.label_dict)})
        self.index_to_ner = {i: j for j, i in self.label_dict.items()}

        # 데이터를 문장과 개체들로 변환
        tups = []
        temp_tup = [data[0][1:]]
        for i, j, k in data:
            if i != 1:
                temp_tup.append([j, self.label_dict[k]])
            if i == 1:
                if len(temp_tup) != 0:
                    tups.append(temp_tup)
                    temp_tup = [[j, self.label_dict[k]]]
        tups.pop()

        # 단어끼리 개체끼리 분류해줍니다
        for tup in tups:
            sentence = []
            target = []
            sentence.append("[CLS]")
            target.append(self.label_dict['-'])
            for i, j in tup:
                sentence.append(i)
                target.append(j)
            sentence.append("[SEP]")
            target.append(self.label_dict['-'])
            self.sentences.append(sentence)
            self.targets.append(target)

        del(self.sentences[0])
        del(self.targets[0])
