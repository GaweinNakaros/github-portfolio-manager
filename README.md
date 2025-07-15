# 🚀 GitHub Portfolio Manager

Sistema completo para la gestión profesional de portfolios de GitHub. Automatiza la auditoría, clasificación y profesionalización de repositorios académicos.

## ✨ Características

- 📊 **Auditoría Automática**: Analiza repositorios con GitHub CLI
- 🎯 **Clasificación Inteligente**: Categoriza repos por tipo (académico, profesional, experimental)
- 🚀 **Profesionalización**: Convierte proyectos académicos en portfolios profesionales
- 📝 **Templates Adaptativos**: Genera documentación según tecnología
- 📈 **Reportes Detallados**: Métricas y recomendaciones automáticas
- 🏗️ **Estructura Estándar**: Organización profesional de proyectos

## 🛠️ Tecnologías

- **Python**: Scripts de automatización
- **GitHub CLI**: Integración con API de GitHub
- **Rich**: Interfaz de consola elegante
- **JSON**: Persistencia de datos
- **Markdown**: Documentación y templates

## 📦 Instalación

```bash
# Clonar repositorio
git clone https://github.com/GaweinNakaros/github-portfolio-manager.git
cd github-portfolio-manager

# Instalar dependencias Python
pip install -r requirements.txt

# Instalar GitHub CLI (si no está instalado)
# Windows: winget install GitHub.cli
# macOS: brew install gh
# Linux: Ver https://cli.github.com/
```

## 🏃‍♂️ Uso

### 1. Auditar Portfolio

```bash
# Auditoría básica
python scripts/audit.py

# Auditar usuario específico
python scripts/audit.py --user tu-usuario

# Especificar directorio de salida
python scripts/audit.py --user tu-usuario --output mi-directorio
```

### 2. Profesionalizar Repositorio

```bash
# Lanzar asistente de profesionalización
python scripts/professionalize.py
```

## 📁 Estructura del Proyecto

```
github-portfolio-manager/
├── 📋 Documentación/
│   ├── methodology.md          # Metodología de auditoría
│   ├── audit-process.md        # Proceso específico de auditoría
│   ├── professionalization-guide.md  # Guía de profesionalización
│   └── project-architecture.md # Arquitectura técnica
├── 🔧 scripts/
│   ├── audit.py               # Script de auditoría automática
│   └── professionalize.py     # Script de profesionalización
├── 📊 data/
│   └── audits/                # Reportes de auditoría en JSON
├── 📝 templates/
│   └── README_template.md     # Plantilla de README profesional
├── ⚙️ package.json            # Configuración del proyecto
├── 🐍 requirements.txt        # Dependencias Python
└── 📖 README.md              # Este archivo
```

## 📊 Ejemplo de Auditoría

El sistema genera reportes como este:

```
📊 Auditoría de Repositorios - GaweinNakaros
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Repositorio                      ┃ Tipo              ┃ Lenguaje ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ github-portfolio-manager         │ 🚀 Profesional    │ Python   │
│ Comision-20015                   │ 🎓 Académico      │ HTML     │
│ Control-de-stock-web             │ 🚀 Profesional    │ Python   │
└──────────────────────────────────┴───────────────────┴──────────┘

🎯 Recomendaciones:
• Prioriza la creación de repositorios profesionales
• 3 repos privados - evalúa hacerlos públicos
• 15 repos sin descripción - agregar documentación
```

## 🎯 Metodología

### Clasificación de Repositorios:

- **🎓 Académicos**: Proyectos de cursos, comisiones, talleres
- **🚀 Profesionales**: Aplicaciones, sistemas, herramientas
- **🧪 Experimentales**: Pruebas, experimentos, prototipos
- **📁 Sin clasificar**: Requieren revisión manual

### Criterios de Profesionalización:

1. **Documentación completa** (README, licencia, contribución)
2. **Estructura organizada** (src/, docs/, tests/)
3. **Descripción clara** del propósito y características
4. **Instalación y uso** detallados
5. **Información de contacto** profesional

## 🤝 Contribución

¿Quieres mejorar el sistema? ¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

## 📞 Contacto

**GitHub**: [@GaweinNakaros](https://github.com/GaweinNakaros)
**Portfolio**: [github-portfolio-manager](https://github.com/GaweinNakaros/github-portfolio-manager)

---

## 🚀 Estado del Proyecto

- ✅ Sistema de auditoría automática
- ✅ Clasificación inteligente de repositorios  
- ✅ Generación de reportes detallados
- ✅ Script de profesionalización interactivo
- ✅ Templates adaptativos de documentación
- ✅ Estructura de proyecto estándar
- 🔄 Dashboard web (próximamente)
- 🔄 Integración con GitHub Actions (próximamente)

⭐ ¡No olvides dar una estrella si este proyecto te fue útil!
