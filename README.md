# Charge API

This is a project that allows charging debts via bank slips.

## Requirements

- Python (~3.10) + FastAPI 🐍
- Docker + docker-compose 🐋

## Getting Started

1. Clone the repo
```sh
   git clone git@github.com:victormartinez/chargeapi.git
```

2. Create a `.env` file from `env.sample`

3. Install the dependencies
    ```sh
    cd chargeapi/
    poetry install
    ```

4. Split the terminal and execute the commands below:
    ```sh
    make up
    make run
    ```

Application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000). For docs, access [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Main Commands

    ```sh
    make help
    ```

    ```sh
    make format
    ```

    ```sh
    make unit-test
    ```

    ```sh
    make integration-test
    ```

### Steps to manually testing

1. Ensure the application is up and access [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

2. Ingest a CSV file via `POST /debts/ingest`

3. (Async) Generate Bank Slips via worker 
    ```sh
    python -m chargeapi.exec -script generate_bank_slips
    ```

4. (Async) Send Bank Slips via worker
    ```sh
    python -m chargeapi.exec -script send_bank_slips
    ```

5. Use webhook to pay a debt via `PATCH /bankslips/pay`

6. Check the result via `GET /bankslips/pay`
