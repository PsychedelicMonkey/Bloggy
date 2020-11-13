# Bloggy
Simple Blog application written in Python-Flask and Bootstrap 4.

# Installation

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
