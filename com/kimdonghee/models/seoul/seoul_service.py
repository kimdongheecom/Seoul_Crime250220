
import os
import pandas as pd

from com.kimdonghee.models.seoul.data_reader import DataReader
from com.kimdonghee.models.seoul.dataset import Dataset
from com.kimdonghee.models.seoul.key_retriever_singleton import KeyRetrieverSingleton


class SeoulService:

    dataset = Dataset()   #Dataset()을 dataset이라고 이 안에서 부르겠다는 의미이다.
    reader = DataReader()

    def new_model(self,fname) -> object: #self는 자기 데이터를 가지고 오겠다라는 의미. #new_model은 모델을 만드는 것을 의미함. fname이라는 파일명을 받고 object에 결과를 찍겠다
        reader = self.reader #self가 붙으면 property인 것을 알수 있다. 그리고 self.dataset을 this라고 설정하였다.
        print(f"😎🥇🐰컨텍스트 경로 : {reader.context}")
        print(f"😎🥇🐰파일명 : {fname}")
        reader.fname = fname
        if fname.endswith('csv'):
            return reader.csv_to_dframe()
        elif fname.endswith('xls'):
            return reader.xls_to_dframe(header = 2, usecols = 'B,D,G,J,N')

    # def csv_model(self,fname) -> object: #self는 자기 데이터를 가지고 오겠다라는 의미. #new_model은 모델을 만드는 것을 의미함. fname이라는 파일명을 받고 object에 결과를 찍겠다
    #     reader = self.reader #self가 붙으면 property인 것을 알수 있다. 그리고 self.dataset을 this라고 설정하였다.
    #     print(f"😎🥇🐰컨텍스트 경로 : {reader.context}")
    #     print(f"😎🥇🐰파일명 : {fname}")
    #     reader.fname = fname
    #     return reader.csv_to_dframe()
    
    # def xls_model(self, fname) -> object:
    #     reader = self.reader
    #     print(f"😎🥇🐰컨텍스트 경로 : {reader.context}")
    #     print(f"😎🥇🐰파일명 : {fname}")
    #     reader.fname = fname
    #     return reader.xls_to_dframe(header = 2, usecols = 'B,D,G,J,N')
    
    
    def preprocess(self, *args) -> object:
        print("---------모델 전처리 시작 ----------")
        temp = []
        for i in list(args): #args를 풀기 위해 temp를 만들었다. temp를 옮겨 담기 위해 포문을 돌렸다.
            print(f"args 값 출력: {i}")
            temp.append(i)
        # feature = ['Public','Subtotal','Before_2013y','2014y','2015y','2016y']

        this = self.dataset
        this.cctv = self.new_model(temp[0])
        print("🎍🎁CCTV 데이터")
        print(this.cctv)
        this = self.cctv_ratio(this)
        this.crime = self.new_model(temp[1])
        print("🤬😈Crime 데이터")
        print(this.crime)
        # this = self.crime_ratio(this)
        this.pop = self.new_model(temp[2])
        print("😋😊Pop 데이터")
        print(this.pop)
        this = self.pop_ratio(this)
        return this
    
    @staticmethod
    def cctv_ratio(this) -> object:
        cctv = this.cctv
        print("🚥🚦", this.cctv)
        cctv = this.cctv.drop(['2013년도 이전','2014년', '2015년', '2016년'],axis = 1)
        print("🌋🗻")
        null_counts = this.cctv.isnull().sum()
        print("🎈🎃🎆cctv 널 값 개수", this.cctv.head()) #head는 위에서 5개를 뽑은 것.
        print("🎈🎃🎆cctv 널 값 개수",null_counts)

        return this
    
    
    @staticmethod
    def crime_ratio(this) -> object:
        crime = this.crime
        station_names = [] #경찰서 관서명 리스트
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1]) +'경찰서')
        print("👮‍♂️👮‍♀️🕵️‍♀️경찰서 관서명 리스트", station_names)
        station_addrs = [] #api관련하여 작성하였다.
        station_lats = []
        station_lngs = []

        singleton1 = KeyRetrieverSingleton()
        singleton2 = KeyRetrieverSingleton()

        print("👩‍🦰👨‍🦰API Key:", singleton1.get_api_key())  # "my-secret-api-key"
        print("👩‍🔧👨‍🔧singleton1 is singleton2:", singleton1 is singleton2)  # True (같은 객체)

        gmaps = DataReader.create_gmaps()
        for name in station_names:
            tmp = gmaps.geocode(name, language = 'ko')
            print(f"""{name}의 검색 결과:, {tmp[0].get("formatted_address")}""" ) #딕셔너리에 담아져 있기 때문에 프린터를 딕셔너리에 담아져 있다. 
            station_addrs.append(tmp[0].get("formatted_address"))
            tmp_loc = tmp[0].get("geometry")
            station_lats.append(tmp_loc['location']['lat'])
            station_lats.append(tmp_loc['location']['lng'])
        print(f"🚈🚅자치구 리스트:, {station_addrs}")
        gu_names = []
        for addr in station_addrs:
            tmp = addr.split()
            tmp_gu = [gu for gu in tmp if gu[-1] == '구'][0]
            gu_names.append(tmp_gu)
        [print(f"자치구 리스트 2: {gu_names}")]
        crime['자치구'] = gu_names
        #저장할 디렉토리 경로 설정
        save_dir = "C:\\Users\\bitcamp\\Documents\\kimdonghee250220\\com\\kimdonghee\\saved_data\\"
        # 폴더가 없으면 생성
        if not os.path.exists(save_dir):
           os.makedirs(save_dir)
        
        # CSV 파일 저장
        crime['자치구'] = gu_names
        crime.to_csv(os.path.join(save_dir, "police_position.csv"), index=False) #내가 있는 위치에서 position_police에 대한 데이터를 saved_data에 올려줘.....올릴 때는 점 두개 쓰고 /를 쓴다.


        null_counts = this.crime.isnull().sum()
        print("🎈🎃🎆cctv 널 값 개수", this.cctv.head())
        print("🛩⛵👨‍🦳crime 널 값 개수",null_counts)

        return this
    
    
    @staticmethod
    def pop_ratio(this) -> object:
        pop = this.pop
        pop.rename(columns = {
            pop.columns[1]: '인구수',
            pop.columns[2]: '한국인',
            pop.columns[3]: '외국인',
            pop.columns[4]: '고령자',}, inplace = True)
        null_counts = this.pop.isnull().sum()
        print("🎈🎃🎆cctv 널 값 개수", this.cctv.head())
        print("🕶👓👸pop 널 값 개수",null_counts)
        return this
 




        # this.id = this.test['PassengerId'] #테스트는 중간고사, 기말고사이고, 트레인은 매일 쪽지 시험 느낌////
        # #'SibSp', 'parch'. 'Cabin', 'Ticket'가 지워야 할 feature 이다.
        # this.label = this.train['Survived']
        # this.train = this.train.drop('Survived', axis = 1)
        # drop_features = ['SibSp', 'Parch', 'Cabin', 'Ticket']
        # this = self.extract_title_from_name(this)
        # title_mapping = self.remove_duplicate_title(this)
        # this = self.title_nominal(this, title_mapping)
        # this = self.drop_feature(this,'Name')
        # this = self.gender_nominal(this)
        # this = self.drop_feature(this,'Sex')
        # this = self.embarked_norminal(this)  
        # # self.df_info(this)
        # this = self.age_ratio(this)
        # this = self.drop_feature(this,'Age')
        # this = self.pclass_ordnal(this)
        # this = self.fare_ordinal(this)
        # this = self.drop_feature(this,"Fare")