<div id="top-header" style="with:100%;height:auto;text-align:right;">
    <img src="./public/files/pr-banner-long.png">
</div>

# SOCIAL FEED - DJANGO 4.2

This repository contains a basic example of a RESTful API service built with **Laravel 12**, intended for research purposes and as a demonstration of my developer profile. It implements the core features of a minimal, custom social feed application and serves as a reference project for learning, experimentation, or as a back-end development code sample.

> ⚠️ **Project Status: In Development**
>
> This repository is currently under active development and not yet ready for use. Features and APIs may change, and breaking changes can occur. Please, be aware that the codebase is actively evolving.

## Project Overview

The API supports a registry of platform "members," enabling users to create posts and voting with like or dislike other users' posts. An administrator role is provided for managing users, content, and platform statistics via a dedicated back office.

## Content of this page:

- [REST API Features](#apirest-features)
- [Infrastructure Platform](#infrastructure-platform)
- [REST API - Development](#apirest-development)
<br><br>

## <a id="apirest-features"></a>REST API Features

- **RESTful API** — Follows common REST patterns for resource-oriented endpoints.
- **Stateless API** — Each request is self-contained, adhering to REST principles.
- **Domain-Driven Design** — Each domain is self-contained in a single directory, except for resources specific to the framework.
- **JWT Role-Based Access** — Authentication and authorization flows support both regular users and administrators, using JWTs with role-based access control.
- **User Registration and Login** — Secure registration and login for members with JWT-based authentication.
- **CRUD Operations** — Users can create, update, and delete their own content.
- **SOLID Principles** — Applies best practices in code structure, validation, error handling, and response formats.
- **Member and Admin Endpoints** — Dedicated endpoints for user/content management, statistics, and moderation tools.
- **Comprehensive API Error Handling** — Standardized, consistent responses for errors and validation.
- **Integration Testing & Static Analysis** — Includes scripts and tools for automated endpoint testing and static code analysis to ensure quality.
- **OpenAPI/Swagger Documentation** — Interactive API documentation generated from code annotations, accessible via a web interface.

#### Tech Stack

- **Framework:** [Django](https://www.djangoproject.com/) / [Django REST Framework](https://www.django-rest-framework.org/)
- **Database:** [PostgreSQL 16.4](https://www.postgresql.org/)
<br><br>

> **Note**: This project is intended for educational and evaluation purposes only. It is not production-ready, but can be extended for more complex scenarios. Contributions and suggestions are welcome!

> **Convention:** `$` at the start of a line means "run this command in your shell."

<br>


## <a id="infrastructure-platform"></a>Infrastructure Platform

You can use your own local infrastructure to clone and run this repository. However, if you use [GNU Make](https://www.gnu.org/software/make/) installed, we recommend using the dedicated Docker repository [**NGINX 1.28, PYTHON 3.12 - POSTGRES 16.4**](https://github.com/pabloripoll/docker-platform-nginx-python-3.12-pgsql-16.4)

With just a few configuration steps, you can quickly set up this project—or any other—with this same required stack.

**Repository directories structure overview:**
```
.
├── apirest (Django)
│   ├── api
│   ├── app
│   ├── venv
│   └── ...
│
├── platform
│   ├── nginx-python3.12
│   │   ├── docker
│   │   │   ├── config
│   │   │   │   ├── python
│   │   │   │   ├── nginx
│   │   │   │   └── supervisor
│   │   │   ├── .env
│   │   │   ├── docker-compose.yml
│   │   │   └── Dockerfile
│   │   │
│   │   └── Makefile
│   └── postgres-16.4
│       ├── docker
│       └── Makefile
├── .env
├── Makefile
└── README.md
```

Follow the documentation to implement it:
- https://github.com/pabloripoll/docker-platform-nginx-python-3.12-pgsql-16.4?tab=readme-ov-file#platform--usage
<br><br>


## <a id="apirest-development"></a>REST API - Development

### Start up the project

```bash
$ make apirest-ssh
/var/www $ python3 setup_env.py
/var/www $ sudo supervisorctl restart django
```

`./platform/nginx-python-3.12/docker/config/supervisor/conf.d/django.conf`
```bash
[program:django]
command=/var/www/venv/bin/gunicorn app.wsgi:application --chdir /var/www --bind 0.0.0.0:8080 --workers 3 --timeout 120
directory=/var/www
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
autorestart=false
startretries=0
```
<br>

### Migrations

Notes about migrations and existing SQL

Option A (recommended if you want Django to manage schema):

- Add each domain package to INSTALLED_APPS or register an app (e.g., "apirest.api") that contains these models.
- python manage.py makemigrations
- python manage.py migrate This will create migration files automatically from these models.

Option B (you already have SQL and want to keep using it):

- Create a migration that runs your SQL directly using migrations.RunSQL. Example migration file:
<br><br>

### Controller

```py
from api.domain.user.models.user import User
from api.domain.member.models.member import Member

# using user pk
members_qs = Member.objects.filter(user_id=123)

# or with a User instance
user = User.objects.get(pk=123)
members_qs = user.members.all()

# iterate
for m in members_qs:
    print(m.uid, m.is_active)
```

How to get a **User**

- If you have a **User** instance: use the reverse accessor created by related_name: user.members.all()
- If you only have a user primary-key (integer): query **Member** directly: Member.objects.filter(user_id=123)

Notes and details

- With your current model (field name is user_id)
- The attribute member.user_id returns the related User instance.
- The raw integer PK for that relation is available as `member.user_id_id`.
    - To get all **Member** rows for user id 123:
    - Member.objects.filter(user_id=123) # Django accepts an int for an FK lookup or user = User.objects.get(pk=123); user.members.all() # uses related_name="members"