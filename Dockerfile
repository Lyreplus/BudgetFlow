FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# some example arguments to run the program
CMD ["python", "budgetflow/prolog.py", "100", "id1", "4", "4", "1", "2", "4"]
