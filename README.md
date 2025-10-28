# FinanceProject



# Activate the virtual environment

    python3 -m venv venv
    source .venv/bin/activate

# Install all dependencies

    pip install -r requirements.txt
    //
    curl -LsSf https://astral.sh/uv/install.sh | sh
    uv --version

# To run the Django development server, use the following command:

    python3 manage.py runserver

# To run migrations, use the following commands:
    
    cd investapp
    python3 manage.py makemigrations
    python3 manage.py migrate

# To use admin panel, create a superuser with the following command:
    
    python3 manage.py createsuperuser

