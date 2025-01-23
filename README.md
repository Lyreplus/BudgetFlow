# BudgetFlow

A Slurm plugin for budget management.
BudgetFlow assign a budget to each user and checks if the user has enough budget to run the job.

## Index

- [Installation](#installation)
    - [Docker](#docker)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [Authors](#authors)
- [Project Status](#project-status)
- [Project Structure](#project-structure)

## Installation

To install BudgetFlow, you need to clone the repository and run the setup script.

```bash
git clone https://github.com/Lyreplus/BudgetFlow.git
cd BudgetFlow
pip install -r requirements.txt
lua lua/job_submit.lua
```

Note: BudgetFlow requires Python 3.10 or higher.
Prolog.py has to be launched via job_submit.lua script.

### Docker compose

You can setup the necessary environment for BudgetFlow, alongside a PostgreSQL database, using the <code>compose.yml</code> file. You'll only need to create the folder <code>./test_compose/data/</code> to store the database.
For the following environment variables, you'll have to store them in a file called <code>budgetflow-database.env</code>, into the folder <code>./test_compose/env/</code>.

```bash
docker compose pull && docker compose up
```

## Configuration

BudgetFlow requires a PostgreSQL database to store the budget information.
You need to set the following environment variables, to configure the database connection:

```bash
DB_NAME=database_name
DB_USER=database_user
DB_PASSWORD=database_password
DB_HOST=database_host
DB_PORT=database_port (default=5432)
POSTGRES_PASSWORD=postgres_password
```

## Contributing

To contribute to BudgetFlow, you can open an issue or a pull request.

## Authors

- [Lyreplus](https://github.com/Lyreplus)

## Project Status

BudgetFlow is currently in development.

## Project Structure

```
.
├── budgetflow
│   ├── multi_job
│   │   ├── file_lock.py
│   │   ├── flock.py
│   │   ├── queue_job.py
│   │   └── save_job.py
│   ├── roles
│   │   ├── __init__.py
│   │   └── roles.py
│   ├── utils 
│   │   ├── __init__.py
│   │   ├── database_utils.py
│   │   └── utils.py
│   ├── prolog.py
│   ├── epilog.py
│   └── resources_coefficients.txt
├── docs
│   ├── db_ideas.md
│   ├── job_attributes.md
├── lua
│   └── job_submit.lua
├── test_compose
│   └── compose.yml
├── Dockerfile
├── database_schema.pdf
├── README.md
└── requirements.txt
```

