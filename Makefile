CONTAINER_NAME := sort-font:python
PORT := 8888

run:
	python3 server.py

clean:
	rm -rf static/images/
	mkdir -p static/images/

docker/build:
	# docker build --tag sort-font:python .
	docker build --tag ${CONTAINER_NAME} .

docker/run:
	# docker run --rm -p 8888:8888 -e PORT=8888 sort-font:python
	docker run  --rm -p ${PORT}:${PORT} -e PORT=${PORT} ${CONTAINER_NAME}
