

## Running the Project

### macOS or Linux
```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Navigate to the project directory
cd mysite

# Run the Django development server
python manage.py runserver
```

### Windows
```powershell
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Navigate to the project directory
cd mysite

# Run the Django development server
python manage.py runserver
```

### Running Migrations
```bash
# If you see a message like this:
# You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.

# Simply run this command to apply the migrations
python manage.py migrate
```

---

## Landon's Django Notes

I will be documenting my understanding of how the Django folder structure works and comparing it to other frameworks for learning purposes. This repository is intended to help me understand the folder structure of Django and to follow best learning practices.

### The Project Directory 
A Django project is the entire web application, containing settings, configurations, and multiple apps. It is not a single function or feature but a collection of apps working together to create a complete website.

#### Folder Structure

```
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

- **Outer Folder (mysite)**: A container for the project. The name doesn't matter to Django and can be anything.
- **manage.py**: A command-line utility to interact with Django, similar to `php artisan` in Laravel or the `nest` command in NestJS. Used to run the server, create migrations, apply migrations, and run tests.
- **Inner Folder (mysite)**: The actual Python package for the project. This name is used to import anything inside it.
    ```python
    from mysite import urls
    ```
- **mysite/__init__.py**: An empty file that tells Python this directory should be considered a Python package.
- **mysite/settings.py**: The settings configuration file, similar to a `.env` file in other frameworks. It contains settings for the database, middleware, installed apps, templates, static files, and more.
- **mysite/urls.py**: Where the URL declarations for the Django project live, serving as a "Table of Contents" for the site. Similar to controllers and route decorators in NestJS or `routes/web.php` and `routes/api.php` in Laravel.
- **mysite/asgi.py**: ASGI stands for **Asynchronous Server Gateway Interface**. This file is the entry point for ASGI-compatible web servers. It supports real-time features like WebSockets and HTTP/2, handling both synchronous and asynchronous communication.
- **mysite/wsgi.py**: WSGI stands for **Web Server Gateway Interface**. This file allows Django applications to handle HTTP requests and is used for traditional web applications, similar to `main.ts` in NestJS or `public/index.php` in Laravel.

---

### The App Directory 

A Django app is a self-contained module that performs a specific function (e.g., blog, forum). It is not the entire project but a part of it. An app can be reused in multiple projects.

#### Folder Structure

```
polls/
    migrations/
    __init__.py
    admin.py
    apps.py
    models.py
    tests.py
    views.py
```

---

## Projects vs. Apps

### Imagine a Website as a Town

Think of a website as a town with different buildings, each doing a specific job.

- **Project**: The project is the entire town. It includes all the buildings and the rules for how everything works together.
- **App**: Each app is a single building in the town, each with a specific job. For example, a library for reading books, a post office for sending mail, and a grocery store for buying food.

### Key Points

- The town (project) can have many buildings (apps).
- A building (app) can be part of many different towns (projects).

### Examples

#### Example 1: Blog and Forum

- **Project**: `MyWebsite`
  - **Apps**:
    - `Blog`: Like a library where you can read and write blog posts.
    - `Forum`: Like a community center where people can have discussions.

In this example, `MyWebsite` is the town that includes both the Blog and Forum buildings (apps).

#### Example 2: Online Store

- **Project**: `OnlineStore`
  - **Apps**:
    - `Products`: Like a supermarket where you can see and buy products.
    - `Cart`: Like your shopping cart where you collect items you want to buy.
    - `Accounts`: Like the customer service office where you manage your account details.

Here, `OnlineStore` is the town, and it includes apps that handle products, the shopping cart, and user accounts.

#### Example 3: Reusing an App

- **Projects**:
  - `ProjectA`
  - `ProjectB`
  - `ProjectC`
  - All these towns use the `Newsletter` app to send out newsletters to people.

In this case, the `Newsletter` app is a special service that can be used by multiple towns (projects). So `ProjectA`, `ProjectB`, and `ProjectC` can all have a post office (Newsletter app) that sends newsletters.

### Comparisons with Other Frameworks

#### NestJS

- **Project**: The whole town.
- **Module**: Each building with a specific job.
  - **Example**:
    - **Project**: `NestApp`
      - **Modules**:
        - `UserModule`: Manages users.
        - `ProductModule`: Manages products.

#### Node.js with Express

- **Project**: The whole town.
- **Module**: Each building with a specific job.
  - **Example**:
    - **Project**: `ExpressApp`
      - **Modules**:
        - `userRoutes`: Manages user routes.
        - `productRoutes`: Manages product routes.

#### Laravel

- **Project**: The whole town.
- **Package**: Each building with a specific job.
  - **Example**:
    - **Project**: `LaravelApp`
      - **Packages**:
        - `UserManagement`: Manages users.
        - `Ecommerce`: Manages products.
        - `Blog`: Manages blog posts.

#### Flask

- **Project**: The whole town.
- **Blueprint**: Each building with a specific job.
  - **Example**:
    - **Project**: `FlaskApp`
      - **Blueprints**:
        - `auth`: Manages user authentication.
        - `blog`: Manages blog posts.

### Summary

In simpler terms:

- A **project** is like a whole town with all its buildings and rules.
- An **app** (or module/package/blueprint) is like a single building in that town, each doing its own specific job.
- You can have multiple buildings (apps) in one town (project).
- A single building (app) can be part of many different towns (projects).

This way of organizing things is used in Django, NestJS, Express (Node.js), Laravel, and Flask, even though the names and details might be a bit different.
