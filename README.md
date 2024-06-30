## Running the project

**macOS or Linux*
```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Navigate to the project directory
cd pollsapp

# Run the Django development server
python manage.py runserver
```
**Windows**

```powershell


# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Navigate to the project directory
cd pollsapp

# Run the Django development server
python manage.py runserver


```


## Landon's Django Notes

I will be documenting my understanding of how the Django folder structure works and comparing it to other frameworks for learning purposes. This repository is intended to help me understand the folder structure of Django and to follow best learning practices.

### Folder Structure

```
pollsapp/
    manage.py
    pollsapp/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

- The outer folder **pollsapp** is a container for the project. The name doesn't matter to Django and can be anything.

- **manage.py** is a command-line utility that lets you interact with Django in various ways, which is why it's called `manage.py`. It is used to interact with and manage the project. It's similar to how **php artisan** works in a **Laravel** project, or how the **nest** command is used in **NestJS**. `manage.py` is used to run the server, create migrations, apply migrations, and run tests.

- The inner folder **pollsapp** is the actual Python package for the project. Its name is the Python package name you will need to use to import anything inside of it:
    ```python
    from pollsapp import urls
    ```

- **pollsapp/__init__.py** is an empty file that tells Python that this directory should be considered a Python package.

- **pollsapp/settings.py** is the settings configuration file for the project. This is similar to how a `.env` file would be used in a NestJS project and then be referenced in a `config.module.ts` file, or how a `.env` file would be used in a Laravel project and then referenced in `config/database.php`. `settings.py` is a centralized configuration file that contains settings for the database, middleware, installed apps, templates, static files, and more.

- **pollsapp/urls.py** is where the URL declarations for the Django project live, serving as a "Table of Contents" for the Django-powered site. It's where all the endpoints are defined. It's similar to how NestJS uses controllers and route decorators, or how Laravel uses `routes/web.php` and `routes/api.php`. In Django, the `urls.py` file uses `path()` or `re_path()` to map URLs to views, making it a central file to define URL patterns and routing them to views.

- **pollsapp/asgi.py**: ASGI stands for **Asynchronous Server Gateway Interface**. This file is the entry point for ASGI-compatible web servers to serve your project. It is similar to `wsgi.py` but is designed for asynchronous web servers and applications. You could compare this to `main.ts` in NestJS or `public/index.php` in Laravel. It uses `get_asgi_application()` to set up the application. It's used for real-time features like WebSockets, HTTP/2, etc., and is designed to handle both synchronous and asynchronous communication. ASGI supports long-lived connections like WebSockets and other asynchronous protocols.

- **pollsapp/wsgi.py**: WSGI stands for **Web Server Gateway Interface**. This file allows Django applications to handle HTTP requests and is used for traditional web applications. It is a standard interface between web servers and Python web applications or frameworks. WSGI is designed for synchronous communication, similar to `main.ts` in NestJS or `public/index.php` in Laravel.



