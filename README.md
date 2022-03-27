# task_fastapi


### 개발 환경
- 언어: 파이썬 3.9
- DB: Mysql 5.7
- 프레임워크: FastApi
- ORM: Totoise ORM


### install
```
python -m venv .venv

. .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

aerich upgrade

python fixture.py

uvicorn main:app --reload
```

### url
- swaager: http://127.0.0.1:8000/docs
- redoc: http://127.0.0.1:8000/redoc

### commands
```sh
# runserver
uvicorn main:app --reload

aerich init -h
aerich init -t core.constants.TORTOISE_ORM
aerich init-db

# make migrations
aerich migrate --name {name}

# migrate
aerich upgrade

# shell
tortoise-cli -c core.constants.TORTOISE_ORM shell
```