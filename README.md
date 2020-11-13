# Bloggy
Simple Blog application written in Python-Flask and Bootstrap 4.

# Installation

## Production
### Environment Varables
Environment variables can be stored in a '.env' file on the project root. Custom values are recommended for the following env variables:

#### Required Environment Variables
| Environment Vairable | Description |
| :-------------: | :---------- |
|  **SECRET_KEY** | The key needed for CSRF. Use of a randomly generated string is recommended in a production environment. |
| **DATABASE_URL** | The database connection string for SQLAlchemy. By default uses SQLite and creates an 'app.db' file on the project root if this variable is unset. Use of a dedicated SQL server is recommended for a production deployment. |
| **IMAGE_UPLOADS** | Directory to store user-uploaded images. If the Docker container is to be used, a volume must be mapped to the container's '/img' directory to retain images uploaded by users. Defaults to the 'static/img' directory from the main app directory. |
| **MAIL_SERVER** | IP Address or domain name of the mail server. A mail server is required for password recovery and sending syslog errors to admins. |
| **MAIL_PORT** | Port used by the mail server. Uses port 25 by default (not recommended because port 25 sends emails in plain text).  |
  
### Unsplash API Integration
This app uses the Unsplash API to give users an convenient way to include photos into blog posts.

An access key and a secret key is required from Unsplash to use their API with this application and must be binded to the two environment variables below:

- **UNSPLASH_ACCESS_KEY**
- **UNSPLASH_SECRET_KEY**

## Debug
1. Create a python virtual environment:
```
python -m venv venv
```

2. Install the required packages from the requirements.txt file:
```
pip install -r requirements.txt
```

3. Create a .env file in the document root and set the following environment variables:
```
FLASK_APP=bloggy.py
FLASK_DEBUG=1
MAIL_SERVER=localhost
MAIL_PORT=8025

UNSPLASH_ACCESS_KEY={insert-your-unsplash-access-key-here}
UNSPLASH_SECRET_KEY={insert-your-unsplash-secret-key-here}
```

4. For debugging issues with the email server run:
```
python -m smtpd -c DebuggingServer -n localhost:8025
```
