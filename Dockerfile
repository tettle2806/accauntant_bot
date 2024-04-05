FROM python:3.10
LABEL authors="Zayniddin"
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
RUN chmod 755 .
COPY . .


CMD ["alembic", "revision", "--autogenerate", "-m", "'initial'"]
CMD ["alembic", "upgrade", "head"]
