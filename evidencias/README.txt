## 📸 Evidencias P15 - Proyecto Libre Full-Stack

### ✅ Capturas OBLIGATORIAS (nombres exactos):

1. **ui_frontend.png** – Vista Vaadin funcionando
   - Debe mostrar: Interfaz Vaadin 24 con el Grid principal lleno de datos reales del dominio elegido.
   - Incluir: URL visible (por ejemplo `http://localhost:8080`) y varias filas en el Grid.
   - Verificar: Columnas coherentes con la entidad principal y consumo del backend REST ya integrado.

2. **tests_ok.png** – Tests de backend en verde
   - Debe mostrar: Resultado de `mvn test` ejecutado dentro de `backend/`.
   - Incluir: Consola con “BUILD SUCCESS” o salida equivalente.
   - Verificar: Que la carpeta `backend/src/test/java` existe y las pruebas pasan sin errores.

3. **actions_ci.png** – Workflow de GitHub Actions
   - Debe mostrar: Pantalla de Actions en GitHub con el workflow `Check P15` finalizado correctamente.
   - Incluir: Evidencia de que se ejecutaron los pasos críticos (checkout, setup-java, mvn test, grades/p15.py).
   - Verificar: Estatus “Success” o equivalente en la ejecución mostrada.

4. **docker_ps.png** – Contenedores activos
   - Debe mostrar: Salida de `docker ps` o la vista de Docker Desktop.
   - Incluir: Servicios `backend`, `frontend` y `db` levantados según `docker-compose.yml`.
   - Verificar: Estado “Up” y puertos mapeados a 8080/8081/3306 (o los definidos en el compose).

### 🏆 Capturas OPCIONALES (para nota extra):

5. **gitflow_branches.png** – Estructura GitFlow completa
   - Mostrar: Salida de `git branch -a` con `develop`, al menos 2 `feature/...` y `release/v1.0.0`.
   - Incluir: Evidencia de que el tag `v1.0.0` existe (`git tag`).

6. **compose_logs.png** – Logs de Docker Compose
   - Mostrar: `docker compose logs backend` o `frontend` evidenciando la integración entre servicios.
   - Incluir: Mensajes donde se vea la API atendiendo peticiones o el frontend llamando al backend.

### ❌ IMPORTANTE:
- Solo formatos PNG o JPG (mínimo 1 KB por archivo).
- Nombres EXACTOS (respeta mayúsculas/minúsculas).
- Las imágenes se validan automáticamente por el `grades/p15.py`.
- Las 4 capturas obligatorias son necesarias para obtener el punto de evidencias.
