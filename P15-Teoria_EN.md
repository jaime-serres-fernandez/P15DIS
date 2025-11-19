# 🚀 P15 - Free Full-Stack Project: REST API + Vaadin + CI/CD
## 📚 Theory and Fundamental Concepts

---

## 📋 Index

1. **🎯 Introduction to Free Full-Stack Project**
2. **🚀 Spring Boot and REST APIs**
3. **🗄️ Persistence with Spring Data JPA**
4. **🌐 Frontend with Vaadin 24**
5. **🐳 Containerization with Docker & Docker Compose**
6. **🔗 Frontend-Backend Integration**
7. **🌿 GitFlow, Tests**
8. **🏆 Best Practices and Architecture**

---

# 1. 🎯 Introduction to Free Full-Stack Project

## ❓ What are we going to build?

In **Practice 15** you will develop a complete web system with a **free theme** (library, gym, recipes, tasks, etc.) but with a **mandatory technical stack**:

- **Backend**: REST API with Spring Boot 3
- **Frontend**: Vaadin 24 interface
- **Database**: Spring Data JPA + H2/MySQL
- **Infrastructure**: Docker, GitFlow and GitHub Actions

### 🌟 Proposed Architecture
```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│                 │ ←──────────────→│                 │
│  Web Frontend   │                 │  Backend API    │
│   (Vaadin 24)   │                 │  (Spring Boot)  │
│                 │                 │                 │
└─────────────────┘                 └─────────────────┘
                                             │
                                             │ JPA/Hibernate
                                             ▼
                                    ┌─────────────────┐
                                    │                 │
                                    │    Database     │
                                    │ (H2/MySQL/...)  │
                                    │                 │
                                    └─────────────────┘
```

### 🎯 Learning Objectives
- Model a **free domain** with clear entities and business rules
- Design maintainable **RESTful endpoints**
- Build Vaadin interfaces that **consume external APIs**
- Automate quality through **tests and CI/CD**
- Containerize backend, frontend and database with **Docker Compose**
- Manage project lifecycle with **GitFlow**

---

# 2. 🚀 Spring Boot and REST APIs

## ⚙️ Why Spring Boot 3?

Spring Boot simplifies the creation of REST services by including an embedded server, automatic configuration, and dependencies organized in starters. In P15 we'll use it to deliver a clean backend.

### 🧱 Essential backend components
- `@Entity`: represents the main model, the data
- `Repository` `extends JpaRepository`: CRUD operations
- `Service`: optional layer for business logic and validations
- `@RestController`: exposes endpoints under `/api/...`

### 🔁 REST Best Practices
- Common prefix `/api`
- Consistent HTTP codes (`200`, `201`, `404`, `400`, `500`)
- DTOs to expose only what's necessary
- Validations with `@Valid` and `@NotBlank`
- Pagination using `Pageable` if handling large listings

---

# 3. 🗄️ Persistence with Spring Data JPA

## 🧩 Why use JPA?

JPA allows mapping our entities to tables and simplifies data access with declarative repositories. Additionally, Spring Data generates basic queries without writing manual SQL.

### 🧠 Key Tips
- Define an initial `schema.sql` or `data.sql` if you need starting data
- Configure `spring.jpa.hibernate.ddl-auto=update` in development and `validate` in production
- Use `@CreationTimestamp` / `@UpdateTimestamp` for auditing
- Prefer `Optional<T>` in services to indicate missing values

---

# 4. 🌐 Frontend with Vaadin 24

## 🖥️ Why Vaadin?

Vaadin 24 (LTS) allows building modern interfaces in pure Java: without manually handling JS frameworks, with accessible and typed components. Ideal for maintaining a homogeneous stack.

### 🧱 Mandatory Elements
- `@Route("")`: main view accessible at `/`
- `Grid<Item>`: displays the main collection
- HTTP client (`RestTemplate`, `WebClient` or `HttpClient`) to consume the backend
- Forms or dialogs to create/edit entities (recommended for extra points)

---

# 5. 🐳 Containerization with Docker & Docker Compose

## ✅ Minimum requirements in P15
- A `Dockerfile` in `backend/` that compiles the JAR and runs it with Java 17
- A `Dockerfile` in `frontend/` that generates the Vaadin package and starts it
- `docker-compose.yml` in the root with three services: `backend`, `frontend`, `db`

---

# 6. 🔗 Frontend-Backend Integration

## 🔄 Reliable HTTP Communication
- Define the backend URL in a property (`app.api.url`) and use `@Value`
- Handle errors with `try/catch` and Vaadin notifications (`Notification.show`)
- Refresh the `Grid` after creating/updating records
- Add Vaadin filters (`TextField`, `ComboBox`) to improve UX

## 🔐 Security and Validation
- Validate data in the backend (Bean Validation)
- Sanitize inputs before persisting
- Consider implementing specific DTOs to minimize exposure of sensitive fields

---

# 7. 🌿 GitFlow, Tests 

## 🪢 Mandatory GitFlow
- Initialize with `git flow init -d`
- Work on `develop`
- Create at least 2 `feature/` branches (backend, frontend, docker, tests, etc.)
- Close with `release/v1.0.0` + `tag v1.0.0`
- Push everything with `git push --all --tags`

## 🧪 Backend Tests (JUnit)
- Place tests in `backend/src/test/java/**`
- Use `@SpringBootTest` or unit tests for services/repositories
- Always run `mvn test` from `backend/`
- Provide screenshots (`evidencias/tests_ok.png`) that demonstrate tests in green

---

# 8. 🏆 Best Practices and Architecture

## 🧱 Separation of Concerns
- **Backend**: business logic, validations, security, API exposure
- **Frontend**: UI, user experience, data consumption, visual feedback

## 🐞 Recommended Debugging
- `mvn spring-boot:run -pl backend` to see live logs
- `http://localhost:8081/actuator/health` to check status
- `docker compose logs -f backend` for local production
- `vaadin-devmode` to inspect components in the browser