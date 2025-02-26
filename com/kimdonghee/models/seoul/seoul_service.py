
import os
import numpy as np
import pandas as pd
from sklearn import preprocessing

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
     
            this.cctv = self.create_matrix(fname)
            this = self.update_cctv(this)
        
        elif not os.path.exists(full_name) and fname == "crime_in_seoul.csv":
         
             this.crime = self.create_matrix(fname)
             this = self.update_crime(this)
             this = self.update_police(this)

        elif not os.path.exists(full_name) and fname == "pop_in_seoul.xls":
     
             this.pop = self.create_matrix(fname)
             this = self.update_pop(this)
        
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
        
        crime.to_csv(os.path.join(save_dir, 'crime_in_seoul.csv'), index=True)

        # CSV 파일 저장
        # crime.to_csv(os.path.join(save_dir, "crime_in_seoul.csv"), index=False) #내가 있는 위치에서 position_police에 대한 데이터를 saved_data에 올려줘.....올릴 때는 점 두개 쓰고 /를 쓴다.
        # this.crime = crime
        this.crime = crime
        return this

        # crime_position_path = os.path.join(save_dir, 'crime_position.csv')
        # if not os.path.exists(crime_position_path):
        #    print("🚨 👩‍🏫👩‍🏫👨‍🎓👨‍🎓김동희 1")
        #    gmaps = DataReader.create_gmaps()
        # else:
        #    print("👩‍🏫👩‍🏫👨‍🎓👨‍🎓김동희 2")
        
    @staticmethod
    def update_police(this) -> object:
        crime = this.crime
        crime = crime.groupby("자치구").sum().reset_index()
        crime = crime.drop(columns=["관서명"])

        #  구 와 경찰서의 위치가 다른 경우 groupby 로 묶어서 작업
        # crime.loc[crime['관서명'] == '혜화서', ['자치구']] == '종로구'
        # crime.loc[crime['관서명'] == '서부서', ['자치구']] == '은평구'
        # crime.loc[crime['관서명'] == '강서서', ['자치구']] == '양천구'
        # crime.loc[crime['관서명'] == '종암서', ['자치구']] == '성북구'
        # crime.loc[crime['관서명'] == '방배서', ['자치구']] == '서초구'
        # crime.loc[crime['관서명'] == '수서서', ['자치구']] == '강남구'

        police = pd.pivot_table(crime, index = '자치구', aggfunc=np.sum).reset_index()
        print("🎆🎇🎄", police.head())

        police['살인검거율'] = (police['살인 검거'].astype(int) / police['살인 발생'].astype(int)) * 100
        police['강도검거율'] = (police['강도 검거'].astype(int) / police['강도 발생'].astype(int)) * 100
        police['강간검거율'] = (police['강간 검거'].astype(int) / police['강간 발생'].astype(int)) * 100
        police['절도검거율'] = (police['절도 검거'].astype(int) / police['절도 발생'].astype(int)) * 100
        police['폭력검거율'] = (police['폭력 검거'].astype(int) / police['폭력 발생'].astype(int)) * 100
        police = police.drop(columns={'살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거'}, axis=1)
        
        police.to_csv(os.path.join(save_dir, 'police_in_seoul.csv'), index=False) 
        # ic(f"🔥💧police: {police.head()}")

        crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        crime_columns = ['살인', '강도', '강간', '절도', '폭력']
        
        for i in  crime_rate_columns:
            police.loc[police[i] > 100, 1] = 100  # 데이터값의 기간 오류로 100을 넘으면 100으로 계산
        police = police.rename(columns={
            '살인 발생': '살인',
            '강도 발생': '강도',
            '강간 발생': '강간',
            '절도 발생': '절도',
            '폭력 발생': '폭력'
        })

        x = police[crime_rate_columns].values
        min_max_scalar = preprocessing.MinMaxScaler()
        """
          스케일링은 선형변환을 적용하여
          전체 자료의 분포를 평균 0, 분산 1이 되도록 만드는 과정
          """
        x_scaled = min_max_scalar.fit_transform(x.astype(float))
        """
         정규화 normalization
         많은 양의 데이터를 처리함에 있어 데이터의 범위(도메인)를 일치시키거나
         분포(스케일)를 유사하게 만드는 작업
         """
        police_norm = pd.DataFrame(x_scaled, columns=crime_columns, index=police.index)
        police_norm[crime_rate_columns] = police[crime_rate_columns]
        police_norm['범죄'] = np.sum(police_norm[crime_rate_columns], axis=1)
        police_norm['검거'] = np.sum(police_norm[crime_columns], axis=1)
        police_norm.to_csv(os.path.join(save_dir, 'police_norm_in_seoul.csv'))

        this.police = police

        return this
       
       
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