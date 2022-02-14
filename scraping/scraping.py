import requests
from bs4 import BeautifulSoup
from time import sleep


class get_data:

    # star_page페이지부터 page_num 페이지까지  특정 아이디의 링크 고유값을 추출

    def id_num(self,start_page,page_num): # 시작페이지와 끝 페이지

        list_nums=[]

        #https://movie.naver.com/movie/point/af/list.naver?&page={j}
        
        for j in range(start_page,page_num+1):
            # netizen's reviews

            header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}

            page_url=f"https://movie.naver.com/movie/point/af/list.naver?&page={j}"
            page =requests.get(page_url,headers=header)
            soup = BeautifulSoup(page.content,'html.parser')
            # 
            tr=soup.find_all('tr')
            # url 접속을 위한 고유 번호 추출
            
            for i in range(1,11): # 리뷰는 총 10줄임
                raw_data_1=tr[i].find_all('a')
                raw_data_2=str(raw_data_1).split('=')[4]
                id_num=raw_data_2.split('&')[0]
                list_nums.append(id_num)
        return list_nums

    
    # id_num으로부터 받은 링크 고유값을 각각 들어가서 정해진 페이지 만큼 고유값, 영화 제목, 평점, 리뷰를 꺼내온다.
    def rating_review(self,start_page,page_num): # id_num과 동일한 변수를 받는다.
        list=[]
        dic={}
        for h,num in enumerate(self.id_num(start_page,page_num)):# list_nums를 받아서 for문을 돌린다. 이부분은 각 개인 id(num)가 들어간다.


            sleep(0.001*h) # 차단 방지를 위해 쉬는 시간을 변칙적으로 넣어준다.

            for m in range(1,100): # 리뷰어의 리뷰 모음으로 따라 들어간 후 그 안에서 페이지수로 적은 만큼 반복(100은 리뷰를 많이 쓰는 사람을 위해 충분히 많은 수로 넣어줬다.)
                

                # 크롤링을 할 때 차단되는 것을 방지해준다고 한다.
                header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
                
                next_url=f"https://movie.naver.com/movie/point/af/list.naver?st=nickname&sword={num}&target=after&page={m}" 
                next_page =requests.get(next_url,headers=header)
                soup_next= BeautifulSoup(next_page.content,'html.parser')  
                tr_2=soup_next.find_all('tr')
                
        ######################################check page############################################################

            ## page가 마지막을 지나도 계속 같은 페이지를 유지한다.
                # 그래서 리뷰어의 리뷰 모음 각 페이지에서 첫번째 리뷰의 고유값을 추출해서 다음 칸으로 넘어갔을 때 페이지의 첫번째 리뷰의 고유값을 대조한다.
            #  그 후 같다면 for문에서 탈출한다.(같은 페이지라는 의미)

                check_1=0
                check_2=0


                # 가끔 첫번째 리뷰 고유값 추출에 이해 못 할 오류가 있어서 오류가 났을 때는 넘어가는 구문이다.(아마도 크롤링 차단/ 리스트 개수 오류가 난다.)
                try:
                    check_1=str(tr_2).split("'")[-4]
                
                
                   
                    next_url_check=f"https://movie.naver.com/movie/point/af/list.naver?st=nickname&sword={num}&target=after&page={m+1}" # m+1
                
                    next_page_check =requests.get(next_url_check)
                    soup_next_check= BeautifulSoup(next_page_check.content,'html.parser')  
                    tr_2_check=soup_next_check.find_all('tr')
                

                    check_2= str(tr_2_check).split("'")[-4]
                except:
                    pass
                
        ######################################check page############################################################                
              
                try:# 리뷰 꺼내온다.
                    for k in range(1,11):# 리뷰는 몇 개인지 모른다 그래서 최댓값 10 넣고 오류 생기면 패스로 넘긴다.
                        raw_data_name_1= tr_2[k].find_all('a')
                        raw_data_name_2= str(raw_data_name_1).split(">")[1]
                        name= raw_data_name_2.split("<")[0]

                        raw_data_rating_1=tr_2[k].find_all('em')
                        raw_data_rating_2=str(raw_data_rating_1).split(">")[1]
                        rating= raw_data_rating_2.split("<")[0]

                        raw_data_review=tr_2[k].find_all('a')
                        review=str(raw_data_review).split("'")[5]
                        
                        dic={'id':num,'movie':name,'rating':rating,'review':review}
                        list.append(dic)
                        
                except:
                    pass
                
                # 위에서 구한 체크를 위한 구문이다. 특정 페이지와 그 다음 페이지의 첫번째 리뷰 고유값을 구해서 대조한다.
                if check_1==check_2:
                    break
               
        return list         


    # txt를 data_n 형식으로 만들어준다. 한 데이터 파일에 전체 리뷰 페이지속 모든 유저(10명)의 리뷰 모음이 들어간다.
    def txt_maker(self,start_page,page_num):# rating_review 함수를 받기 위해 전체 리뷰의 시작 페이지와 끝 페이지가 필요하다. 그리고 n의 값은 정해준 페이지 개수이다.
        for i in range(1,page_num):
    
            list=self.rating_review(i,i+1)
    
            f = open(f"data/data_{i}.txt",'w')
            f.write(str(list)+"\n")
            f.close()

            sleep(0.003*i)




