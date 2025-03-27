Scrap Chef - Web Application

Project Overview
Scrap Chef is a web application designed for users to post, rate, and review their "struggle meals." The application allows users to create an account, upload meals, and rate them based on taste, ease of preparation, and struggle level. It is built using Python, Django, HTML, CSS, and other associated technologies including JavaScript, AJAX, and JQuery.


Features
User Authentication: Users can sign up, log in, and manage their profiles.
Post Uploading: Users can upload posts with media (images/videos) and captions for their meals.
Meal Rating: Users can rate meals based on taste, struggle, and preparation time.
Meal Saving: Users can save their favorite posts to their profile.
Feed and Dashboard: A personalized dashboard to view and manage posts, as well as an aggregated feed of all posts with ratings.
Responsive Design: The interface is responsive and adjusts according to screen size for both mobile and desktop views.

Technologies Used
Python 3.x
Django
HTML, CSS, JavaScript, JQuery, and AJAX
SQLite or PostgreSQL (for database)
Bootstrap (for responsive design)


Installation
Prerequisites
1. Python 3.x installed on your machine.
2. Django installed. You can install Django by running:
 
   ```bash
    pip install django
    ```

Setup Instructions
1. Clone the Repository

    ```bash
    git clone https://github.com/yourusername/scrapchef.git
    cd scrapchef
    ```

    2. Create a Virtual Environment

    ```bash
    python -m venv venv
    ```

    3. Activate the Virtual Environment

    - Windows:
    ```bash
    .\venv\Scripts\activate
    ```

    - Mac/Linux:
    ```bash
    source venv/bin/activate
    ```

    4. Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```

    5. Set Up the Database

    If you are using SQLite (default):
    ```bash
    python manage.py migrate
    ```

    6. Create a Superuser for Admin Access

    ```bash
    python manage.py createsuperuser
    ```

    7. Run the Development Server

    ```bash
    python manage.py runserver
    ```

    8. Access the Application

    Open your browser and go to `http://127.0.0.1:8000/`.

Deployment Instructions
- The application should be deployed on PythonAnywhere for production.
- Ensure that the latest version of the code is hosted on a public GitHub repository.
- Use a requirements.txt file to manage dependencies:

    ```bash
    pip freeze > requirements.txt
    ```
- Database files should not be committed. The database can be recreated from migrations.
- Provide a population script that loads relevant example data into the database.

Contribution
To contribute to Scrap Chef:
    1. Fork the repository.
    2. Create a new branch for your changes.
    3. Commit your changes and push them to your forked repository.
    4. Create a pull request for review.


External Libraries Used
- Bootstrap for responsive CSS.
- JavaScript/jQuery/AJAX for dynamic content updates without page reloads.

External API’s
youtube

Acknowledgements
- Special thanks to the Django framework for simplifying backend development.
- Bootstrap for providing responsive CSS features.

Team members: Lab group 5 E
Bayan Alkhuzaei - (3070264a)
Hans Novenson - (2889880n)
Liam Redmond - (2761753r)
Varshini Seshan - (2889241s)
Yiming Wang - (3025943w)
Zhihao Zhang - (2961112z)


