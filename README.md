# Consumer Supply

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Set Up Virtual Environment](#set-up-virtual-environment)
  - [Install Dependencies](#install-dependencies)
  - [Configure Environment Variables](#configure-environment-variables)
  - [Apply Migrations](#apply-migrations)
  - [Run the Development Server](#run-the-development-server)
- [Running Tests](#running-tests)
  - [Unit and Functional Tests](#unit-and-functional-tests)
  - [Test Coverage](#test-coverage)
- [API Documentation](#api-documentation)
  - [Authentication](#authentication)
    - [User Registration](#user-registration)
    - [User Login](#user-login)
  - [Warehouses](#warehouses)
    - [Create Warehouse](#create-warehouse)
    - [List Warehouses](#list-warehouses)
    - [Retrieve Warehouse](#retrieve-warehouse)
    - [Update Warehouse](#update-warehouse)
    - [Delete Warehouse](#delete-warehouse)
  - [Products](#products)
    - [Create Product](#create-product)
    - [List Products](#list-products)
    - [Retrieve Product](#retrieve-product)
    - [Update Product](#update-product)
    - [Delete Product](#delete-product)
  - [Stocks](#stocks)
    - [Supply Product](#supply-product)
    - [Consume Product](#consume-product)
- [Permissions](#permissions)
- [Error Handling](#error-handling)
- [License](#license)

## Introduction

**Consumer Supply** is a Django-based RESTful API designed to manage the supply and consumption of products across multiple warehouses. The system distinguishes between two types of users:

- **Suppliers**: Users who can supply products to warehouses.
- **Consumers**: Users who can consume products from warehouses.

The application ensures secure access through token-based authentication and enforces strict permission controls to maintain data integrity and security.

## Features

- **User Authentication**: Secure registration and login using token-based authentication.
- **Role-Based Access Control**: Distinct permissions for suppliers and consumers.
- **Warehouse Management**: Create, retrieve, update, and delete warehouse records.
- **Product Management**: Manage product inventory with CRUD operations.
- **Stock Management**: Suppliers can supply products to warehouses, and consumers can consume products, with validation to prevent overconsumption.
- **Comprehensive Testing**: Functional tests using `pytest` and `pytest-django` to ensure API reliability.
- **Custom Error Handling**: Tailored error messages for better user experience.

## Technologies Used

- **Backend Framework**: Django 5.1.2, Django REST Framework
- **Authentication**: Token-based authentication
- **Testing**: Pytest, Pytest-Django
- **Database**: SQLite (default; can be configured to use other databases)
- **Version Control**: Git
- **Others**: Docker (optional for containerization)

## Architecture

The project follows a modular architecture with clear separation of concerns:

- **`consumer_supply/`**: Main project configuration.
- **`api/`**: Core application containing models, serializers, views, permissions, and tests.

## Installation

### Prerequisites

- **Python 3.12.7**
- **Git**
- **Virtual Environment Manager**: `venv` or `virtualenv`

### Clone the Repository

```bash
git clone https://github.com/whoisoldman/consumer_supply.git
cd consumer_supply
```

### Set Up Virtual Environment

Create and activate a virtual environment to manage dependencies.

```bash
# For Unix or MacOS
python3 -m venv .venv
source .venv/bin/activate

# For Windows
python -m venv .venv
.\.venv\Scripts\activate
```

### Install Dependencies

Install the required Python packages using `pip`.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the root directory to store environment-specific settings. This file should include sensitive information like secret keys and database configurations.

```bash
touch .env
```

**Sample `.env` Content:**

```env
DEBUG=True
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///db.sqlite3
```

> **Note**: Replace `your_secret_key_here` with a secure secret key. For production, set `DEBUG=False` and configure an appropriate database.

### Apply Migrations

Run database migrations to set up the necessary tables.

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser (Optional)

Create a superuser account to access the Django admin interface.

```bash
python manage.py createsuperuser
```

### Run the Development Server

Start the Django development server.

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`.

## Running Tests

### Unit and Functional Tests

The project includes a suite of tests to ensure API reliability.

#### **Run All Tests**

```bash
pytest -v
```

#### **Run Specific Test Module**

```bash
pytest -v api/tests/test_auth.py
```

### Test Coverage

To check how much of your code is covered by tests, use `pytest-cov`.

#### **Install `pytest-cov`**

```bash
pip install pytest-cov
```

#### **Run Tests with Coverage Report**

```bash
pytest --cov=api --cov-report=html -v
```

#### **View Coverage Report**

Open the generated HTML report in your browser:

```bash
open htmlcov/index.html
```

> **Note**: Ensure `pytest-cov` is included in your `requirements.txt` for consistency across environments.

## API Documentation

The API follows RESTful principles and supports JSON-formatted requests and responses. Below are the available endpoints and their functionalities.

### Authentication

#### User Registration

- **Endpoint**: `/api/register/`
- **Method**: `POST`
- **Description**: Register a new user as a supplier or consumer.
- **Request Body**:

  ```json
  {
      "username": "string",
      "email": "string",
      "password": "string",
      "password2": "string",
      "user_type": "supplier" | "consumer"
  }
  ```

- **Response**:

  - **Success (201 Created)**:

    ```json
    {
        "user": {
            "id": 1,
            "username": "string",
            "email": "string",
            "user_type": "supplier"
        },
        "token": "authentication_token"
    }
    ```

  - **Error (400 Bad Request)**:

    ```json
    {
        "password": ["Password fields didn't match."]
    }
    ```

#### User Login

- **Endpoint**: `/api/login/`
- **Method**: `POST`
- **Description**: Authenticate a user and retrieve an authentication token.
- **Request Body**:

  ```json
  {
      "username": "string",
      "password": "string"
  }
  ```

- **Response**:

  - **Success (200 OK)**:

    ```json
    {
        "token": "authentication_token"
    }
    ```

  - **Error (400 Bad Request)**:

    ```json
    {
        "detail": "Invalid credentials."
    }
    ```

### Warehouses

#### Create Warehouse

- **Endpoint**: `/api/warehouses/`
- **Method**: `POST`
- **Description**: Create a new warehouse. Only suppliers can perform this action.
- **Authentication**: Required (Token)

- **Request Body**:

  ```json
  {
      "name": "string",
      "address": "string"
  }
  ```

- **Response**:

  - **Success (201 Created)**:

    ```json
    {
        "id": 1,
        "name": "string",
        "address": "string",
        "owner": "supplier_username"
    }
    ```

  - **Error (403 Forbidden)**:

    ```json
    {
        "detail": "You do not have permission to perform this action."
    }
    ```

#### List Warehouses

- **Endpoint**: `/api/warehouses/`
- **Method**: `GET`
- **Description**: Retrieve a list of all warehouses.
- **Authentication**: Required (Token)

- **Response**:

  - **Success (200 OK)**:

    ```json
    [
        {
            "id": 1,
            "name": "Warehouse A",
            "address": "123 Main St",
            "owner": "supplier1"
        },
        {
            "id": 2,
            "name": "Warehouse B",
            "address": "456 Elm St",
            "owner": "supplier2"
        }
    ]
    ```

#### Retrieve Warehouse

- **Endpoint**: `/api/warehouses/{id}/`
- **Method**: `GET`
- **Description**: Retrieve details of a specific warehouse by ID.
- **Authentication**: Required (Token)

- **Response**:

  - **Success (200 OK)**:

    ```json
    {
        "id": 1,
        "name": "Warehouse A",
        "address": "123 Main St",
        "owner": "supplier1"
    }
    ```

  - **Error (404 Not Found)**:

    ```json
    {
        "detail": "Not found."
    }
    ```

#### Update Warehouse

- **Endpoint**: `/api/warehouses/{id}/`
- **Method**: `PUT` | `PATCH`
- **Description**: Update details of a specific warehouse. Only the owner (supplier) can perform this action.
- **Authentication**: Required (Token)

- **Request Body**:

  ```json
  {
      "name": "string",
      "address": "string"
  }
  ```

- **Response**:

  - **Success (200 OK)**:

    ```json
    {
        "id": 1,
        "name": "Updated Warehouse Name",
        "address": "Updated Address",
        "owner": "supplier1"
    }
    ```

  - **Error (403 Forbidden)**:

    ```json
    {
        "detail": "You do not have permission to perform this action."
    }
    ```

#### Delete Warehouse

- **Endpoint**: `/api/warehouses/{id}/`
- **Method**: `DELETE`
- **Description**: Delete a specific warehouse. Only the owner (supplier) can perform this action.
- **Authentication**: Required (Token)

- **Response**:

  - **Success (204 No Content)**: No response body.

  - **Error (403 Forbidden)**:

    ```json
    {
        "detail": "You do not have permission to perform this action."
    }
    ```

### Products

#### Create Product

- **Endpoint**: `/api/products/`
- **Method**: `POST`
- **Description**: Create a new product. Only suppliers can perform this action.
- **Authentication**: Required (Token)

- **Request Body**:

  ```json
  {
      "name": "string",
      "description": "string",
      "price": "decimal"
  }
  ```

- **Response**:

  - **Success (201 Created)**:

    ```json
    {
        "id": 1,
        "name": "Product A",
        "description": "Description of Product A",
        "price": "99.99"
    }
    ```

  - **Error (403 Forbidden)**:

    ```json
    {
        "detail": "You do not have permission to perform this action."
    }
    ```

#### List Products

- **Endpoint**: `/api/products/`
- **Method**: `GET`
- **Description**: Retrieve a list of all products.
- **Authentication**: Required (Token)

- **Response**:

  - **Success (200 OK)**:

    ```json
    [
        {
            "id": 1,
            "name": "Product A",
            "description": "Description of Product A",
            "price": "99.99"
        },
        {
            "id": 2,
            "name": "Product B",
            "description": "Description of Product B",
            "price": "149.99"
        }
    ]
    ```

#### Retrieve Product

- **Endpoint**: `/api/products/{id}/`
- **Method**: `GET`
- **Description**: Retrieve details of a specific product by ID.
- **Authentication**: Required (Token)

- **Response**:

  - **Success (200 OK)**:

    ```json
    {
        "id": 1,
        "name": "Product A",
        "description": "Description of Product A",
        "price": "99.99"
    }
    ```

  - **Error (404 Not Found)**:

    ```json
    {
        "detail": "Not found."
    }
    ```

#### Update Product

- **Endpoint**: `/api/products/{id}/`
- **Method**: `PUT` | `PATCH`
- **Description**: Update details of a specific product. Only suppliers can perform this action.
- **Authentication**: Required (Token)

- **Request Body**:

  ```json
  {
      "name": "string",
      "description": "string",
      "price": "decimal"
  }
  ```

- **Response**:

  - **Success (200 OK)**:

    ```json
    {
        "id": 1,
        "name": "Updated Product Name",
        "description": "Updated Description",
        "price": "119.99"
    }
    ```

  - **Error (403 Forbidden)**:

    ```json
    {
        "detail": "You do not have permission to perform this action."
    }
    ```

#### Delete Product

- **Endpoint**: `/api/products/{id}/`
- **Method**: `DELETE`
- **Description**: Delete a specific product. Only suppliers can perform this action.
- **Authentication**: Required (Token)

- **Response**:

  - **Success (204 No Content)**: No response body.

  - **Error (403 Forbidden)**:

    ```json
    {
        "detail": "You do not have permission to perform this action."
    }
    ```

### Stocks

#### Supply Product

- **Endpoint**: `/api/stocks/supply/`
- **Method**: `POST`
- **Description**: Supply a specified quantity of a product to a warehouse. Only suppliers can perform this action.
- **Authentication**: Required (Token)

- **Request Body**:

  ```json
  {
      "warehouse": 1,  // Warehouse ID
      "product": 1,    // Product ID
      "quantity": 100  // Quantity to supply
  }
  ```

- **Response**:

  - **Success (200 OK)**:

    ```json
    {
        "warehouse": 1,
        "product": 1,
        "quantity": 100
    }
    ```

  - **Error (403 Forbidden)**:

    ```json
    {
        "detail": "You do not have permission to perform this action."
    }
    ```

#### Consume Product

- **Endpoint**: `/api/stocks/consume/`
- **Method**: `PUT`
- **Description**: Consume a specified quantity of a product from a warehouse. Only consumers can perform this action.
- **Authentication**: Required (Token)

- **Request Body**:

  ```json
  {
      "warehouse": 1,  // Warehouse ID
      "product": 1,    // Product ID
      "quantity": 20   // Quantity to consume
  }
  ```

- **Response**:

  - **Success (200 OK)**:

    ```json
    {
        "warehouse": 1,
        "product": 1,
        "quantity": 80  // Updated quantity after consumption
    }
    ```

  - **Error (400 Bad Request)**:

    ```json
    {
        "error": "Insufficient product quantity in the warehouse."
    }
    ```

  - **Error (403 Forbidden)**:

    ```json
    {
        "detail": "You do not have permission to perform this action."
    }
    ```

## Permissions

The application enforces role-based access control to ensure that users can only perform actions permitted by their roles.

- **Suppliers**:
  - Can create, update, and delete warehouses.
  - Can create, update, and delete products.
  - Can supply products to warehouses.

- **Consumers**:
  - Can consume products from warehouses.

Any attempt to perform unauthorized actions will result in a `403 Forbidden` response with an appropriate error message.

## Error Handling

The API provides clear and consistent error messages to help users understand and rectify issues.

- **400 Bad Request**: Returned when the request data is invalid or incomplete.

  ```json
  {
      "error": "Detailed error message."
  }
  ```

- **401 Unauthorized**: Returned when authentication credentials are missing or invalid.

  ```json
  {
      "detail": "Authentication credentials were not provided."
  }
  ```

- **403 Forbidden**: Returned when the user does not have permission to perform the action.

  ```json
  {
      "detail": "You do not have permission to perform this action."
  }
  ```

- **404 Not Found**: Returned when the requested resource does not exist.

  ```json
  {
      "detail": "Not found."
  }
  ```

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Pytest](https://docs.pytest.org/)
- [Pytest-Django](https://pytest-django.readthedocs.io/)
- [GitHub](https://github.com/)

---



To get started with **Consumer Supply**, follow the installation instructions above to set up the development environment. Once set up, you can interact with the API using tools like [Postman](https://www.postman.com/) or [cURL](https://curl.se/), or integrate it with frontend applications.
