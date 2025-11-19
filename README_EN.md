# 🚀 P15 · Free Full-Stack Project: REST API + Vaadin + Tests 

## 📋 Description

**Practice 15** consists of building a complete web system with a **free functional theme**, but with a **mandatory architecture**: REST backend with Spring Boot 3, Vaadin 24 frontend, persistence with Spring Data JPA, automated tests, and execution via Docker Compose. You'll maintain the same philosophy as previous practices, but now oriented to a project where you choose the domain.

## 🎯 Learning Objectives

- Design a **REST API** with Spring Boot 3 and Java 17+
- Persist data with **Spring Data JPA** and H2/MySQL/MariaDB
- Build a **Vaadin 24 UI** that consumes the API via HTTP
- Write **automated tests** and run them with `mvn test`
- Containerize backend, frontend, and database with **Docker Compose**
- Configure **GitFlow** and tags
- Document and demonstrate functionality through **evidence**

## 📁 Repository Content

- `P15-Teoria.md`: theoretical reference adapted to the free full-stack project
- `README.md`: this complete practice statement
- `backend/`: folder where you should have the Spring Boot project (created by you)
- `frontend/`: folder where you should have the Vaadin project (created by you)
- `docker-compose.yml`: mandatory service orchestration (created by you)
- `evidencias/`: folder for screenshots with mandatory P15 names

## 🛠️ Mandatory Technical Stack

- Java **17 or higher**
- Spring Boot **3.x**
- Spring Data JPA + **H2 or MySQL/MariaDB**
- Vaadin **24 LTS**
- Maven
- Docker & Docker Compose
- GitFlow (develop + features + release + tag)

## 🗂️ Minimum Required Structure

```
.
├── backend/             # Spring Boot project (REST API)
├── frontend/            # Vaadin 24 project
├── docker-compose.yml   # Backend + frontend + db orchestration
├── evidencias/          # Official practice screenshots
```

## GitFlow Mandatory (C0 – 1 point)

Same rules as in previous practices:
- Active `develop` branch with real commits
- Minimum **2** descriptive `feature/...` branches (backend, frontend, docker, tests, etc.)
- One `release/v1.0.0` release
- Tag `v1.0.0`
- Mandatory `git push --all --tags`

## Quick Start

1. **Read the theory** (`P15-Teoria.md`) to align the stack.
2. **Generate backend** in `backend/` with Spring Initializr (Spring Web + Data JPA + H2/MySQL).
3. **Create frontend** Vaadin 24 in `frontend/` (rest-client + Grid).
4. **Integrate REST**: `frontend` consumes `backend` via `/api/...`.
5. **Add tests** JUnit in `backend/src/test/java/**` and validate with `mvn test`.
6. **Write Dockerfiles** (`backend/Dockerfile`, `frontend/Dockerfile`) and `docker-compose.yml` with `backend`, `frontend` and `db`.
7. **Check your grade** by running `python3 grades/p15.py`.
8. **Capture evidence** official screenshots in `evidencias/`.

## Architecture 
```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│  Frontend       │ ←──────────────→│  Backend        │
│  (Vaadin 24)    │                 │  (Spring Boot)  │
└─────────────────┘                 └─────────────────┘
                                             │
                                      Spring Data JPA
                                             ▼
                                    ┌─────────────────┐
                                    │ Database        │
                                    │ H2/MySQL/Maria  │
                                    └─────────────────┘
```

## 📊 Evaluation Criteria (Rubric)

| Criterion | Points | Description |
|-----------|--------|-------------|
| **C0 – GitFlow** | 1.0 | `develop`, ≥2 `feature/`, `release/v1.0.0`, tag `v1.0.0` |
| **C1 – Backend API** | 2.0 | `backend/` with `spring-boot-starter-web`, `spring-boot-starter-data-jpa`, DB driver, `@Entity` entity, `JpaRepository` repository, REST controller `/api/...` |
| **C2 – Vaadin Frontend** | 2.0 | `frontend/` with Vaadin 24, `@Route` class, `Grid<>` showing main entity and HTTP client (`RestTemplate`, `WebClient` or similar) |
| **C3 – Backend Tests** | 2.0 | JUnit tests in `backend/src/test/java/**` + successful `mvn test` |
| **C4 – Docker** | 2.0 | `docker-compose.yml` with `backend`, `frontend`, `db` services, ≥2 Dockerfiles, `mvn test` |
| **C5 – Evidence** | 1.0 | Official screenshots in `evidencias/` with exact names |
| **Extra** | +1.5 | significant UX improvements, validations, advanced Vaadin components, clean design patterns, additional tests, extended documentation... (max. 10 pts total) |

## 📸 Required Evidence (C5 – 1 point)

Save screenshots in `evidencias/` respecting these names:

1. `ui_frontend.png` → Vaadin view with `Grid` showing real data.
2. `tests_ok.png` → Result of `mvn test` in `backend/` in green.
3. `actions_ci.png` → GitHub Actions workflow finished correctly.
4. `docker_ps.png` → Output of `docker ps` or Compose showing the 3 services.

> Upload images in PNG/JPG, ≥1 KB, and verify content is readable. Names will be automatically validated by `grades/p15.py`.

## Technical Requirements Details

### Backend (`backend/`)
- Maven + Java 17+
- Minimum dependencies: `spring-boot-starter-web`, `spring-boot-starter-data-jpa`, H2/MySQL/MariaDB driver
- At least one `@Entity` entity and its `JpaRepository` repository
- REST controller with `/api/...` prefix implementing `GET` list, `GET/{id}`, `POST` (PUT/DELETE optional but recommended)
- JUnit tests in `backend/src/test/java/**` (TDD recommended)

### Frontend (`frontend/`)
- Vaadin 24 (LTS) project
- `@Route("")` and a `Grid<YourEntityDto>` showing data
- HTTP client (RestTemplate / WebClient / HttpClient) that consumes the backend
- Property configuration to point to backend (`APP_API_URL`, etc.)

### Docker / Compose
- `backend/Dockerfile` and `frontend/Dockerfile`
- `docker-compose.yml` with `backend`, `frontend`, `db` services
- Environment variables documented in README

## 🛠️ Step-by-Step Guide

### Step 1 – Backend API
1. Generate project in `backend/` (Spring Initializr).
2. Implement main entity, repository and service.
3. Expose REST endpoints `/api/...` following good practices.
4. Add unit and integration tests (`@SpringBootTest`, `@DataJpaTest`).

### Step 2 – Vaadin Frontend
1. Create project in `frontend/` with Vaadin 24.
2. Implement DTO compatible with backend and HTTP client.
3. Build main view with `Grid`, filters and notifications.

### Step 3 – Docker + Compose
1. Write `backend/Dockerfile` (multi-stage recommended).
2. Write `frontend/Dockerfile` (build + execution).
3. Configure `docker-compose.yml` with 3 services, networks and variables.

### Step 4 – Tests + CI
1. Run `mvn test` from `backend/` until it passes without errors.
2. Configure `.github/workflows/check_p15.yml` to automate verification.
3. Run `python3 grades/p15.py` locally before uploading to see your grade. Check that the Action result in GitHub matches. If not, check what might be happening in your local repository.

### Step 5 – Evidence and submission
1. Run `docker compose up --build` and capture `docker_ps.png`.
2. Capture Vaadin UI (`ui_frontend.png`) with real data.
3. Capture tests (`tests_ok.png`) and workflow execution in GitHub Action (`actions_ci.png`).
4. Upload everything to GitHub (`git push --all --tags`) and submit ZIP in Canvas.

## 🐞 Troubleshooting

- **Vaadin doesn't load data** → Verify `APP_API_URL` and exposed ports.
- **`mvn test` fails in CI** → Check dependencies in `backend/pom.xml` and relative paths.
- **Docker doesn't start database** → Ensure `db` service exports port and uses healthchecks or `depends_on`.
- **Grader gives 0 in C5** → Check exact evidence names.

## 📚 Recommended Resources

- [Spring Boot Reference](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Vaadin 24 Docs](https://vaadin.com/docs/latest/)
- [Spring Data JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [Docker Compose](https://docs.docker.com/compose/)
- [GitFlow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)

## ✅ Final Checklist

- [ ] `backend/` and `frontend/` compiling without errors
- [ ] `mvn test` OK in `backend/` and in CI
- [ ] Dockerfiles + `docker-compose.yml` with 3 services
- [ ] Workflow `.github/workflows/check_p15.yml`
- [ ] Evidence (`ui_frontend`, `tests_ok`, `actions_ci`, `docker_ps`)
- [ ] Complete GitFlow (`develop`, `feature/*`, `release/v1.0.0`, tag `v1.0.0`)
- [ ] `grades/p15.py` generated and executed

Choose the domain that motivates you most and demonstrate your fluency with Java's typical full stack.