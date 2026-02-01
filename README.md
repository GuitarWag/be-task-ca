# Backend Task - Clean Architecture

This project is a very naive implementation of a simple shop system. It mimics in its structure a real world example of a service that was prepared for being split into microservices and uses the current Helu backend tech stack.

## Goals

Please answer the following questions:

1. Why can we not easily split this project into two microservices?
2. Why does this project not adhere to the clean architecture even though we have seperate modules for api, repositories, usecases and the model?
3. What would be your plan to refactor the project to stick to the clean architecture?
4. How can you make dependencies between modules more explicit?

See [ANSWERS.md](ANSWERS.md) for detailed analysis and refactoring approach.

## Architecture

```
be_task_ca/
├── domain/entities/          # Pure business entities (User, Item, CartItem)
├── ports/repositories/       # Repository interfaces (contracts)
├── use_cases/               # Application business rules
│   ├── commands/           # DTOs for use case input
│   └── exceptions/         # Domain exceptions
├── adapters/repositories/   # In-memory implementations
└── drivers/rest/           # FastAPI HTTP layer
    ├── routers/
    ├── schemas/
    ├── dependencies.py     # DI container
    └── exception_handlers.py
```

*Please do not spend more than 2-3 hours on this task.*

Stretch goals:
* Fork the repository and start refactoring
* Write meaningful tests
* Replace the SQL repository with an in-memory implementation

## References
* [Clean Architecture by Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
* [Clean Architecture in Python](https://www.youtube.com/watch?v=C7MRkqP5NRI)
* [A detailed summary of the Clean Architecture book by Uncle Bob](https://github.com/serodriguez68/clean-architecture)

## How to use this project

If you have not installed poetry you find instructions [here](https://python-poetry.org/).

1. `docker-compose up` - runs a postgres instance for development
2. `poetry install` - install all dependency for the project
3. `poetry run schema` - creates the database schema in the postgres instance
4. `poetry run start` - runs the development server at port 8000
5. `/postman` - contains an postman environment and collections to test the project

## Other commands

* `poetry run graph` - draws a dependency graph for the project
* `poetry run tests` - runs the test suite
* `poetry run lint` - runs flake8 with a few plugins
* `poetry run format` - uses isort and black for autoformating
* `poetry run typing` - uses mypy to typecheck the project

## Specification - A simple shop

* As a customer, I want to be able to create an account so that I can save my personal information.
* As a customer, I want to be able to view detailed product information, such as price, quantity available, and product description, so that I can make an informed purchase decision.
* As a customer, I want to be able to add products to my cart so that I can easily keep track of my intended purchases.
* As an inventory manager, I want to be able to add new products to the system so that they are available for customers to purchase.