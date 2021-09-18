CONTAINER_NAME := sort-font:python
PORT := 8888

init:
	python3 -m venv venv

setup:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

run:
	python3 server.py

test:
	python3 -m pytest .

clean:
	rm -rf static/images/
	mkdir -p static/images/

docker/build:
	# docker build --tag sort-font:python .
	docker build --tag ${CONTAINER_NAME} .

docker/run:
	# docker run --rm -p 8888:8888 -e PORT=8888 sort-font:python
	docker run  --rm -p ${PORT}:${PORT} -e PORT=${PORT} ${CONTAINER_NAME}
