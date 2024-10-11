live-reload:
	cd app && uvicorn main:app --port 5000 --reload

start-web:
	cd web && npm start

lint:
	black .