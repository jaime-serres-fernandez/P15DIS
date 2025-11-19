# 🚀 P15 - Proyecto Libre Full-Stack: API REST + Vaadin + CI/CD
## 📚 Teoría y Conceptos Fundamentales

---

## 📋 Índice

1. **🎯 Introducción al Proyecto Libre Full-Stack**
2. **🚀 Spring Boot y APIs REST**
3. **🗄️ Persistencia con Spring Data JPA**
4. **🌐 Frontend con Vaadin 24**
5. **🐳 Contenerización con Docker & Docker Compose**
6. **🔗 Integración Frontend-Backend**
7. **🌿 GitFlow, Tests**
8. **🏆 Mejores Prácticas y Arquitectura**

---

# 1. 🎯 Introducción al Proyecto Libre Full-Stack

## ❓ ¿Qué vamos a construir?

En la **Práctica 15** desarrollarás un sistema web completo de **tema libre** (biblioteca, gimnasio, recetas, tareas, etc.) pero con un **stack técnico obligatorio**:

- **Backend**: API REST con Spring Boot 3
- **Frontend**: Interfaz Vaadin 24
- **Base de datos**: Spring Data JPA + H2/MySQL
- **Infraestructura**: Docker, GitFlow y GitHub Actions

### 🌟 Arquitectura propuesta
```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│                 │ ←──────────────→│                 │
│  Frontend Web   │                 │  Backend API    │
│   (Vaadin 24)   │                 │  (Spring Boot)  │
│                 │                 │                 │
└─────────────────┘                 └─────────────────┘
                                             │
                                             │ JPA/Hibernate
                                             ▼
                                    ┌─────────────────┐
                                    │                 │
                                    │   Base de Datos │
                                    │ (H2/MySQL/...)  │
                                    │                 │
                                    └─────────────────┘
```

### 🎯 Objetivos de aprendizaje
- Modelar un **dominio libre** con entidades y reglas de negocio claras
- Diseñar **endpoints RESTful** mantenibles
- Construir interfaces Vaadin que **consuman APIs** externas
- Automatizar la calidad mediante **tests y CI/CD**
- Contenerizar backend, frontend y base de datos con **Docker Compose**
- Gestionar el ciclo de vida del proyecto con **GitFlow**

---

# 2. 🚀 Spring Boot y APIs REST

## ⚙️ ¿Por qué Spring Boot 3?

Spring Boot simplifica la creación de servicios REST al incluir servidor embebido, configuración automática y dependencias organizadas en starters. En P15 lo usaremos para entregar un backend limpio.

### 🧱 Componentes esenciales del backend
- `@Entity`: representa el modelo principal, los datos
- `Repository` `extends JpaRepository`: operaciones CRUD
- `Service`: capa opcional para lógica de negocio y validaciones
- `@RestController`: expone endpoints bajo `/api/...`


### 🔁 Buenas prácticas REST
- Prefijo común `/api`
- Códigos HTTP coherentes (`200`, `201`, `404`, `400`, `500`)
- DTOs para exponer solo lo necesario
- Validaciones con `@Valid` y `@NotBlank`
- Paginación usando `Pageable` si manejas grandes listados

---

# 3. 🗄️ Persistencia con Spring Data JPA

## 🧩 ¿Por qué usar JPA?

JPA permite mapear nuestras entidades a tablas y simplifica el acceso a datos con repositorios declarativos. Además, Spring Data genera consultas básicas sin escribir SQL manual.


### 🧠 Consejos clave
- Define un `schema.sql` o `data.sql` inicial si necesitas datos de partida
- Configura `spring.jpa.hibernate.ddl-auto=update` en desarrollo y `validate` en producción
- Usa `@CreationTimestamp` / `@UpdateTimestamp` para auditoría
- Prefiere `Optional<T>` en servicios para indicar valores faltantes

---

# 4. 🌐 Frontend con Vaadin 24

## 🖥️ ¿Por qué Vaadin?

Vaadin 24 (LTS) permite construir interfaces modernas en Java puro: sin manejar manualmente frameworks JS, con componentes accesibles y tipados. Ideal para mantener un stack homogéneo.

### 🧱 Elementos obligatorios
- `@Route("")`: vista principal accesible en `/`
- `Grid<Item>`: muestra la colección principal
- Cliente HTTP (`RestTemplate`, `WebClient` o `HttpClient`) para consumir el backend
- Formularios o diálogos para crear/editar entidades (recomendado para nota extra)


---

# 5. 🐳 Contenerización con Docker & Docker Compose

## ✅ Requisitos mínimos en P15
- Un `Dockerfile` en `backend/` que compile el JAR y lo ejecute con Java 17
- Un `Dockerfile` en `frontend/` que genere el paquete Vaadin y lo arranque
- `docker-compose.yml` en la raíz con tres servicios: `backend`, `frontend`, `db`


---

# 6. 🔗 Integración Frontend-Backend

## 🔄 Comunicación HTTP fiable
- Define la URL del backend en una propiedad (`app.api.url`) y usa `@Value`
- Maneja errores con `try/catch` y notificaciones Vaadin (`Notification.show`)
- Refresca el `Grid` tras crear/actualizar registros
- Añade filtros Vaadin (`TextField`, `ComboBox`) para mejorar la UX

## 🔐 Seguridad y validación
- Valida los datos en el backend (Bean Validation)
- Sanitiza entradas antes de persistir
- Considera implementar DTOs específicos para minimizar exposición de campos sensibles

---

# 7. 🌿 GitFlow, Tests 

## 🪢 GitFlow obligatorio
- Inicializa con `git flow init -d`
- Trabaja sobre `develop`
- Crea al menos 2 ramas `feature/` (backend, frontend, docker, tests, etc.)
- Cierra con `release/v1.0.0` + `tag v1.0.0`
- Empuja todo con `git push --all --tags`

## 🧪 Tests backend (JUnit)
- Coloca las pruebas en `backend/src/test/java/**`
- Usa `@SpringBootTest` o pruebas unitarias de servicios/repositorios
- Ejecuta siempre `mvn test` desde `backend/`
- Aporta capturas (`evidencias/tests_ok.png`) que demuestren los tests en verde


---

# 8. 🏆 Mejores Prácticas y Arquitectura

## 🧱 Separación de responsabilidades
- **Backend**: lógica de negocio, validaciones, seguridad, exposición de APIs
- **Frontend**: UI, experiencia de usuario, consumo de datos, feedback visual



## 🐞 Debugging recomendado
- `mvn spring-boot:run -pl backend` para ver logs en vivo
- `http://localhost:8081/actuator/health` para revisar estado
- `docker compose logs -f backend` para producción local
- `vaadin-devmode` para inspeccionar componentes en el navegador

