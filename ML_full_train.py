import joblib
from function.recommend import movie
import pymysql
import pandas as pd
import pickle


from surprise import SVD ,Reader, accuracy
from surprise import Dataset
from surprise.model_selection import train_test_split


# 데이터 프레임에 불러오기
conn=pymysql.connect(
    user="root",
    password='dlwdjfk',
    host='localhost',
    charset='utf8',
    db='movie'
)

cur=conn.cursor()

sql="""select * from movie.rating"""

cur.execute(sql)

tuple_df=cur.fetchall()

conn.commit()
conn.close()

df=pd.DataFrame(list(tuple_df))

# suprise 라이브러리를 사용하기 위해 사용자 , 이름, 평점 순으로 바꿔준다.
df=df.drop(columns=[0,4]).rename(columns={1:'userID',2:'itemID',3:'rating'})

# movies 목록을 따로 추출해준다.
movies=df['itemID'].drop_duplicates(keep='first').to_frame(name='title')


reader= Reader(rating_scale=(0,10))
data= Dataset.load_from_df(df[['userID','itemID','rating']], reader)

trainset = data.build_full_trainset()

algorithm=SVD()
algorithm.fit(trainset)
#################################



joblib.dump(algorithm,'./model.pkl')




# tuple1=(
#     ('asdf'	,'공공의 적 2'	,10),
#     ('asdf'	,'모노노케 히메'	,6),
#     ('asdf'	,'킬 빌 - 2부'	,9),
#     ('asdf'	,'위대한 산티니'	,10),
#     ('asdf'	,'젠틀맨 리그'	,1),
#     ('asdf'	,'레이디킬러'	,10),
#     ('bcad','킬 빌 - 1부',10),
#     ('bcad','킬 빌 - 2부',5),
#     ('bcad','위대한 산티니',3)
#     )




# rating_data=list(tuple1)

# movies_data=movies


# a=movie(rating_data,movies_data)

# userid='bcad'

# a.recommend(algorithm,userid,top_n=10)





