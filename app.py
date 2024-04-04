import joblib
from flask import Flask, render_template, request
import requests
import pandas

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

app = Flask(__name__)

@app.route('/Recommend', methods=["GET", "POST"])
def hello():
    data = []
    poster = []
    if request.method == "POST" and request.form['moviename'] != "":
        moviename = request.form['moviename']
        with open('movie_list.pkl', 'rb') as f:
            new_df = joblib.load(f)
            with open('similarity.pkl', 'rb') as h:
                similarity = joblib.load(h)
                movie_index = new_df[new_df['title'] == moviename].index[0]
                movie_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
    
                for i in movie_list:
                    movie_id = new_df.iloc[i[0]].movie_id
                    poster.append(fetch_poster(movie_id))
                    data.append(new_df.iloc[i[0]].title)
                
    if len(data) > 0:
        return render_template('Recommend.html', data=data, poster=poster)
    else:
        return render_template('Recommend.html', data=["None"], poster=["none"])

@app.route('/')
def all_movies():
    poster = []
    data = []
    with open('movie_list.pkl', 'rb') as f:
        new_df = joblib.load(f)
        for i in new_df['movie_id'][0:50]:
            poster.append(fetch_poster(i))
        for i in new_df['title'][0:50]:
            data.append(i)
            
    return render_template('index.html', data=data, poster=poster)
