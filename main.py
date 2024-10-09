from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import requests
import os

API_KEY = "YOUR_MOVIE_DB_API_KEY"
MOVIE_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_INFO_URL = "https://api.themoviedb.org/3/movie"
POSTER_URL = "https://image.tmdb.org/t/p/w500/"

app = Flask(__name__)
app.config['SECRET_KEY'] = '2NH9B7FCLp2jGwrJmgdmDYIOHq0OQCsR'
Bootstrap5(app)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'movies.db')
db = SQLAlchemy(app)


class Movie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()
    

class EditForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")

class AddForm(FlaskForm):    
    title = StringField('Movie Title')
    submit = SubmitField('Add Movie')


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating).limit(10))
    all_movies = result.scalars().all()   
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    
    return render_template('index.html', movies=all_movies)

@app.route("/edit_movie", methods=["GET", "POST"])
def edit_movie():
    form = EditForm()
    movie_id = request.args.get("id")
    movie_to_update = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
            if form.rating.data:
                movie_to_update.rating = form.rating.data
            if form.review.data:
                movie_to_update.review = form.review.data
            db.session.commit()
            return redirect(url_for('home'))
        
    return render_template('edit.html', movie=movie_to_update, form=form)

@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    form = AddForm()
    if form.validate_on_submit():
        if form.title.data:
            movie_title = form.title.data
            response = requests.get(MOVIE_SEARCH_URL, params={"api_key": API_KEY, "query": movie_title})
            data = response.json()["results"]
            return render_template("select.html", options=data)
        return redirect(url_for('home'))
    return render_template('add.html', form=form)

@app.route("/find_movie")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{MOVIE_INFO_URL}/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": API_KEY, "language": "en-US"})
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            description=data["overview"],
            img_url=f"{POSTER_URL}{data['poster_path']}",
            rating=data["vote_average"],
            review="No review yet",
            ranking=1
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("home"))
        
@app.route("/delete_movie/<int:id>")
def delete_movie(id):
    movie_to_delete = db.get_or_404(Movie, id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
