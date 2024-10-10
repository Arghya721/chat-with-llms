live-reload:
	cd app && uvicorn main:main --port 5000 --reload

start-web:
	cd web && npm start