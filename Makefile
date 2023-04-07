create_backend_venv:
	cd backend
	python3 -m venv venv
	pip install .[dev,build]
	cd ..

run_backend:
	cd backend
	python -m personal_website
	cd ..

run:
	docker compose -f compose.yml -f compose.prod.yml up --build -d