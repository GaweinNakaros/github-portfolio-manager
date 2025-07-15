#!/usr/bin/env python3
"""
GitHub Repository Professionalization Script
Automatiza la profesionalización de repositorios académicos
"""

import json
import os
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

console = Console()

class RepoProfessionalizer:
    def __init__(self):
        self.templates_dir = Path('templates')
        self.audit_data = None
        
    def load_latest_audit(self):
        """Carga la auditoría más reciente"""
        audit_dir = Path('data/audits')
        if not audit_dir.exists():
            console.print("❌ No se encontraron auditorías previas", style="red")
            return False
        
        # Buscar el archivo más reciente
        audit_files = list(audit_dir.glob('audit_*.json'))
        if not audit_files:
            console.print("❌ No se encontraron archivos de auditoría", style="red")
            return False
        
        latest_file = max(audit_files, key=os.path.getctime)
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                self.audit_data = json.load(f)
            console.print(f"✅ Cargada auditoría: {latest_file.name}", style="green")
            return True
        except Exception as e:
            console.print(f"❌ Error cargando auditoría: {e}", style="red")
            return False
    
    def select_repository(self):
        """Permite seleccionar un repositorio para profesionalizar"""
        if not self.audit_data:
            return None
        
        # Filtrar repositorios académicos y sin clasificar
        candidates = []
        for repo in self.audit_data['repositories']:
            if "🎓" in repo['classification'] or "📁" in repo['classification']:
                candidates.append(repo)
        
        if not candidates:
            console.print("❌ No hay repositorios candidatos para profesionalizar", style="yellow")
            return None
        
        console.print("\n🎯 Repositorios candidatos para profesionalización:")
        for i, repo in enumerate(candidates, 1):
            console.print(f"{i}. {repo['name']} - {repo['classification']}")
        
        try:
            choice = int(Prompt.ask("Selecciona un repositorio", default="1"))
            if 1 <= choice <= len(candidates):
                return candidates[choice - 1]
        except ValueError:
            console.print("❌ Selección inválida", style="red")
        
        return None
    
    def create_professional_readme(self, repo):
        """Crea un README profesional para el repositorio"""
        template_path = self.templates_dir / 'README_template.md'
        
        if not template_path.exists():
            console.print("❌ Plantilla README no encontrada", style="red")
            return False
        
        # Leer plantilla
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Solicitar información del usuario
        console.print(f"\n📝 Configurando README para: {repo['name']}")
        
        project_name = repo['name']
        description = Prompt.ask("Descripción del proyecto", default=repo.get('description', ''))
        
        # Detectar tecnologías basadas en el lenguaje
        language = repo.get('language', 'N/A')
        tech_suggestions = {
            'Python': {'backend': 'Python, Flask/Django', 'frontend': 'HTML, CSS, JavaScript'},
            'HTML': {'frontend': 'HTML, CSS, JavaScript', 'backend': 'N/A'},
            'CSS': {'frontend': 'HTML, CSS, JavaScript', 'backend': 'N/A'},
            'JavaScript': {'frontend': 'JavaScript, React/Vue', 'backend': 'Node.js'},
            'PHP': {'backend': 'PHP', 'frontend': 'HTML, CSS, JavaScript'}
        }
        
        frontend_tech = Prompt.ask("Tecnologías Frontend", 
                                  default=tech_suggestions.get(language, {}).get('frontend', 'HTML, CSS, JavaScript'))
        backend_tech = Prompt.ask("Tecnologías Backend", 
                                 default=tech_suggestions.get(language, {}).get('backend', 'N/A'))
        database = Prompt.ask("Base de datos", default="SQLite/MySQL")
        
        # Comandos de instalación y ejecución
        install_commands = self.get_install_commands(language)
        run_commands = self.get_run_commands(language)
        
        # Reemplazar placeholders
        readme_content = template.replace('{PROJECT_NAME}', project_name)
        readme_content = readme_content.replace('{DESCRIPTION}', description)
        readme_content = readme_content.replace('{FRONTEND_TECH}', frontend_tech)
        readme_content = readme_content.replace('{BACKEND_TECH}', backend_tech)
        readme_content = readme_content.replace('{DATABASE}', database)
        readme_content = readme_content.replace('{OTHER_TECH}', f"{language}, Git, GitHub")
        readme_content = readme_content.replace('{INSTALL_COMMANDS}', install_commands)
        readme_content = readme_content.replace('{RUN_COMMANDS}', run_commands)
        readme_content = readme_content.replace('{YOUR_NAME}', "Tu Nombre")
        readme_content = readme_content.replace('{YOUR_EMAIL}', "tu.email@ejemplo.com")
        readme_content = readme_content.replace('{YOUR_LINKEDIN}', "https://linkedin.com/in/tu-perfil")
        readme_content = readme_content.replace('{YOUR_PORTFOLIO}', "https://tu-portfolio.com")
        
        # Agregar características automáticas
        features = self.generate_features(repo, language)
        for i, feature in enumerate(features, 1):
            readme_content = readme_content.replace(f'{{FEATURE_{i}}}', feature)
        
        # Guardar README
        output_dir = Path('output') / project_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        readme_path = output_dir / 'README.md'
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        console.print(f"✅ README generado: {readme_path}", style="green")
        return True
    
    def get_install_commands(self, language):
        """Genera comandos de instalación según el lenguaje"""
        commands = {
            'Python': '# Instalar dependencias\npip install -r requirements.txt',
            'JavaScript': '# Instalar dependencias\nnpm install',
            'PHP': '# Instalar dependencias\ncomposer install',
            'HTML': '# No requiere instalación especial\n# Abrir index.html en navegador'
        }
        return commands.get(language, '# Seguir instrucciones específicas del proyecto')
    
    def get_run_commands(self, language):
        """Genera comandos de ejecución según el lenguaje"""
        commands = {
            'Python': '# Ejecutar aplicación\npython app.py\n# o\npython manage.py runserver',
            'JavaScript': '# Ejecutar en modo desarrollo\nnpm start\n# o\nnpm run dev',
            'PHP': '# Ejecutar servidor local\nphp -S localhost:8000',
            'HTML': '# Abrir en navegador\n# Usar Live Server en VS Code'
        }
        return commands.get(language, '# Seguir instrucciones del proyecto')
    
    def generate_features(self, repo, language):
        """Genera características automáticas basadas en el tipo de proyecto"""
        base_features = [
            "Interfaz intuitiva y responsive",
            f"Desarrollado en {language}",
            "Código limpio y documentado"
        ]
        
        # Agregar características específicas según el nombre del repo
        name_lower = repo['name'].lower()
        if 'control' in name_lower or 'stock' in name_lower:
            base_features.extend([
                "Gestión de inventario en tiempo real",
                "Sistema de alertas de stock bajo",
                "Reportes y estadísticas"
            ])
        elif 'web' in name_lower:
            base_features.extend([
                "Diseño responsive para todos los dispositivos",
                "Optimización SEO",
                "Carga rápida y eficiente"
            ])
        elif any(word in name_lower for word in ['comision', 'clase', 'curso']):
            base_features.extend([
                "Material educativo estructurado",
                "Ejercicios prácticos incluidos",
                "Ejemplos de código comentados"
            ])
        
        return base_features[:3]  # Retornar solo las primeras 3
    
    def create_project_structure(self, repo):
        """Crea estructura de proyecto profesional"""
        project_name = repo['name']
        output_dir = Path('output') / project_name
        
        # Crear directorios estándar
        directories = [
            'src',
            'docs',
            'tests',
            'assets/css',
            'assets/js',
            'assets/images',
            'config'
        ]
        
        for directory in directories:
            dir_path = output_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Crear archivos básicos
        files_to_create = {
            'src/main.py': '#!/usr/bin/env python3\n"""Archivo principal del proyecto"""\n\nif __name__ == "__main__":\n    print("¡Hola mundo!")\n',
            'requirements.txt': '# Dependencias del proyecto\n# requests>=2.25.1\n# flask>=2.0.0\n',
            'LICENSE': 'MIT License\n\nCopyright (c) 2025\n\n...',
            '.gitignore': '# Python\n__pycache__/\n*.pyc\n*.pyo\n*.pyd\n.Python\nenv/\nvenv/\n.venv/\n.env\n\n# IDE\n.vscode/\n.idea/\n*.swp\n*.swo\n\n# OS\n.DS_Store\nThumbs.db\n',
            'docs/CONTRIBUTING.md': '# Guía de Contribución\n\n## Cómo contribuir\n\n1. Fork el proyecto\n2. Crea una rama para tu feature\n3. Realiza tus cambios\n4. Envía un pull request\n'
        }
        
        for file_path, content in files_to_create.items():
            full_path = output_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        console.print(f"✅ Estructura de proyecto creada en: {output_dir}", style="green")

def main():
    professionalizer = RepoProfessionalizer()
    
    console.print(Panel.fit(
        "🚀 GitHub Repository Professionalizer\n"
        "Convierte repositorios académicos en proyectos profesionales",
        title="Professional Portfolio Manager"
    ))
    
    # Cargar auditoría
    if not professionalizer.load_latest_audit():
        return
    
    # Seleccionar repositorio
    selected_repo = professionalizer.select_repository()
    if not selected_repo:
        return
    
    console.print(f"\n🎯 Profesionalizando: {selected_repo['name']}")
    
    # Confirmar proceso
    if not Confirm.ask("¿Continuar con la profesionalización?"):
        console.print("❌ Operación cancelada", style="yellow")
        return
    
    # Crear README profesional
    if professionalizer.create_professional_readme(selected_repo):
        # Crear estructura de proyecto
        professionalizer.create_project_structure(selected_repo)
        
        console.print(f"\n✅ ¡Repositorio {selected_repo['name']} profesionalizado exitosamente!", style="green bold")
        console.print("\n📋 Próximos pasos:")
        console.print("1. Revisar y personalizar el README generado")
        console.print("2. Agregar el código fuente a la carpeta src/")
        console.print("3. Completar la documentación en docs/")
        console.print("4. Agregar tests en la carpeta tests/")
        console.print("5. Publicar en GitHub con la nueva estructura")

if __name__ == "__main__":
    main()
