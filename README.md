# [Job Portal](http://djangojobupwork.herokuapp.com/)


## Running the Project Locally

1. First, clone the repository to your local machine and add `.env` file and `db.sqlite3` file:
    ```bash
    git clone https://github.com/gamifications/jobportal
    cp .env.example .env
    cp sample.sqlite3 db.sqlite3
    ```

2. Ideally, create a [virtualenv](https://docs.python-guide.org/dev/virtualenvs/):
	```bash
	cd jobportal
	python3 -m venv env
	source env/bin/activate
	```

3. Install requirements
	```bash
	pip install -r requirements.txt
	```

4. Init database and runserver
	```bash
	./manage.py migrate
	./manage.py djstripe_sync_plans_from_stripe
	./manage.py loaddata datas.json
	./manage.py runserver
	```

5. The project will be available at http://127.0.0.1:8000, Login using::
	+ email: `test@test.com`
	+ password: `testuser`
