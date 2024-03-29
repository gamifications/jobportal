# [Job Portal](http://djangojobupwork.herokuapp.com/)


## Running the Project Locally

1. First, clone the repository to your local machine and add `.env` file and `db.sqlite3` file:
	```bash
	git clone https://github.com/gamifications/jobportal
	cd jobportal
	cp .env.example .env
	cp sample.sqlite3 db.sqlite3
	```

1. Setup a test stripe account and update `STRIPE_TEST_PUBLIC_KEY` and  `STRIPE_TEST_SECRET_KEY` in `.env` file:

	```
	STRIPE_TEST_PUBLIC_KEY=pk_test_xxxxx
	STRIPE_TEST_SECRET_KEY=sk_test_xxxxx
	```

2. Ideally, create a [virtualenv](https://docs.python-guide.org/dev/virtualenvs/):
	```bash
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
