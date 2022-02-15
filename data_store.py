import pymysql
from function.scraping import get_data
from time import sleep

conn=pymysql.connect(
    user="root",
    password='dlwdjfk',
    host='localhost',
    charset='utf8',
    db='movie'
)

cur=conn.cursor()
cur.execute("DROP TABLE IF EXISTS rating;")

cur.execute("CREATE TABLE rating(ID INT PRIMARY KEY AUTO_INCREMENT,NUM INT(10), title VARCHAR(100),rating INT(2) , review VARCHAR(1000));")

for i in range(1,1000):
    with open(f"data/data_{i}.txt",'r') as f:
        list=f.readlines()
        st_list=list[0]
    ex=eval(st_list)

    insert_sql = "INSERT INTO rating(NUM,title,rating,review) VALUES (%(id)s , %(movie)s,%(rating)s ,%(review)s);"
    cur.executemany(insert_sql,ex)


conn.commit()
conn.close()