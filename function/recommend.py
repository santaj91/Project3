import pandas as pd


class movie:# 선언시 rating_data와 movies_data 필요

    def __init__(self,rating_data,movies_data):

        self.ratings=pd.DataFrame(rating_data,columns=['userid','title','rating'])
        self.movies=movies_data


        

    def unseen_list(self,userid):
        # ratings에 컬럼으로 userid, title, ratings가 있는데, ratings 테이블에서 변수로 받은 userid가 같은 데이터 중 title 목록만 리스트로 뽑는다. 
        seen_movies=self.ratings[self.ratings['userid']==userid]['title'].tolist()

        total_movies = self.movies['title'].tolist()

        unseen_movies = [movie for movie in total_movies if movie not in seen_movies]

        print(f"{userid}가 본 영화 수: {len(seen_movies)}\n 추천한 영화 개수 {len(unseen_movies)}\n 전체 영화수: {len(total_movies)} ")

        return unseen_movies

    def recommend(self,algorithm,userid,top_n=10):

        unseen_movies=self.unseen_list(userid)

        predictions = [algorithm.predict(str(userid),str(title))for title in unseen_movies]

        def sortkey_est(pred):
            return pred.est
        
        predictions.sort(key=sortkey_est, reverse=True)

        top_predictions= predictions[:top_n]

        top_movie_ids=[str(pred.iid) for pred in top_predictions]
        top_movie_ratings=[pred.est for pred in top_predictions]
        top_movie_titles=self.movies[self.movies.title.isin(top_movie_ids)]['title']

        top_movies_preds = [(ids,rating,title) for ids,rating,title in zip(top_movie_ids, top_movie_ratings, top_movie_titles)]

        for top_movie in top_movies_preds:
            print('* 추천 영화 이름: ', top_movie[2])
            print('* 해당 영화의 예측평점: ', top_movie[1])
            print()

        return top_movies_preds





        
        
        