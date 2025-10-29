all: hymns.json

install:
	pip install -r requirements.txt

hymns.json:
	python get_hymns.py

clean:
	rm -f hymns.json
