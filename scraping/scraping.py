import requests
from bs4 import BeautifulSoup



class get_data:
    # 1페이지부터 page_num까지 반복 그리고 그 안에서 다시 15회 반복해서 num를 추출
    def id_num(self,page_num):

        list_nums=[]

        #https://movie.naver.com/movie/point/af/list.naver?&page={j}
        
        for j in range(1,page_num+1):
            # netizen's reviews
            page_url=f"https://movie.naver.com/movie/point/af/list.naver?&page={j}"
            page =requests.get(page_url)
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

    
    def rating_review(self,page_num):
        list=[]
        dic={}
        for h,num in enumerate(self.id_num(page_num)):# list_num을 받아서 for문을 돌린다. 이부분은 각 개인 id(num)가 들어간다.
            globals()['list_name'+str(h)]=[]
           
            for m in range(1,100): # 리뷰어의 리뷰 모음으로 따라 들어간 후 그 안에서 페이지수로 적은 만큼 반복
                
                next_url=f"https://movie.naver.com/movie/point/af/list.naver?st=nickname&sword={num}&target=after&page={m}" 
                next_page =requests.get(next_url)
                soup_next= BeautifulSoup(next_page.content,'html.parser')  
                tr_2=soup_next.find_all('tr')
                
        ######################################check page############################################################

            ## page가 마지막을 지나도 계속 같은 페이지를 유지한다.
                # 그래서 리뷰어의 리뷰 모음 각 페이지에서 첫번째 리뷰의 고유값을 추출해서 다음 칸으로 넘어갔을 때 페이지의 첫번째 리뷰의 고유값을 대조한다.
            #  그 후 같다면 for문에서 탈출한다.(같은 페이지라는 의미)

                check_1=0
                check_2=0


                # 가끔 첫번째 리뷰 고유값 추출에 이해 못 할 오류가 있어서 오류가 났을 때는 넘어가는 구문이다.
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
              
                try:
                    for k in range(1,11):# 리뷰는 몇개인지 모른다 그래서 최댓값 15 넣고 오류 생기면 패스로 넘긴다.
                        raw_data_name_1= tr_2[k].find_all('a')
                        raw_data_name_2= str(raw_data_name_1).split(">")[1]
                        name= raw_data_name_2.split("<")[0]

                        raw_data_rating_1=tr_2[k].find_all('em')
                        raw_data_rating_2=str(raw_data_rating_1).split(">")[1]
                        rating= raw_data_rating_2.split("<")[0]

                        raw_data_review=tr_2[k].find_all('a')
                        review=str(raw_data_review).split("'")[5]
                        
                        dic={'id':num,'movie':name,'stars':rating,'review':review}
                        list.append(dic)
                        
                except:
                    pass
                
                # 위에서 구한 고유값을 대조한다
                if check_1==check_2:
                    break
                
                
        return list         

