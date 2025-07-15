#!/usr/bin/env python3
"""
GitHub Portfolio Audit Script
Automatiza la auditoría de repositorios siguiendo metodología establecida
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class GitHubAuditor:
    def __init__(self, username):
        self.username = username
        self.repos = []
        self.gh_command = 'gh'  # Comando por defecto
        
    def check_gh_cli(self):
        """Verifica que GitHub CLI esté instalado"""
        # Ubicaciones comunes de GitHub CLI en Windows
        possible_paths = [
            'gh',  # Si está en PATH
            'C:\\Program Files\\GitHub CLI\\gh.exe',
            'C:\\Program Files (x86)\\GitHub CLI\\gh.exe',
            f'{Path.home()}\\AppData\\Local\\GitHubCLI\\gh.exe'
        ]
        
        for gh_path in possible_paths:
            try:
                result = subprocess.run(
                    [gh_path, '--version'],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    msg = f"✅ GitHub CLI detectado en: {gh_path}"
                    console.print(msg, style="green")
                    self.gh_command = gh_path
                    return True
            except (FileNotFoundError, OSError):
                continue
        
        console.print("❌ GitHub CLI no encontrado", style="red")
        console.print("Instala GitHub CLI: https://cli.github.com/")
        return False
    
    def fetch_repositories(self):
        """Obtiene lista de repositorios del usuario"""
        console.print(f"🔍 Analizando repositorios de {self.username}...")
        
        try:
            cmd = [
                self.gh_command, 'repo', 'list', self.username,
                '--limit', '100', '--json',
                'name,description,primaryLanguage,isPrivate,' +
                'updatedAt,stargazerCount'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.repos = json.loads(result.stdout)
                msg = f"✅ {len(self.repos)} repositorios encontrados"
                console.print(msg, style="green")
                return True
            else:
                error_msg = f"❌ Error al obtener repositorios: {result.stderr}"
                console.print(error_msg, style="red")
                return False
                
        except Exception as e:
            console.print(f"❌ Error: {e}", style="red")
            return False
    
    def classify_repository(self, repo):
        """Clasifica el repositorio según criterios establecidos"""
        name = repo['name'].lower()
        
        # Clasificación según nomenclatura
        academic_keywords = [
            'comision', 'clase', 'coder', 'pfi', 'talento', 'curso'
        ]
        professional_keywords = [
            'control', 'stock', 'web', 'app', 'system', 'manager'
        ]
        
        if any(keyword in name for keyword in academic_keywords):
            return "🎓 Académico"
        elif any(keyword in name for keyword in professional_keywords):
            return "🚀 Profesional"
        elif repo['name'].startswith('test') or 'experiment' in name:
            return "🧪 Experimental"
        else:
            return "📁 Sin clasificar"
    
    def generate_report(self):
        """Genera reporte de auditoría"""
        if not self.repos:
            console.print("❌ No hay repositorios para reportar", style="red")
            return
        
        # Crear tabla de resultados
        table = Table(title=f"📊 Auditoría de Repositorios - {self.username}")
        
        table.add_column("Repositorio", style="cyan", no_wrap=True)
        table.add_column("Tipo", style="magenta")
        table.add_column("Lenguaje", style="green")
        table.add_column("Privado", justify="center")
        table.add_column("Stars", justify="center")
        table.add_column("Actualizado", style="yellow")
        
        # Clasificar y agregar repositorios
        classified_repos = []
        for repo in self.repos:
            classification = self.classify_repository(repo)
            if repo['primaryLanguage']:
                language = repo['primaryLanguage']['name']
            else:
                language = 'N/A'
            private = "🔒" if repo['isPrivate'] else "🌐"
            stars = str(repo['stargazerCount'])
            updated = repo['updatedAt'][:10]  # Solo fecha
            
            table.add_row(
                repo['name'],
                classification,
                language,
                private,
                stars,
                updated
            )
            
            classified_repos.append({
                'name': repo['name'],
                'classification': classification,
                'language': language,
                'private': repo['isPrivate'],
                'stars': repo['stargazerCount'],
                'updated': updated,
                'description': repo['description']
            })
        
        console.print(table)
        
        # Guardar reporte en archivo
        self.save_report(classified_repos)
        
        # Mostrar recomendaciones
        self.show_recommendations(classified_repos)
    
    def save_report(self, classified_repos):
        """Guarda el reporte en formato JSON"""
        output_dir = Path('data/audits')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = output_dir / f'audit_{self.username}_{timestamp}.json'
        
        report_data = {
            'username': self.username,
            'audit_date': datetime.now().isoformat(),
            'total_repos': len(classified_repos),
            'repositories': classified_repos
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        console.print(f"💾 Reporte guardado: {filename}", style="green")
    
    def show_recommendations(self, repos):
        """Muestra recomendaciones basadas en la auditoría"""
        academic_count = len([r for r in repos if "🎓" in r['classification']])
        prof_count = len([r for r in repos if "🚀" in r['classification']])
        
        recommendations = []
        
        if prof_count < 3:
            msg = "• Considera convertir repos académicos en proyectos profesionales"
            recommendations.append(msg)
        
        if academic_count > prof_count:
            msg = "• Prioriza la creación de repositorios profesionales"
            recommendations.append(msg)
        
        private_repos = [r for r in repos if r['private']]
        if private_repos:
            msg = f"• Tienes {len(private_repos)} repos privados - evalúa hacerlos públicos"
            recommendations.append(msg)
        
        no_description = [r for r in repos if not r['description']]
        if no_description:
            msg = f"• {len(no_description)} repos sin descripción - agregar documentación"
            recommendations.append(msg)
        
        if recommendations:
            panel = Panel(
                "\n".join(recommendations),
                title="🎯 Recomendaciones",
                border_style="yellow"
            )
            console.print(panel)

def main():
    parser = argparse.ArgumentParser(description='Auditoría profesional de repositorios GitHub')
    parser.add_argument('--user', '-u', default='GaweinNakaros', 
                       help='Usuario de GitHub a auditar')
    parser.add_argument('--output', '-o', default='data/audits',
                       help='Directorio de salida para reportes')
    
    args = parser.parse_args()
    
    # Crear instancia del auditor
    auditor = GitHubAuditor(args.user)
    
    # Verificar prerequisitos
    if not auditor.check_gh_cli():
        sys.exit(1)
    
    # Ejecutar auditoría
    if auditor.fetch_repositories():
        auditor.generate_report()
        console.print("\n✅ Auditoría completada exitosamente", style="green bold")
    else:
        console.print("\n❌ Error en la auditoría", style="red bold")
        sys.exit(1)

if __name__ == "__main__":
    main()
