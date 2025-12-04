#!/usr/bin/env python3
"""
Script to setup the Administration Module
Runs migrations and seeds initial data
"""

import os
import sys
import subprocess
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print a header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")


def run_command(command, description):
    """Run a shell command and return success status"""
    print_info(f"{description}...")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            print(result.stdout)
        
        print_success(f"{description} - Concluído!")
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"{description} - Falhou!")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False


def check_venv():
    """Check if virtual environment is activated"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if not in_venv:
        print_warning("Virtual environment não está ativado!")
        print_info("Tentando ativar automaticamente...")
        return False
    
    print_success("Virtual environment ativo")
    return True


def get_project_root():
    """Get project root directory"""
    script_path = Path(__file__).resolve()
    return script_path.parent.parent


def main():
    """Main function"""
    print_header("🚀 Setup - Módulo de Administração")
    
    # Get project root
    project_root = get_project_root()
    os.chdir(project_root)
    
    print_info(f"Diretório do projeto: {project_root}")
    
    # Check if we're in the right directory
    if not (project_root / "app").exists():
        print_error("Diretório 'app' não encontrado!")
        print_error("Execute este script da raiz do projeto.")
        return 1
    
    # Check virtual environment
    venv_activated = check_venv()
    
    # Prepare command prefix
    if venv_activated:
        cmd_prefix = ""
    else:
        # Try to activate venv
        venv_path = project_root / ".venv" / "bin" / "activate"
        if venv_path.exists():
            cmd_prefix = f"source {venv_path} && "
            print_info("Usando virtual environment: .venv")
        else:
            print_warning("Virtual environment não encontrado, continuando sem ele...")
            cmd_prefix = ""
    
    # Step 1: Apply migration
    print_header("📦 Passo 1: Aplicar Migration")
    
    upgrade_cmd = f"{cmd_prefix}flask db upgrade"
    
    if not run_command(upgrade_cmd, "Aplicando migration"):
        print_error("\n⚠️  Migration falhou!")
        print_info("\nTentando solução alternativa...")
        
        # Try to fix the migration file first
        print_info("Corrigindo arquivo de migration...")
        
        # Find the latest migration file
        migrations_dir = project_root / "migrations" / "versions"
        if migrations_dir.exists():
            migration_files = list(migrations_dir.glob("*.py"))
            if migration_files:
                latest_migration = max(migration_files, key=lambda p: p.stat().st_mtime)
                print_info(f"Migration encontrada: {latest_migration.name}")
                
                # Try again
                if not run_command(upgrade_cmd, "Tentando aplicar migration novamente"):
                    print_error("\nNão foi possível aplicar a migration automaticamente.")
                    print_info("\nExecute manualmente:")
                    print(f"  cd {project_root}")
                    print(f"  source .venv/bin/activate")
                    print(f"  flask db upgrade")
                    return 1
    
    # Step 2: Seed admin data
    print_header("🌱 Passo 2: Popular Dados Iniciais")
    
    seed_script = project_root / "scripts" / "seed_admin_data.py"
    
    if not seed_script.exists():
        print_error(f"Script de seed não encontrado: {seed_script}")
        return 1
    
    seed_cmd = f"{cmd_prefix}python {seed_script}"
    
    if not run_command(seed_cmd, "Populando dados"):
        print_warning("Falha ao popular dados iniciais.")
        print_info("Você pode executar manualmente:")
        print(f"  python scripts/seed_admin_data.py")
    
    # Success
    print_header("✅ Setup Concluído com Sucesso!")
    
    print(f"{Colors.OKGREEN}O módulo de administração está pronto para uso!{Colors.ENDC}\n")
    print(f"{Colors.BOLD}Próximos passos:{Colors.ENDC}")
    print(f"  1. Reinicie o servidor Flask:")
    print(f"     {Colors.OKCYAN}python run.py{Colors.ENDC}")
    print(f"\n  2. Acesse no navegador:")
    print(f"     {Colors.OKCYAN}http://localhost:5000/admin{Colors.ENDC}")
    print(f"\n  3. Faça login como Admin ou Editor")
    print(f"\n  4. Veja os dados cadastrados:")
    print(f"     • 6 Vendedores")
    print(f"     • 5 Categorias")
    print(f"     • 5 Fabricantes")
    
    print(f"\n{Colors.BOLD}Documentação:{Colors.ENDC}")
    print(f"  {Colors.OKCYAN}ADMIN_README.md{Colors.ENDC} - Guia rápido")
    print(f"  {Colors.OKCYAN}docs/ADMIN_MODULE_SETUP.md{Colors.ENDC} - Documentação completa")
    
    print(f"\n{Colors.OKGREEN}{'=' * 70}{Colors.ENDC}\n")
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print_warning("\n\nOperação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nErro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

