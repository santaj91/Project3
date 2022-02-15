from function.recommend import movie
import pymysql
import pandas as pd


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

movies=df['itemID'].drop_duplicates(keep='first').to_frame(name='title')


print(movies)