# 🚀 P15 · Proyecto Libre Full-Stack: API REST + Vaadin + Tests 

## 📋 Descripción

La **Práctica 15** consiste en construir un sistema web completo de **tema funcional libre**, pero con una **arquitectura obligatoria**: backend REST con Spring Boot 3, frontend Vaadin 24, persistencia con Spring Data JPA, tests automatizados y ejecución mediante Docker Compose. Mantendrás la misma filosofía de las prácticas anteriores, pero ahora orientada a un proyecto donde el dominio lo eliges tú.

## 🎯 Objetivos de Aprendizaje

- Diseñar una **API REST** con Spring Boot 3 y Java 17+
- Persistir datos con **Spring Data JPA** y H2/MySQL/MariaDB
- Construir una **UI Vaadin 24** que consuma la API vía HTTP
- Escribir **tests automatizados** y ejecutarlos con `mvn test`
- Contenerizar backend, frontend y base de datos con **Docker Compose**
- Configurar **GitFlow** y tags
- Documentar y demostrar el funcionamiento mediante **evidencias**

## 📁 Contenido del Repositorio

- `P15-Teoria.md`: referencia teórica adaptada al proyecto libre full-stack
- `README.md`: este enunciado completo de la práctica
- `backend/`: carpeta donde debes tener el proyecto Spring Boot (creada por ti)
- `frontend/`: carpeta donde debes tener el proyecto Vaadin (creada por ti)
- `docker-compose.yml`: orquestación de servicios obligatoria (creado por ti)
- `evidencias/`: carpeta para capturas con nombres obligatorios de P15


## 🛠️ Stack Técnico Obligatorio

- Java **17 o superior**
- Spring Boot **3.x**
- Spring Data JPA + **H2 o MySQL/MariaDB**
- Vaadin **24 LTS**
- Maven
- Docker & Docker Compose
- GitFlow (develop + features + release + tag)


## 🗂️ Estructura mínima requerida

```
.
├── backend/             # Proyecto Spring Boot (API REST)
├── frontend/            # Proyecto Vaadin 24
├── docker-compose.yml   # Orquestación backend + frontend + db
├── evidencias/          # Capturas oficiales de la práctica

```

## GitFlow Obligatorio (C0 – 1 punto)

Mismas reglas que en las prácticas previas:
- Rama `develop` activa con commits reales
- Mínimo **2** ramas `feature/...` descriptivas (backend, frontend, docker, tests, etc.)
- Una release `release/v1.0.0`
- Tag `v1.0.0`
- `git push --all --tags` obligatorio



## Inicio Rápido

1. **Lee la teoría** (`P15-Teoria.md`) para alinear el stack.
2. **Genera backend** en `backend/` con Spring Initializr (Spring Web + Data JPA + H2/MySQL).
3. **Crea frontend** Vaadin 24 en `frontend/` (rest-client + Grid).
4. **Integra REST**: `frontend` consume `backend` vía `/api/...`.
5. **Añade tests** JUnit en `backend/src/test/java/**` y valida con `mvn test`.
6. **Escribe Dockerfiles** (`backend/Dockerfile`, `frontend/Dockerfile`) y `docker-compose.yml` con `backend`, `frontend` y `db`.
7. **Chequea tu nota** ejecutando `python3 grades/p15.py`.
8. **Captura evidencias** oficiales en `evidencias/`.

##  Arquitectura 
```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│  Frontend       │ ←──────────────→│  Backend        │
│  (Vaadin 24)    │                 │  (Spring Boot)  │
└─────────────────┘                 └─────────────────┘
                                             │
                                      Spring Data JPA
                                             ▼
                                    ┌─────────────────┐
                                    │ Base de datos   │
                                    │ H2/MySQL/Maria  │
                                    └─────────────────┘
```

## 📊 Criterios de Evaluación (Rúbrica)

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| **C0 – GitFlow** | 1.0 | `develop`, ≥2 `feature/`, `release/v1.0.0`, tag `v1.0.0` |
| **C1 – Backend API** | 2.0 | `backend/` con `spring-boot-starter-web`, `spring-boot-starter-data-jpa`, driver BD, entidad `@Entity`, repositorio `JpaRepository`, controlador REST `/api/...` |
| **C2 – Frontend Vaadin** | 2.0 | `frontend/` con Vaadin 24, clase `@Route`, `Grid<>` mostrando entidad principal y cliente HTTP (`RestTemplate`, `WebClient` o similar) |
| **C3 – Tests backend** | 2.0 | Tests JUnit en `backend/src/test/java/**` + `mvn test` exitoso |
| **C4 – Docker** | 2.0 | `docker-compose.yml` con servicios `backend`, `frontend`, `db`, ≥2 Dockerfiles, `mvn test` |
| **C5 – Evidencias** | 1.0 | Capturas oficiales en `evidencias/` con nombres exactos |
| **Extra** | +1.5 | mejoras significativas en UX, validaciones, componentes Vaadin avanzados, patrones de diseño limpios, pruebas adicionales, documentación ampliada… (máx. 10 pts totales) |

## 📸 Evidencias Requeridas (C5 – 1 punto)

Guarda las capturas en `evidencias/` respetando estos nombres:

1. `ui_frontend.png` → Vista Vaadin con el `Grid` mostrando datos reales.
2. `tests_ok.png` → Resultado de `mvn test` en `backend/` en verde.
3. `actions_ci.png` → Workflow de GitHub Actions finalizado correctamente.
4. `docker_ps.png` → Salida de `docker ps` o Compose mostrando los 3 servicios.

> Sube las imágenes en PNG/JPG, ≥1 KB, y verifica que el contenido es legible. Los nombres serán validados automáticamente por `grades/p15.py`.

##  Requisitos Técnicos Detallados

### Backend (`backend/`)
- Maven + Java 17+
- Dependencias mínimas: `spring-boot-starter-web`, `spring-boot-starter-data-jpa`, driver H2/MySQL/MariaDB
- Al menos una entidad `@Entity` y su repositorio `JpaRepository`
- Controlador REST con prefijo `/api/...` implementando `GET` lista, `GET/{id}`, `POST` (PUT/DELETE opcionales pero recomendados)
- Tests JUnit en `backend/src/test/java/**` (TDD recomendado)

### Frontend (`frontend/`)
- Proyecto Vaadin 24 (LTS)
- `@Route("")` y un `Grid<YourEntityDto>` mostrando datos
- Cliente HTTP (RestTemplate / WebClient / HttpClient) que consuma el backend
- Configuración de propiedades para apuntar al backend (`APP_API_URL`, etc.)

### Docker / Compose
- `backend/Dockerfile` y `frontend/Dockerfile`
- `docker-compose.yml` con servicios `backend`, `frontend`, `db`
- Variables de entorno documentadas en el README


## 🛠️ Guía Paso a Paso

### Paso 1 – Backend API
1. Genera el proyecto en `backend/` (Spring Initializr).
2. Implementa la entidad principal, repositorio y servicio.
3. Expone endpoints REST `/api/...` siguiendo buenas prácticas.
4. Añade pruebas unitarias y de integración (`@SpringBootTest`, `@DataJpaTest`).

### Paso 2 – Frontend Vaadin
1. Crea el proyecto en `frontend/` con Vaadin 24.
2. Implementa un DTO compatible con el backend y un cliente HTTP.
3. Construye la vista principal con `Grid`, filtros y notificaciones.

### Paso 3 – Docker + Compose
1. Escribe `backend/Dockerfile` (multi-stage recomendado).
2. Escribe `frontend/Dockerfile` (build + ejecución).
3. Configura `docker-compose.yml` con los 3 servicios, redes y variables.

### Paso 4 – Tests + CI
1. Ejecuta `mvn test` desde `backend/` hasta que pase sin errores.
2. Configura `.github/workflows/check_p15.yml` para automatizar la verificación.
3. Ejecuta `python3 grades/p15.py` en local antes de subir para ver tu nota. Conviene que te fijes en el resultado del Action en github para comprobar que es la misma nota. Si no es la misma, chequea qué puede estar pasando en un tu repositorio local.

### Paso 5 – Evidencias y entrega
1. Ejecuta `docker compose up --build` y captura `docker_ps.png`.
2. Captura la UI Vaadin (`ui_frontend.png`) con datos reales.
3. Captura los tests (`tests_ok.png`) y la ejecución del workflow en el Action de Github (`actions_ci.png`).
4. Sube todo a GitHub (`git push --all --tags`) y entrega el ZIP en Canvas.


## 🐞 Solución de Problemas

- **Vaadin no carga datos** → Verifica `APP_API_URL` y puertos expuestos.
- **`mvn test` falla en CI** → Revisa dependencias en `backend/pom.xml` y rutas relativas.
- **Docker no levanta la base de datos** → Asegura que el servicio `db` exporta el puerto y usa healthchecks o `depends_on`.
- **Grader da 0 en C5** → Revisa nombres exactos de las evidencias.

## 📚 Recursos recomendados

- [Spring Boot Reference](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Vaadin 24 Docs](https://vaadin.com/docs/latest/)
- [Spring Data JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [Docker Compose](https://docs.docker.com/compose/)
- [GitFlow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)

## ✅ Checklist final

- [ ] `backend/` y `frontend/` compilando sin errores
- [ ] `mvn test` OK en `backend/` y en CI
- [ ] Dockerfiles + `docker-compose.yml` con 3 servicios
- [ ] Workflow `.github/workflows/check_p15.yml`
- [ ] Evidencias (`ui_frontend`, `tests_ok`, `actions_ci`, `docker_ps`)
- [ ] GitFlow completo (`develop`, `feature/*`, `release/v1.0.0`, tag `v1.0.0`)
- [ ] `grades/p15.py` generado y ejecutado

Escoge el dominio que más te motive y demuestra tu soltura con el full stack típico de Java. 
