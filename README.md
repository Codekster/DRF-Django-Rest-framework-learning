# DRF-Django-Rest-framework-learning

## Purpose
This repository is a comprehensive learning resource for mastering Django REST Framework (DRF). It is designed and maintained by **Abhishek Pandey** to help developers and students understand, implement, and practice modern RESTful APIs using Django and DRF.

## Contents
- **DRF_Learning_Notes.md**: A book-style, in-depth guide covering all major DRF concepts, including function-based views, class-based views, generic views, mixins, concrete views, viewsets, serializers, authentication, permissions, and more. Includes practical code examples, interview prep, and best practices.
- **Projects & Examples**:
  - `functionBasedApi/`, `GenericApiView/`, `deserializer/`, `update_and_delete/`: Multiple Django projects and apps demonstrating CRUD operations, serializers, advanced update/delete logic, and DRF features in real code.
  - Each project contains models, serializers, views, migrations, and test files for hands-on learning.
- **Database & SQL**:
  - `DBMS iNDEX/`: Reference materials for MySQL indexing, triggers, stored procedures, and window functions.
- **Other Files**:
  - Example scripts (`extApp1.py`, `extApp2.py`, `hh.cpp`) and notes for broader backend and database learning.

## How to Use
1. **Read the Notes**: Start with `DRF_Learning_Notes.md` for a structured, progressive learning path.
2. **Explore the Projects**: Dive into the Django apps to see real DRF code in action. Each app is self-contained and demonstrates specific DRF features.
3. **Run and Experiment**: Use the provided `manage.py` files to run servers, test APIs, and experiment with CRUD operations.
4. **Practice Interview Prep**: Use the included interview questions and answers to prepare for technical interviews.
5. **Reference SQL Concepts**: Use the DBMS notes for database theory and practical SQL skills.

## Getting Started
- Clone the repository:
  ```bash
  git clone https://github.com/Codekster/DRF-Django-Rest-framework-learning.git
  ```
- Install dependencies for any Django project (see each project's requirements).
- Run migrations and start the development server:
  ```bash
  python manage.py migrate
  python manage.py runserver
  ```
- Test API endpoints using curl, Postman, or the browsable DRF API.

## Author
**Abhishek Pandey**

## License
This repository is for educational purposes. Please credit the author if you use or share the content.

---
Happy Learning Django REST Framework!
