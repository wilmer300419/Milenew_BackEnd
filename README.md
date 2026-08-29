# 🚀 Milenew — RESTful API

## 👥 Team Members

### 🗄️ Database Team

| Team Member                    | Email                                                           |
| ------------------------------ | --------------------------------------------------------------- |
| Wilmer Andrés Capera Hernández | [wilmerandres3004@gmail.com](mailto:wilmerandres3004@gmail.com) |
| Esteban Salvador               | [windishowlingf@gmail.com](mailto:windishowlingf@gmail.com)     |
| Héctor Fabián Ruiz Ordoñez     | [ruizfabian2003@gmail.com](mailto:ruizfabian2003@gmail.com)     |
| Sebastian Restrepo             | [bastianrtl@gmail.com](mailto:bastianrtl@gmail.com)             |

### ⚙️ BackEnd Team

| Team Member              | Email                                                       |
| ------------------------ | ----------------------------------------------------------- |
| Angel David Peña Sanchez | [superoofio60.p@gmail.com](mailto:superoofio60.p@gmail.com) |
| Pablo Rodríguez          | [huevito1009@hotmail.com](mailto:huevito1009@hotmail.com)   |
| Gylmar Rodriguez         | [gylmara1981@gmail.com](mailto:gylmara1981@gmail.com)       |
| Fray Nicolás Minganquer  | [fraynicming@gmail.com](mailto:fraynicming@gmail.com)       |

### 🎨 FrontEnd Team

| Team Member                   | Email                                                                                   |
| ----------------------------- | --------------------------------------------------------------------------------------- |
| Joan Sebastian Romaña Tavera  | [Joansebastianromanatavera@gmail.com](mailto:Joansebastianromanatavera@gmail.com)       |
| Santiago Santana              | [santiagosantananieto2@gmail.com](mailto:santiagosantananieto2@gmail.com)               |
| Juan Jose Lopez Reina         | [Juan1909070@gmail.com](mailto:Juan1909070@gmail.com)                                   |
| Daniel Chaves Muñoz           | [decosmos.dan@gmail.com](mailto:decosmos.dan@gmail.com)                                 |
| Andres Felipe Dueñas Martinez | [andresfelipeduenasmartinez10@gmail.com](mailto:andresfelipeduenasmartinez10@gmail.com) |

---

# 📌 Project Description

Milenew is a web application developed using a decoupled architecture, separating the FrontEnd, BackEnd, and Database into independent components.

The project is designed to allow each development team to work independently while maintaining clear communication and integration between all system components.

The application will mainly be divided into three layers:

```text
┌─────────────────────────────┐
│          FRONTEND           │
│      React + JavaScript     │
└──────────────┬──────────────┘
               │
               │ HTTP / JSON
               ▼
┌─────────────────────────────┐
│           BACKEND           │
│       Python + Flask        │
│          REST API           │
└──────────────┬──────────────┘
               │
               │ SQL / Stored Procedures
               ▼
┌─────────────────────────────┐
│          DATABASE           │
│         PostgreSQL          │
└─────────────────────────────┘
```

The FrontEnd will be responsible for providing the graphical interface and user interaction.

The BackEnd will act as an intermediary between the FrontEnd and the database by exposing a **RESTful API** through HTTP endpoints.

The database will be managed independently using **PostgreSQL**, including the development of stored procedures for specific database operations and data-related logic.

Communication between the FrontEnd and BackEnd will primarily use **JSON**, allowing both components to work independently as long as they comply with the API contract.

---

# 🏗️ Project Architecture

The architecture is designed to maintain a clear separation of responsibilities between the different components.

## 🎨 FrontEnd

Technologies:

* React
* JavaScript

The FrontEnd will be responsible for:

* Providing the graphical user interface.
* Capturing information entered by users.
* Performing basic client-side validation.
* Consuming API endpoints.
* Processing JSON responses.
* Displaying success and error messages.
* Managing the application's visual components.

The FrontEnd **will not have direct access to PostgreSQL**.

All database-related communication must be performed through the BackEnd API.

---

## ⚙️ BackEnd

Technologies:

* Python
* Flask
* Pytest

The BackEnd will act as the layer responsible for processing requests received from the FrontEnd.

Its responsibilities include:

* Creating REST endpoints.
* Receiving HTTP requests.
* Validating incoming data.
* Processing business logic.
* Communicating with PostgreSQL.
* Executing SQL queries or stored procedures.
* Building API responses.
* Returning information using JSON.
* Handling errors.
* Performing automated tests using Pytest.

Example communication flow:

```text
React
   │
   │ POST /api/products
   │
   ▼
Flask
   │
   │ Validation
   │ Business Logic
   │
   ▼
PostgreSQL
   │
   │ Stored Procedure
   │
   ▼
Flask
   │
   │ JSON Response
   ▼
React
```

---

# 🗄️ Database

Main technology:

* PostgreSQL

The Database Team will be responsible for designing, implementing, and maintaining the database structure.

Their responsibilities include:

* Database modeling.
* Table creation.
* Primary key definition.
* Foreign key definition.
* Data integrity constraints.
* Relationships between entities.
* Indexes when necessary.
* SQL queries.
* Stored procedures.
* Transactions when required.
* Database creation and configuration scripts.

The database will remain decoupled from the FrontEnd.

Access to PostgreSQL will be handled exclusively through the BackEnd.

---

# 🔄 Communication Between Components

One of the main principles of this project is the separation between the different components.

## General Flow

```text
User
   │
   ▼
React
   │
   │ HTTP
   ▼
Flask API
   │
   │ SQL / Stored Procedure
   ▼
PostgreSQL
   │
   │ Result
   ▼
Flask API
   │
   │ JSON
   ▼
React
   │
   ▼
User
```

For example, when a user registers information:

1. The user fills out a form in React.
2. React performs basic validation.
3. React creates an HTTP request.
4. The request is sent to a Flask endpoint.
5. Flask receives and validates the information.
6. Flask executes the required business logic.
7. Flask communicates with PostgreSQL.
8. PostgreSQL performs the required operation.
9. PostgreSQL returns the result.
10. Flask builds a JSON response.
11. React receives the response.
12. React updates the user interface.

---

# 🌐 RESTful API

Communication between the FrontEnd and BackEnd will use a RESTful API.

Resources will be manipulated using the corresponding HTTP methods.

| HTTP Method | Purpose                      |
| ----------- | ---------------------------- |
| GET         | Retrieve information         |
| POST        | Create information           |
| PUT         | Update information           |
| PATCH       | Partially update information |
| DELETE      | Delete information           |

Example:

```http
GET /api/products
```

Response:

```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Product 1",
            "price": 25000
        }
    ]
}
```

The final endpoint structure and response formats must be agreed upon by the FrontEnd and BackEnd teams.

This will establish a clear **API communication contract**, preventing one team from developing based on assumptions that differ from the actual implementation.

---

# 📦 JSON Format

JSON will be the primary format used to exchange information between the FrontEnd and BackEnd.

Example request:

```json
{
    "name": "Product",
    "price": 25000,
    "quantity": 10
}
```

Example response:

```json
{
    "success": true,
    "message": "Product created successfully",
    "data": {
        "id": 1,
        "name": "Product",
        "price": 25000,
        "quantity": 10
    }
}
```

A consistent response structure is recommended to simplify API consumption on the FrontEnd.

---

# 🧪 Testing

The BackEnd will use **Pytest** for automated testing.

Testing will allow the team to verify that the different components of the application work correctly.

Tests may cover:

* API endpoints.
* Input validation.
* HTTP responses.
* Business logic.
* Successful operations.
* Error cases.
* Invalid data.
* CRUD operations.

Example conceptual flow:

```text
Request
   │
   ▼
Endpoint
   │
   ▼
Validation
   │
   ▼
Business Logic
   │
   ▼
Expected Result
```

Before integrating important changes into the main development branches, the corresponding tests should be executed.

---

# 👨‍💻 Development Methodology

The project will use **Scrum** as its agile development methodology.

The work will be divided into small tasks that can be planned, developed, reviewed, tested, and delivered progressively.

## 📋 Jira

**Jira** will be used to manage and track the team's work.

Tasks may be organized using:

* Epics.
* User stories.
* Technical tasks.
* Bugs.
* Subtasks.

Recommended workflow:

```text
BACKLOG
   │
   ▼
TO DO
   │
   ▼
IN PROGRESS
   │
   ▼
IN REVIEW
   │
   ▼
IN TESTING
   │
   ▼
DONE
```

Each task should clearly specify:

* What needs to be implemented.
* Assigned developer.
* Priority.
* Acceptance criteria.
* Current status.
* Associated sprint.

---

# 🌿 GitFlow

The project will use **GitFlow** as the version control workflow.

GitFlow provides a structured branching strategy that allows multiple developers and teams to work simultaneously without directly modifying the stable version of the project.

The proposed branch structure is:

```text
main
  │
  └── develop
        │
        ├── feature/frontend-login
        ├── feature/backend-products
        ├── feature/database-products
        │
        └── ...
```

---

## 🔵 `main`

The `main` branch will contain the **stable versions** of the project.

Developers should not work directly on this branch.

Changes should reach `main` through a controlled integration and review process.

The `main` branch represents a version that is considered stable and potentially ready for deployment or delivery.

---

## 🟢 `develop`

The `develop` branch will be the main integration branch during development.

Completed and reviewed features will be integrated into this branch.

```text
main
 │
 └── develop
```

Developers should create their feature branches from `develop`.

---

# 🔨 Feature Branches

`feature` branches will be used to develop specific functionalities.

Examples:

```text
feature/login
feature/user-registration
feature/products-api
feature/products-ui
feature/database-products
```

Branch names should be descriptive and related to the functionality being developed.

Example:

```bash
git checkout develop
git pull origin develop

git checkout -b feature/products-api
```

After implementing the functionality:

```bash
git add .
git commit -m "feat: create product endpoints"
```

Then push the branch:

```bash
git push -u origin feature/products-api
```

Finally, a **Pull Request** should be created to merge the feature into `develop`.

---

# 🔀 Pull Requests

A Pull Request will be used to request the integration of a feature branch into `develop`.

The workflow is:

```text
feature
   │
   │ Push
   ▼
GitHub
   │
   │ Pull Request
   ▼
develop
```

Before approving a Pull Request, the following should be verified:

* The code runs correctly.
* Tests pass.
* There are no known errors.
* The project structure is respected.
* The changes correspond to the assigned task.
* Unnecessary changes have not been introduced.
* Another team member has reviewed the code.

---

# 🧪 Complete GitFlow Process

The recommended process for every feature is the following.

## 1. Update `develop`

Before starting a new feature, make sure the local `develop` branch is up to date.

```bash
git checkout develop
git pull origin develop
```

This reduces the possibility of working with outdated code.

---

## 2. Create a Feature Branch

Create a new branch from `develop`.

```bash
git checkout -b feature/feature-name
```

For example:

```bash
git checkout -b feature/products-api
```

---

## 3. Develop the Feature

The developer implements only the functionality assigned to the Jira task.

Changes should remain focused on the corresponding feature.

---

## 4. Create Commits

Commits should be small, meaningful, and related to a specific change.

Example:

```bash
git add .
git commit -m "feat: implement product creation endpoint"
```

---

## 5. Push the Branch

Upload the branch to the remote repository:

```bash
git push -u origin feature/products-api
```

---

## 6. Create a Pull Request

Create a Pull Request from:

```text
feature/products-api
```

to:

```text
develop
```

The Pull Request should contain a clear description of:

* What was implemented.
* Which Jira task it addresses.
* Important technical changes.
* Tests performed.
* Any considerations for reviewers.

---

## 7. Code Review

Another team member should review the Pull Request.

The reviewer should check:

* Code quality.
* Project architecture.
* Naming conventions.
* Potential bugs.
* Security considerations.
* Test coverage.
* Compliance with the Jira requirements.

If changes are required, the developer should make the corrections in the same feature branch.

---

## 8. Run Tests

Before merging the Pull Request, the required tests should be executed.

For the BackEnd:

```bash
pytest -v
```

The feature should not be integrated if the relevant tests are failing.

---

## 9. Merge into `develop`

Once the Pull Request has been reviewed and approved:

```text
feature
   ↓
develop
```

The feature becomes part of the development version of the application.

---

## 10. Integration Testing

Once multiple features have been merged into `develop`, integration tests should verify that the FrontEnd, BackEnd, and Database work correctly together.

For example:

```text
React
  ↓
Flask API
  ↓
PostgreSQL
  ↓
Flask API
  ↓
React
```

This is particularly important because the project is developed using a decoupled architecture.

---

## 11. Release to `main`

When the required functionality for a stable version has been completed and tested:

```text
develop
   ↓
Stable Version
   ↓
main
```

The `main` branch should only contain versions that have passed the required validation process.

---

# 🏷️ Commit Convention

The project recommends using a commit convention based on **Conventional Commits**.

## New Features

```bash
git commit -m "feat: add product endpoint"
```

## Bug Fixes

```bash
git commit -m "fix: correct product validation"
```

## Documentation

```bash
git commit -m "docs: update README"
```

## Tests

```bash
git commit -m "test: add product endpoint tests"
```

## Refactoring

```bash
git commit -m "refactor: reorganize backend services"
```

## Configuration

```bash
git commit -m "chore: update dependencies"
```

---

# 🚨 Git Rules

To reduce conflicts and development problems, the following rules should be followed:

1. Do not work directly on `main`.
2. Avoid working directly on `develop`.
3. Every feature should have its own branch.
4. Update `develop` before creating a new feature branch.
5. Create small and descriptive commits.
6. Do not commit sensitive information.
7. Do not commit passwords.
8. Do not commit `.env` files.
9. Review changes before pushing them.
10. Use Pull Requests to integrate features.
11. Resolve merge conflicts before requesting final approval.
12. Run tests before merging changes.
13. Keep branches focused on a single feature or task.
14. Do not mix unrelated changes in the same Pull Request.

---

# 🔐 Environment Variables

Sensitive credentials and configuration values must not be stored directly in the source code.

An `.env` file should be used to store configuration such as:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=database_name
DATABASE_USER=database_user
DATABASE_PASSWORD=database_password
```

The `.env` file must be included in `.gitignore`.

Example:

```gitignore
.env
__pycache__/
*.pyc
venv/
node_modules/
```

An `.env.example` file should be included in the repository.

Example:

```env
DATABASE_HOST=
DATABASE_PORT=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
```

This allows developers to know which environment variables are required without exposing sensitive information.

---

# 📁 Proposed Project Structure

The project may be organized as follows:

```text
project/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── ...
│
├── database/
│   ├── tables/
│   ├── procedures/
│   ├── functions/
│   └── scripts/
│
├── docs/
│
├── .gitignore
├── .env.example
└── README.md
```

The final structure may be modified according to the project's requirements.

---

# 🚀 Installation and Execution

## Requirements

Before running the project, the following software must be installed:

* Python
* Node.js
* npm
* PostgreSQL
* Git

---

# 📥 Clone the Repository

```bash
git clone REPOSITORY_URL
cd project-name
```

---

# ⚙️ Run the BackEnd

Navigate to the BackEnd directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Flask application:

```bash
flask run
```

---

# 🎨 Run the FrontEnd

Navigate to the FrontEnd directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

---

# 🗄️ PostgreSQL Configuration

The database setup should follow these steps:

1. Create the PostgreSQL database.
2. Execute the table creation scripts.
3. Create the required relationships.
4. Create stored procedures and functions.
5. Configure the environment variables.
6. Verify the connection between the BackEnd and PostgreSQL.
7. Insert the required initial data, if applicable.

---

# 🧪 Run Tests

From the BackEnd directory:

```bash
pytest
```

For detailed test output:

```bash
pytest -v
```

---

# 📖 Documentation

The project documentation may include:

* Software requirements.
* User stories.
* Entity-Relationship Diagram.
* Relational model.
* API documentation.
* Data dictionary.
* Stored procedures.
* Test cases.
* Installation guide.
* User manual.
* Development evidence.

---

# 🔗 Contract Between Teams

Because the project uses a decoupled architecture, communication between teams is essential.

## FrontEnd ↔ BackEnd

Before implementing a feature, both teams should agree on:

* Endpoint.
* HTTP method.
* Parameters.
* Request JSON structure.
* Response JSON structure.
* HTTP status codes.
* Error messages.
* Validation rules.

Example:

```text
POST /api/products
```

Request:

```json
{
    "name": "Laptop",
    "price": 2500000
}
```

Response:

```json
{
    "success": true,
    "message": "Product created successfully",
    "data": {
        "id": 1,
        "name": "Laptop",
        "price": 2500000
    }
}
```

This allows the FrontEnd team to develop against a clearly defined contract while the BackEnd team implements the internal logic required to fulfill that contract.

---

# 🔄 Team Integration

The project requires coordination between all three teams.

A complete feature may follow this workflow:

```text
              ┌───────────────────┐
              │    Jira Story     │
              └─────────┬─────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
      Database       BackEnd       FrontEnd
          │             │             │
          ▼             ▼             ▼
       Tables        Endpoints         UI
          │        Procedures          │
          │             │              │
          └─────────────┼──────────────┘
                        ▼
                    Integration
                        │
                        ▼
                      Tests
                        │
                        ▼
                   Pull Request
                        │
                        ▼
                     develop
                        │
                        ▼
                      main
```

This allows each team to have clearly defined responsibilities while maintaining the overall integration of the application.

---

# 🎯 Project Objectives

The main objectives of the project are:

* Develop a functional web application.
* Implement a decoupled architecture.
* Develop a RESTful API using Flask.
* Implement a user interface using React.
* Use PostgreSQL as the database management system.
* Implement stored procedures.
* Use JSON as the communication format.
* Implement automated tests using Pytest.
* Use Scrum as the development methodology.
* Manage tasks using Jira.
* Use GitFlow for version control.
* Maintain a clear separation of responsibilities between FrontEnd, BackEnd, and Database teams.

---

# 📌 Best Practices

During development, the following practices are recommended:

* Keep the code organized.
* Use descriptive names.
* Avoid code duplication.
* Document important functionality.
* Keep dependencies updated.
* Create tests for critical functionality.
* Keep commits related to a single task.
* Review code through Pull Requests.
* Keep branches synchronized.
* Never store credentials in Git.
* Keep the README and technical documentation updated.
* Maintain a clear API contract between FrontEnd and BackEnd.
* Keep database scripts version-controlled.

---

# 🏁 Final Development Workflow

The complete development process can be summarized as follows:

```text
                 ┌───────────────┐
                 │     SCRUM     │
                 │     JIRA      │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │      TASK     │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │    develop    │
                 └───────┬───────┘
                         │
                         ▼
                ┌─────────────────┐
                │     feature     │
                └────────┬────────┘
                         │
                     Development
                         │
                         ▼
                ┌─────────────────┐
                │     Commit      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │      Push       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Pull Request   │
                └────────┬────────┘
                         │
                    Code Review
                         │
                         ▼
                ┌─────────────────┐
                │      Tests      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │     develop     │
                └────────┬────────┘
                         │
                  Integration Tests
                         │
                         ▼
                ┌─────────────────┐
                │ Stable Version  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │      main       │
                └─────────────────┘
```

## 🔎 Why Is This Workflow Important?

The objective is not simply to use Git because it is a version control tool. The purpose is to establish a controlled development process capable of supporting a team of 13 developers working simultaneously.

For example, if a BackEnd developer is implementing the products endpoint, they should not modify `main` directly.

Instead, they should work on:

```text
feature/backend-products
```

At the same time, a FrontEnd developer can work on:

```text
feature/frontend-products
```

And the Database Team can work on:

```text
feature/database-products
```

Each team can therefore work independently.

When a feature is completed, it is submitted through a Pull Request.

The complete flow is:

```text
Jira
  ↓
Feature Branch
  ↓
Development
  ↓
Commit
  ↓
Push
  ↓
Pull Request
  ↓
Code Review
  ↓
Automated Tests
  ↓
Integration
  ↓
develop
  ↓
Integration Testing
  ↓
Stable Release
  ↓
main
```

This process helps maintain `main` as a stable branch while `develop` acts as the main integration point for the work performed by the different teams.

---

# 👨‍👩‍👧‍👦 Team Organization

The project is divided into three main areas:

```text
                    PROJECT
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    FRONTEND        BACKEND       DATABASE
        │              │              │
      React          Flask        PostgreSQL
    JavaScript       Python       Procedures
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
                  INTEGRATION
                       │
                       ▼
                    SYSTEM
```

Each team can work relatively independently, but all features must eventually be integrated through the defined communication contract, Jira workflow, GitFlow process, and testing strategy.

---

# 📄 Project Status

> 🚧 **Project under development**

The functionality, API structure, database model, and FrontEnd components may change as development progresses and new requirements are defined.
