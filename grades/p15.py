#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
P15 Grader — Proyecto Libre Full-Stack: API REST + Vaadin + Tests + CI/CD

Criterios de evaluación (total base 10 puntos):
C0 (1.0): GitFlow completo (develop + ≥2 features + release v1.0.0 + tag)
C1 (2.0): Backend API en backend/ (Spring Boot + JPA + driver BD + REST CRUD)
C2 (2.0): Frontend Vaadin en frontend/ (Vaadin 24 + Grid + cliente HTTP)
C3 (2.0): Tests backend (archivos *Test.java + mvn test exitoso)
C4 (2.0): Docker & CI (docker-compose + Dockerfiles + workflow check_p15)
C5 (1.0): Evidencias oficiales en evidencias/

Puntuación extra (hasta +1.5 pts, máximo 10 total):
- +0.5: Integración de cobertura o calidad (JaCoCo, reports)
- +0.5: Despliegues o publicación de imágenes
- +0.5: Funcionalidades avanzadas en el frontend (diálogos, filtros, etc.)

Salida:
- resultados.csv (Usuario GitHub, Practica, Nota, Comentarios)

Uso:
python3 grades/p15.py
"""

import os
import re
import sys
import csv
import xml.etree.ElementTree as ET
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional, Set

EXCLUDED_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    "node_modules",
    "target",
    "grades",
    "ejemplos",
}

PRACTICA = "P15"

# ------------------------------ utilidades ------------------------------

def get_repo_root() -> Path:
    return Path(os.getcwd())

def extract_github_user() -> str:
    repo_name = os.getenv("GITHUB_REPOSITORY", "") # owner/repo
    if repo_name:
        repo_short = repo_name.split("/")[-1]
    else:
        repo_short = os.path.basename(os.getcwd())
    
    # Limpieza de prefijos habituales para P15
    cleaned = re.sub(r"(?i)^(DIS|dis)[_-]?p15[_-]?", "", repo_short)
    cleaned = re.sub(r"(?i)^p15[_-]?", "", cleaned)
    return cleaned or repo_short or "desconocido"

def write_csv_row(path: str, headers: List[str], row: List[str], append: bool = True):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    file_exists = os.path.exists(path)
    mode = "a" if append else "w"
    
    with open(path, mode, newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not file_exists or not append:
            w.writerow(headers)
        w.writerow(row)

def find_files_by_pattern(root: Path, patterns: List[str], exclude_dirs: Optional[Set[str]] = None) -> List[Path]:
    """Busca archivos que coincidan con patrones específicos"""
    excluded = exclude_dirs or EXCLUDED_DIRS
    found: List[Path] = []
    for pattern in patterns:
        for path in root.rglob(pattern):
            if any(part in excluded for part in path.parts):
                continue
            found.append(path)
    return found

def read_file_safe(path: Path) -> str:
    """Lee un archivo de forma segura"""
    try:
        # Intentar primero UTF-8
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            # Si falla, intentar con latin-1
            return path.read_text(encoding="latin-1")
        except Exception:
            return ""
    except Exception:
        return ""

def validate_evidence_name(img_name: str, expected_name: str) -> bool:
    """
    Valida si el nombre de imagen coincide con el esperado.
    Permite variaciones menores pero mantiene strictness para evitar falsos positivos.
    """
    img_lower = img_name.lower().strip()
    expected_lower = expected_name.lower().strip()
    
    # Matching exacto (ideal)
    if img_lower == expected_lower:
        return True
    
    # Matching con prefijo exacto (permite sufijos como _v1, _final, etc.)
    if img_lower.startswith(expected_lower):
        remainder = img_lower[len(expected_lower):]
        # Permitir solo sufijos numéricos o descriptivos comunes
        if re.match(r'^(_v?\d+|_final|_last|_complete)?$', remainder):
            return True
    
    # Matching flexible para nombres con guiones o espacios
    normalized_img = re.sub(r'[-_\s]+', '_', img_lower)
    normalized_expected = re.sub(r'[-_\s]+', '_', expected_lower)
    
    return normalized_img == normalized_expected or normalized_img.startswith(normalized_expected + '_')

def parse_java_version(value: str) -> Optional[int]:
    """Convierte una cadena de versión JVM en un entero comparable"""
    if not value:
        return None

    cleaned = value.strip()

    # Ignorar placeholders como ${java.version}
    if cleaned.startswith("${") and cleaned.endswith("}"):
        return None

    match = re.search(r"\d+(?:\.\d+)?", cleaned)
    if not match:
        return None

    token = match.group(0)

    if token.startswith("1."):
        try:
            return int(token.split(".")[1])
        except (IndexError, ValueError):
            return None

    try:
        return int(token.split(".")[0])
    except ValueError:
        return None


def detect_java_version(pom_path: Path) -> Optional[int]:
    """Intenta detectar la versión de Java configurada en un pom.xml"""
    versions: List[int] = []

    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
    except Exception:
        root = None

    if root is not None:
        for tag in [
            "java.version",
            "maven.compiler.release",
            "maven.compiler.target",
            "maven.compiler.source",
        ]:
            for elem in root.findall(f".//{{*}}{tag}"):
                parsed = parse_java_version(elem.text or "")
                if parsed is not None:
                    versions.append(parsed)

    if versions:
        return max(versions)

    content = read_file_safe(pom_path)
    pattern = re.compile(
        r"<(?:[\w\-.]+:)?(java\.version|maven\.compiler\.(?:release|target|source))>([^<]+)<",
        re.IGNORECASE,
    )

    for _, value in pattern.findall(content):
        parsed = parse_java_version(value)
        if parsed is not None:
            versions.append(parsed)

    return max(versions) if versions else None

# ------------------------------ criterios ------------------------------

IMG_EXTS = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"]

def score_c0_gitflow(root: Path) -> Tuple[float, str, List[str]]:
    """C0: GitFlow correcto (develop + ≥2 features + release v1.0.0 + tag)"""
    score = 0.0
    issues = []
    files_found = []
    
    try:
        # Verificar si hay repositorio git
        git_dir = root / ".git"
        if not git_dir.exists():
            return 0.0, "No hay repositorio Git inicializado", []
        
        # Obtener ramas
        result = subprocess.run(
            ["git", "branch", "-a"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return 0.5, "Error al ejecutar git branch", []
        
        branches = result.stdout.lower()
        
        # Verificar rama develop
        has_develop = "develop" in branches
        if has_develop:
            score += 0.3
        else:
            issues.append("falta rama develop")
        
        # Contar features
        feature_count = branches.count("feature/")
        if feature_count >= 2:
            score += 0.4
        elif feature_count == 1:
            score += 0.2
            issues.append("solo 1 feature (se requieren mínimo 2)")
        else:
            issues.append("faltan ramas feature")
        
        # Verificar release
        has_release = "release/" in branches or "release/v1.0.0" in branches
        if has_release:
            score += 0.2
        else:
            issues.append("falta rama release")
        
        # Verificar tag v1.0.0
        tag_result = subprocess.run(
            ["git", "tag"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if tag_result.returncode == 0:
            tags = tag_result.stdout.lower()
            if "v1.0.0" in tags:
                score += 0.1
            else:
                issues.append("falta tag v1.0.0")
        
        score = min(1.0, score)
        issue_text = "; ".join(issues[:3])
        comment = f"GitFlow: {score:.1f}/1.0"
        if issue_text:
            comment += f" - {issue_text}"
        
        return score, comment, files_found
        
    except subprocess.TimeoutExpired:
        return 0.5, "Timeout ejecutando comandos git", []
    except FileNotFoundError:
        return 0.0, "Git no está instalado", []
    except Exception as e:
        return 0.0, f"Error evaluando GitFlow: {str(e)}", []

def score_c1_backend_api(root: Path) -> Tuple[float, str, List[str]]:
    """C1: Backend API REST (Spring Boot + JPA + Endpoints)"""
    backend_dir = root / "backend"
    pom_path = backend_dir / "pom.xml"
    files_found: List[str] = []

    if not backend_dir.exists():
        return 0.0, "No existe la carpeta backend/", files_found
    if not pom_path.exists():
        return 0.0, "No se encontró backend/pom.xml", files_found

    files_found.append(str(pom_path))
    pom_content = read_file_safe(pom_path)

    score = 0.0
    issues = []

    if "spring-boot-starter-web" in pom_content:
        score += 0.4
    else:
        issues.append("Falta spring-boot-starter-web en backend/pom.xml")

    if "spring-boot-starter-data-jpa" in pom_content:
        score += 0.4
    else:
        issues.append("Falta spring-boot-starter-data-jpa en backend/pom.xml")

    if any(db in pom_content.lower() for db in ["mysql", "mariadb", "h2"]):
        score += 0.2
    else:
        issues.append("Falta driver de base de datos (H2/MySQL/MariaDB)")

    java_version = detect_java_version(pom_path)
    if java_version is not None and java_version < 17:
        issues.append(f"Java < 17 en backend (detectado {java_version})")

    java_files = find_files_by_pattern(backend_dir, ["**/*.java"])
    has_entity = False
    has_repository = False
    has_rest_controller = False

    for java_file in java_files:
        content = read_file_safe(java_file)
        if not has_entity and "@Entity" in content:
            has_entity = True
            files_found.append(str(java_file))
        if not has_repository and "extends" in content and "JpaRepository" in content:
            has_repository = True
            files_found.append(str(java_file))
        if "@RestController" in content:
            if ("/api" in content) or ("@RequestMapping(\"/api" in content):
                has_rest_controller = True
                files_found.append(str(java_file))

    if has_entity:
        score += 0.3
    else:
        issues.append("No se encontró ninguna entidad @Entity en backend/")

    if has_repository:
        score += 0.3
    else:
        issues.append("No se encontró repositorio que extienda JpaRepository")

    if has_rest_controller:
        score += 0.4
    else:
        issues.append("No se encontró @RestController con prefijo /api")

    score = min(2.0, score)
    issue_text = "; ".join(issues[:3])
    comment = f"Backend API: {score:.1f}/2.0"
    if issue_text:
        comment += f" - {issue_text}"

    return score, comment, files_found

def score_c2_frontend_vaadin(root: Path) -> Tuple[float, str, List[str]]:
    """C2: Frontend Vaadin (HTTP Client + Grid + @Route)"""
    frontend_dir = root / "frontend"
    pom_path = frontend_dir / "pom.xml"
    files_found: List[str] = []

    if not frontend_dir.exists():
        return 0.0, "No existe la carpeta frontend/", files_found
    if not pom_path.exists():
        return 0.0, "No se encontró frontend/pom.xml", files_found

    files_found.append(str(pom_path))
    pom_content = read_file_safe(pom_path).lower()

    score = 0.0
    issues = []

    if "vaadin" in pom_content and ("24." in pom_content or "<vaadin.version>24" in pom_content):
        score += 0.5
    else:
        issues.append("frontend/pom.xml no declara Vaadin 24")

    java_files = find_files_by_pattern(frontend_dir, ["**/*.java"])
    has_route = False
    has_grid = False
    has_http_client = False

    for java_file in java_files:
        content = read_file_safe(java_file)
        if "@Route" in content:
            has_route = True
            files_found.append(str(java_file))
        if "Grid<" in content:
            has_grid = True
            files_found.append(str(java_file))
        if any(client in content for client in ["RestTemplate", "WebClient", "HttpClient"]):
            has_http_client = True
            files_found.append(str(java_file))

    if has_route:
        score += 0.5
    else:
        issues.append("No se encontró ninguna vista con @Route")

    if has_grid:
        score += 0.5
    else:
        issues.append("No se encontró Grid mostrando datos")

    if has_http_client:
        score += 0.5
    else:
        issues.append("No se encontró cliente HTTP en frontend/")

    score = min(2.0, score)
    issue_text = "; ".join(issues[:3])
    comment = f"Frontend Vaadin: {score:.1f}/2.0"
    if issue_text:
        comment += f" - {issue_text}"

    return score, comment, files_found

def score_c3_tests_backend(root: Path) -> Tuple[float, str, List[str]]:
    """C3: Tests backend (JUnit + mvn test)"""
    backend_dir = root / "backend"
    files_found: List[str] = []
    issues = []

    if not backend_dir.exists():
        return 0.0, "No existe backend/ para ejecutar tests", files_found

    test_dir = backend_dir / "src" / "test" / "java"
    test_files = list(test_dir.rglob("*Test.java")) if test_dir.exists() else []
    files_found.extend(str(f) for f in test_files)

    # Ejecutar mvn test (criterio obligatorio)
    try:
        result = subprocess.run(
            ["mvn", "test", "-q"],
            cwd=backend_dir,
            capture_output=True,
            text=True,
            timeout=180
        )
    except FileNotFoundError:
        return 0.0, "Maven no está instalado en el runner", files_found
    except subprocess.TimeoutExpired:
        return 0.0, "Timeout ejecutando mvn test en backend/", files_found

    if result.returncode != 0:
        issues.append("mvn test falló (revisa logs en target/surefire-reports)")
        return 0.0, f"Tests backend: 0/2.0 - mvn test falló\n{result.stderr[-400:]}", files_found

    score = 1.0  # mvn test OK

    if test_files:
        score += 0.6
    else:
        issues.append("No hay archivos *Test.java en backend/src/test/java")

    test_annotations = 0
    for java_file in test_files:
        content = read_file_safe(java_file)
        test_annotations += content.count("@Test")

    if test_annotations >= 3:
        score += 0.4
    elif test_annotations >= 1:
        score += 0.2
        issues.append("Menos de 3 métodos @Test")
    else:
        issues.append("No se detectó ninguna anotación @Test")

    score = min(2.0, score)
    issue_text = "; ".join(issues[:3])
    comment = f"Tests backend: {score:.1f}/2.0"
    if issue_text:
        comment += f" - {issue_text}"

    return score, comment, files_found

def score_c4_docker_ci(root: Path) -> Tuple[float, str, List[str]]:
    """C4: Docker & CI (docker-compose + Dockerfiles + workflow check_p15)"""
    score = 0.0
    issues = []
    files_found: List[str] = []

    compose_path = root / "docker-compose.yml"
    if compose_path.exists():
        files_found.append(str(compose_path))
        content = read_file_safe(compose_path)
        score += 0.3  # archivo presente

        service_names = set(re.findall(r"^\s{2,}([A-Za-z0-9_-]+):\s*$", content, re.MULTILINE))
        if len(service_names) >= 3:
            score += 0.3
        else:
            issues.append("docker-compose.yml tiene menos de 3 servicios")

        required_services = {
            "backend": {"backend"},
            "frontend": {"frontend"},
            "db": {"db", "database", "mysql", "mariadb", "postgres"}
        }
        matched = 0
        for key, aliases in required_services.items():
            if any(service in service_names for service in aliases):
                matched += 1
        if matched == 3:
            score += 0.3
        else:
            issues.append("docker-compose.yml debe contener servicios backend/frontend/db")
    else:
        issues.append("No se encontró docker-compose.yml en la raíz")

    backend_dockerfile = root / "backend" / "Dockerfile"
    frontend_dockerfile = root / "frontend" / "Dockerfile"

    if backend_dockerfile.exists():
        score += 0.3
        files_found.append(str(backend_dockerfile))
    else:
        issues.append("Falta backend/Dockerfile")

    if frontend_dockerfile.exists():
        score += 0.3
        files_found.append(str(frontend_dockerfile))
    else:
        issues.append("Falta frontend/Dockerfile")

    workflow_path = root / ".github" / "workflows" / "check_p15.yml"
    workflow_score = 0.0
    if workflow_path.exists():
        files_found.append(str(workflow_path))
        workflow_content = read_file_safe(workflow_path)
        workflow_score += 0.2  # archivo presente

        if "actions/setup-java" in workflow_content and "17" in workflow_content:
            workflow_score += 0.2
        else:
            issues.append("Workflow check_p15.yml no configura Java 17")

        if "mvn test" in workflow_content and "backend" in workflow_content:
            workflow_score += 0.1
        else:
            issues.append("Workflow debe ejecutar mvn test en backend/")

        if "grades/p15.py" in workflow_content:
            workflow_score += 0.2
        else:
            issues.append("Workflow no ejecuta grades/p15.py")

        if "actions/checkout" in workflow_content:
            workflow_score += 0.1
        else:
            issues.append("Workflow debe usar actions/checkout")
    else:
        issues.append("No existe .github/workflows/check_p15.yml")

    score += min(0.6, workflow_score)
    score = min(2.0, score)

    issue_text = "; ".join(issues[:3])
    comment = f"Docker & CI: {score:.1f}/2.0"
    if issue_text:
        comment += f" - {issue_text}"

    return score, comment, files_found

def score_evidencias(root: Path) -> Tuple[float, str, List[str]]:
    """C5: Evidencias de funcionamiento (imágenes requeridas) - 1.0 punto"""
    evidencias_dir = root / "evidencias"
    if not evidencias_dir.exists():
        return 0.0, "Carpeta 'evidencias/' no encontrada", []

    required_images = {
        "ui_frontend": 0.25,   # Grid Vaadin funcionando
        "tests_ok": 0.25,      # mvn test en verde
        "actions_ci": 0.25,    # Workflow GitHub Actions finalizado
        "docker_ps": 0.25      # Contenedores activos
    }

    bonus_images = {
        "gitflow_branches": 0.1,
        "compose_logs": 0.1
    }

    found_images = []
    found_required = set()
    found_bonus = set()
    score = 0.0

    all_images = []
    for ext in IMG_EXTS:
        all_images.extend(evidencias_dir.glob(f"*{ext}"))

    for img_path in all_images:
        if img_path.stat().st_size < 1000:
            continue

        img_name = img_path.stem.lower()
        found_images.append(str(img_path))

        for req_name, points in required_images.items():
            if validate_evidence_name(img_name, req_name):
                if req_name not in found_required:
                    found_required.add(req_name)
                    score += points
                break

        for bonus_name, points in bonus_images.items():
            if validate_evidence_name(img_name, bonus_name):
                if bonus_name not in found_bonus:
                    found_bonus.add(bonus_name)
                    score += points
                break

    score = min(1.0, score)
    found_req_list = [name for name in required_images.keys() if name in found_required]
    missing_list = [name for name in required_images.keys() if name not in found_required]

    comment = f"{len(found_required)}/4 obligatorias"
    if found_req_list:
        comment += f" ({', '.join(found_req_list)})"
    if missing_list:
        comment += f"; faltan: {', '.join(missing_list)}"
    if found_bonus:
        comment += f"; bonus: {', '.join(sorted(found_bonus))}"

    return score, comment, found_images

def calculate_extra_score(root: Path) -> Tuple[float, str]:
    """Puntuación extra por mejoras avanzadas"""
    extra_score = 0.0
    improvements = []

    workflow_path = root / ".github" / "workflows" / "check_p15.yml"
    workflow_content = read_file_safe(workflow_path) if workflow_path.exists() else ""

    backend_pom = root / "backend" / "pom.xml"
    pom_content = read_file_safe(backend_pom) if backend_pom.exists() else ""
    if "jacoco" in pom_content.lower() or "coverage" in workflow_content.lower():
        extra_score += 0.5
        improvements.append("Cobertura configurada")

    if any(keyword in workflow_content.lower() for keyword in ["deploy", "build-push-action", "ghcr.io", "docker/login-action"]):
        extra_score += 0.5
        improvements.append("Despliegue / publicación en CI")

    frontend_dir = root / "frontend"
    vaadin_files = find_files_by_pattern(frontend_dir, ["**/*.java"]) if frontend_dir.exists() else []
    vaadin_content = "".join(read_file_safe(f) for f in vaadin_files)
    if any(component in vaadin_content for component in ["Dialog", "ComboBox", "Binder", "GridPro", "Charts"]):
        extra_score += 0.5
        improvements.append("UI avanzada en Vaadin")

    extra_score = min(1.5, extra_score)
    comment = f"Extra: +{extra_score:.1f} pts"
    if improvements:
        comment += f" ({', '.join(improvements)})"

    return extra_score, comment

def main():
    root = get_repo_root()
    usuario = extract_github_user()

    print(f"🔍 Evaluando P15 para usuario: {usuario}")
    print(f"📁 Directorio raíz: {root}")

    # Evaluar criterios
    c0_score, c0_comment, c0_files = score_c0_gitflow(root)
    c1_score, c1_comment, c1_files = score_c1_backend_api(root)
    c2_score, c2_comment, c2_files = score_c2_frontend_vaadin(root)
    c3_score, c3_comment, c3_files = score_c3_tests_backend(root)
    c4_score, c4_comment, c4_files = score_c4_docker_ci(root)

    # Evidencias (C5)
    ev_score, ev_comment, ev_files = score_evidencias(root)

    # Extra
    extra_score, extra_comment = calculate_extra_score(root)

    base_score = c0_score + c1_score + c2_score + c3_score + c4_score + ev_score
    total_score = min(10.0, base_score + extra_score)

    comments = [
        f"C0 GitFlow: {c0_score:.1f}/1.0",
        f"C1 Backend API: {c1_score:.1f}/2.0",
        f"C2 Frontend Vaadin: {c2_score:.1f}/2.0",
        f"C3 Tests backend: {c3_score:.1f}/2.0",
        f"C4 Docker & CI: {c4_score:.1f}/2.0",
        f"C5 Evidencias: {ev_score:.1f}/1.0"
    ]
    if extra_score > 0:
        comments.append(f"Extra: +{extra_score:.1f}/2.0")

    final_comment = "; ".join(comments)

    print("\n" + "="*60)
    print(f"📊 RESULTADOS EVALUACIÓN {PRACTICA}")
    print("="*60)
    print(f"👤 Usuario: {usuario}")
    print(f"🎯 Práctica: {PRACTICA}")
    print(f"📈 Nota: {total_score:.1f}/10.0")
    print("\n📋 Detalle por criterios:")
    print(f"  C0 - GitFlow:         {c0_score:.1f}/1.0")
    print(f"  C1 - Backend API:     {c1_score:.1f}/2.0")
    print(f"  C2 - Frontend Vaadin: {c2_score:.1f}/2.0")
    print(f"  C3 - Tests backend:   {c3_score:.1f}/2.0")
    print(f"  C4 - Docker & CI:     {c4_score:.1f}/2.0")
    print(f"  C5 - Evidencias:      {ev_score:.1f}/1.0")
    if extra_score > 0:
        print(f"  ⭐ Extra:            +{extra_score:.1f}/2.0 (máx 10 total)")

    print(f"\n💬 Comentarios: {final_comment}")

    all_files = set(c0_files + c1_files + c2_files + c3_files + c4_files + ev_files)
    if all_files:
        print(f"\n📁 Archivos evaluados ({len(all_files)}):")
        for file_path in sorted(all_files)[:10]:
            print(f"  ✓ {file_path}")
        if len(all_files) > 10:
            print(f"  ... y {len(all_files) - 10} más")

    print("\n" + "="*60)

    write_csv_row(
        "resultados.csv",
        ["Usuario GitHub", "Practica", "Nota", "Comentarios"],
        [usuario, PRACTICA, f"{total_score:.1f}", final_comment],
        append=False
    )

    print(f"✅ Resultado guardado en resultados.csv")
    return int(total_score)

if __name__ == "__main__":
    try:
        exit_code = main()
        if exit_code < 5:
            print("⚠️ Nota inferior a 5.0; el CSV se ha generado igualmente.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error durante la evaluación: {e}")
        sys.exit(1)
