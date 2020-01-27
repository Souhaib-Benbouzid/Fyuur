Fyyur
-----

### Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

### Overview

This app is done under udacity fullstack web development nanodegree program 
the app is using a PostgreSQL database:

* creating new venues, artists, and creating new shows.
* searching for venues and artists.
* learning more about a specific artist or venue.

We want Fyyur to be the next new platform that artists and musical venues can use to find each other, and discover new music shows. Let's make that happen!

### Tech Stack

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependences
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`

Instructions
-----

1. Understand the Project Structure (explained above) and where important files are located.
2. Build and run local development following the Development Setup steps below.
3. Fill in the missing functionality in this application: this application currently pulls in fake data, and needs to now connect to a real database and talk to a real backend.
3. Fill out every `TODO` section throughout the codebase. We suggest going in order of the following:

  1. Connect to a database in `config.py`. A project submission that uses a local database connection is fine. [DONE]
  2. Using SQLAlchemy, set up normalized models for the objects we support in our web app in the Models section of `app.py`. Check out the sample pages provided at /artists/1, /venues/1, and /shows/1 for examples of the data we want to model, using all of the learned best practices in database schema design. Implement missing model properties and relationships using database migrations via Flask-Migrate. [DONE]
  3. Implement form submissions for creating new Venues, Artists, and Shows. There should be proper constraints, powering the `/create` endpoints that serve the create form templates, to avoid duplicate or nonsensical form submissions. Submitting a form should create proper new records in the database.[done]
  4. Implement the controllers for listing venues, artists, and shows. Note the structure of the mock data used. We want to keep the structure of the mock data.[done]
  5. Implement search, powering the `/search` endpoints that serve the application's search functionalities.[done]
  6. Serve venue and artist detail pages, powering the `<venue|artist>/<id>` endpoints that power the detail pages.[done]


### Development Setup

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) if you haven't already.

  ```
  $ cd ~
  $ sudo pip3 install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)
