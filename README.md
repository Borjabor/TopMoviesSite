# Movie Database Project

This project is a learning exercise focused on Python web development, SQLite3 with SQLAlchemy. It also includes API calls to The Movie Database (TMDb).

## Overview

The `main.py` file is the entry point of the project, containing the Flask web application that interacts with the SQLite database using SQLAlchemy.

## Features

* Displays a list of watched movies on the homepage, ranked in order of rating
* Allows users to add new movies to the database
* Enables users to edit and delete existing movies
* Retrieves movie data from TMDb API

## Requirements

* Python 3.x
* Flask
* Flask-SQLAlchemy
* SQLite3
* TMDb API key (replace `YOUR_MOVIE_DB_API_KEY` with your actual API key)

## Running the Project

1. Clone the repository
2. Install the dependencies: `pip install -r requirements.txt`
3. Run the project: `python main.py`
4. Open a web browser and navigate to `http://localhost:5000`

## API Documentation

The project uses the TMDb API to retrieve movie data. You can find the API documentation [here](https://developers.themoviedb.org/3/getting-started/introduction).

## Database Schema

The project uses a SQLite database with the following schema:

* `movies` table:
	+ `id` (primary key)
	+ `title`
	+ `year`
	+ `description`
	+ `rating`
	+ `ranking`
	+ `review`
	+ `img_url`

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
