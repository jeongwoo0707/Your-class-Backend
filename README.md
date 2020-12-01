# pilot_project
# Your-class-Backed
Pilot-project at DGU CSE 2020-2-Introduction to Software Engineering-Team hAAArd Work

# Usage
Your class is a Learning Management System for Your Students!

# Include (Apps)
```
accounts
Student & Instructor models
Views for CRUD user models & profile
```

```
subject
Class & Enroll models
Views for CRUD Classes & Enroll your student
```

```
assignment
Assignment & Submit models
Views for CRUD Assignments & Submissions
Upload/Download your Assignments files & Submission Files
```

```
post
Q&A & Notice models
Views for CRUD Q&As & Notices
```
## Project setup
```
pip3 install django
pip3 install -r requirements.txt
```

## If psycopg2 error occurred
```
pip3 install psycopg2_binary
```

## Add your own SECRET_KEY, DATABASE, HOST, etcs at settings.py

## Migrate your settings
```
python3 manage.py makemigrations
python3 manage.py migrate
```

## Compiles for development
```
python3 manage.py runserver
```

## Complies for Deploy Productions
```
Edit DEBUG = True to DEBUG=False at settings.py
```

### Customize configuration
See [Django REST framework Reference](https://www.django-rest-framework.org/).

