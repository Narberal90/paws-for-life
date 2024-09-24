
# Paws For Life

Paws For Life is a website for an animal shelter where users can apply to adopt a cat or dog and register for walks with dogs. The administrator manages the animals and adoption requests.


You can see deployed project by the link below

> https://paws-for-life.onrender.com/

Use this credentials to log in:

**Username** `Test` 

**Password** `Qwerty123!` 

## Functionality

- **Adoption Requests**: Visitors can apply to adopt cats and dogs. The administrator can approve or reject these requests.
- **Profile Phone Number**: A phone number is required to submit an adoption request, so users need to complete their profile.
- **Dog Walk Registration**: Visitors can register for a dog walk between 10:00 and 17:00, for today or tomorrow.
- **Homepage**: Displays the total number of animals accepted, adopted, and available for adoption.
- **Animal Management**: The administrator can add new animals, their descriptions, and photos. Only cats and dogs can be adopted.

## Clone the repository

```bash
git clone https://github.com/Narberal90/paws-for-life
cd paws-for-life
```

## Installation

1. Create and activate a virtual environment:

    For Unix systems:
    ```bash
    python -m venv env
    source venv/bin/activate
    ```

    For Windows systems:
    ```bash
    python -m venv env
    venv\Scripts\activate
    ```

2. Install the requirements:

    ```bash
    pip install -r requirements.txt
    ```

3. Make database migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. (Optional) Load fixture data:

    ```bash
    python manage.py loaddata all_data.json
    ```

5. Create a superuser and run the server:

    ```bash
    python manage.py createsuperuser
    python manage.py runserver
    ```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Project Structure

```

Project
├── paws_for_life
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── shelter
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── urls.py
│   ├── views.py
│   └── migrations
│       └── __init__.py
│
├── static
│   
├── templates
│   
├── all_data.json
│
├── manage.py
│
└── requirements.txt

```

## Requirements

All dependencies are listed in the `requirements.txt` file.

## Author

Developed by Narberal90.


![Project diagram](diagram.png)