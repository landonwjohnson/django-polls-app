Here is the updated markdown file with the links added:

```markdown
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
- [Project Vs Apps](PROJECTVSAPPS.md)
- [Project Directory](PROJECTDIRECTORY.md)
- [App Directory](APPDIRECTORY.md)
