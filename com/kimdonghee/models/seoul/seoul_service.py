
import os
import pandas as pd

from com.kimdonghee.models.seoul.data_reader import DataReader
from com.kimdonghee.models.seoul.dataset import Dataset

from com.kimdonghee.models.seoul import save_dir
from com.kimdonghee.models.seoul.google_map_singleton import GoogleMapSingleton


class SeoulService:

    dataset = Dataset()   #Dataset()을 dataset이라고 이 안에서 부르겠다는 의미이다.
    reader = DataReader()
    # csv 파일 저장
    # 현재 스크립트의 절대 경로 가져오기
    # 저장할 디렉토리 설정(스크립트 위치 기준)

    def preprocess(self, *args) -> object:
        print("---------모델 전처리 시작 ----------")
        this = self.dataset
        for i in list(args):
            # print(f"args 값 출력: {i}")
            self.save_object_to_csv(this,i)

        return this
    
    def create_matrix(self,fname) -> object: #self는 자기 데이터를 가지고 오겠다라는 의미. #new_model은 모델을 만드는 것을 의미함. fname이라는 파일명을 받고 object는 타입을 의미함.
        reader = self.reader #self가 붙으면 property인 것을 알수 있다. 그리고 self.dataset을 this라고 설정하였다.
        print(f"😎🥇🐰컨텍스트 경로 : {reader.context}")
        print(f"😎🥇🐰파일명 : {fname}")
        reader.fname = fname
        if fname.endswith('csv'):
            return reader.csv_to_dframe()
        elif fname.endswith('xls'):
            return reader.xls_to_dframe(header = 2, usecols = 'B,D,G,J,N')

    def save_object_to_csv(self, this, fname) -> object:

        print(f"🍟🧈🥙save_csv 실행: {fname}")
        # file_path = os.path.join(save_dir, fname)

        full_name = os.path.join(save_dir, fname)

        if not os.path.exists(full_name) and fname == "cctv_in_seoul.csv":
            print(f"*"*20, "🔰1. cctv 편집")
            print(f"🍤🦪🍛1-cctv_in_seoul. {fname}")
            this.cctv = self.create_matrix(fname)
            this = self.update_cctv(this)
            this.cctv.to_csv(full_name, index = False)
        
        elif not os.path.exists(full_name) and fname == "crime_in_seoul.csv":
             print(f"*"*20, "🔰2. crime 편집")
             print(f"🍤🦪🍛2-crime_in_seoul. {fname}")
             this.crime = self.create_matrix(fname)
             this = self.update_crime(this)
             this.crime.to_csv(full_name, index = False)
        
        elif not os.path.exists(full_name) and fname == "pop_in_seoul.xls":
             print(f"*"*20, "🔰3. pop 편집")
             print(f"🍚🍙🍘3- pop_in_seoul. {fname}")
             this.pop = self.create_matrix(fname)
             this = self.update_pop(this)
             this.pop.to_csv(os.path.join(save_dir,"pop_in_seoul.csv"), index = False) #save_dir 경로에 "pop_in_seoul.csv" 파일을 저장할 경로를 생성.

        
        else:
            print(f"파일이 이미 존재합니다.{fname}")
        
        return this


    
    @staticmethod
    def update_cctv(this) -> object:
        print("cctv 데이터 헤드", this.cctv.head())
        print("🚥🚦", this.cctv)
        this.cctv = this.cctv.drop(['2013년도 이전','2014년', '2015년', '2016년'], axis = 1)
        cctv = this.cctv
        cctv = this.cctv.rename(columns={"기관명": "자치구"})
        cctv.to_csv(os.path.join(save_dir, "cctv_in_seoul.csv"), index=False) #내가 있는 위치에서 position_police에 대한 데이터를 saved_data에 올려줘.....올릴 때는 점 두개 쓰고 /를 쓴다.
        this.cctv = cctv
        print("🌋🗻기관명을 자치구로 변경")
        print(cctv)
        return this
    
        #  #저장할 디렉토리 경로 설정
        # save_dir = "C:\\Users\\bitcamp\\Documents\\kimdonghee250220\\com\\kimdonghee\\saved_data\\"
        # # 폴더가 없으면 생성
        # if not os.path.exists(save_dir):
        #    os.makedirs(save_dir)
    
    
    @staticmethod
    def update_crime(this) -> object:
        print("crime 데이터 헤드", this.crime.head())
        crime = this.crime
        station_names = [] #경찰서 관서명 리스트
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1]) +'경찰서')
        print("👮‍♂️👮‍♀️🕵️‍♀️경찰서 관서명 리스트", station_names)
        station_addrs = [] #api관련하여 작성하였다.
        station_lats = [] #lat은 위도
        station_lngs = [] #lng은 경도

        gmaps1 =  GoogleMapSingleton()
        gmaps2 =  GoogleMapSingleton()
        if gmaps1 is gmaps2:
            print("동일한 객체이다.")
        else:
            print("다른 객체 입니다.")
        gmaps = GoogleMapSingleton()
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
        # #저장할 디렉토리 경로 설정

        # CSV 파일 저장
        crime.to_csv(os.path.join(save_dir, "crime_in_seoul.csv"), index=False) #내가 있는 위치에서 position_police에 대한 데이터를 saved_data에 올려줘.....올릴 때는 점 두개 쓰고 /를 쓴다.
        this.crime = crime
        return this

        # crime_position_path = os.path.join(save_dir, 'crime_position.csv')
        # if not os.path.exists(crime_position_path):
        #    print("🚨 👩‍🏫👩‍🏫👨‍🎓👨‍🎓김동희 1")
        #    gmaps = DataReader.create_gmaps()
        # else:
        #    print("👩‍🏫👩‍🏫👨‍🎓👨‍🎓김동희 2")
       
       
    @staticmethod
    def update_pop(this) -> object:
        pop = this.pop
        pop.rename(columns = {
            pop.columns[1]: '인구수',
            pop.columns[2]: '한국인',
            pop.columns[3]: '외국인',
            pop.columns[4]: '고령자',}, inplace = True)
        print("🥽데이터 헤드", this.pop.head())
        pop.to_csv(os.path.join(save_dir, "pop_in_seoul.csv"), index=False) #내가 있는 위치에서 position_police에 대한 데이터를 saved_data에 올려줘.....올릴 때는 점 두개 쓰고 /를 쓴다.
        this.pop = pop
        return this