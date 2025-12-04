#!/usr/bin/env python3
"""
Script to create users in the database
Interactive script with role selection (admin, editor, viewer)
"""

import sys
import os
from getpass import getpass

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, RoleEnum
from werkzeug.security import generate_password_hash


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


def get_input(prompt, default=None):
    """Get input from user"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()


def get_password():
    """Get password securely"""
    while True:
        password = getpass("Senha: ")
        if len(password) < 6:
            print_error("Senha deve ter pelo menos 6 caracteres!")
            continue
        
        confirm = getpass("Confirme a senha: ")
        if password != confirm:
            print_error("Senhas não coincidem!")
            continue
        
        return password


def get_role():
    """Get user role"""
    print(f"\n{Colors.BOLD}Escolha o tipo de usuário:{Colors.ENDC}")
    print(f"  {Colors.OKGREEN}1{Colors.ENDC} - {Colors.BOLD}Admin{Colors.ENDC} (Acesso total, pode criar/editar/deletar tudo)")
    print(f"  {Colors.OKBLUE}2{Colors.ENDC} - {Colors.BOLD}Editor{Colors.ENDC} (Pode criar e editar, mas não deletar)")
    print(f"  {Colors.OKCYAN}3{Colors.ENDC} - {Colors.BOLD}Viewer{Colors.ENDC} (Apenas visualizar, sem edição)")
    
    while True:
        choice = input(f"\n{Colors.BOLD}Escolha (1-3):{Colors.ENDC} ").strip()
        
        if choice == "1":
            return RoleEnum.ADMIN
        elif choice == "2":
            return RoleEnum.EDITOR
        elif choice == "3":
            return RoleEnum.VIEWER
        else:
            print_error("Opção inválida! Digite 1, 2 ou 3.")


def list_existing_users(app):
    """List existing users"""
    with app.app_context():
        users = User.query.all()
        
        if not users:
            print_info("Nenhum usuário cadastrado no banco de dados.")
            return
        
        print(f"\n{Colors.BOLD}Usuários existentes:{Colors.ENDC}")
        print(f"{Colors.BOLD}{'ID':<5} {'Email':<30} {'Nome':<25} {'Função':<10}{Colors.ENDC}")
        print("-" * 70)
        
        for user in users:
            role_color = {
                'admin': Colors.OKGREEN,
                'editor': Colors.OKBLUE,
                'viewer': Colors.OKCYAN,
            }.get(user.role.value, Colors.ENDC)
            
            print(f"{user.id:<5} {user.email:<30} {user.full_name:<25} {role_color}{user.role.value}{Colors.ENDC}")


def create_user(app):
    """Create a new user"""
    with app.app_context():
        print_header("👤 Criar Novo Usuário")
        
        # Get user information
        print(f"{Colors.BOLD}Informações do usuário:{Colors.ENDC}\n")
        
        # Email
        while True:
            email = get_input("Email").lower()
            if not email:
                print_error("Email não pode estar vazio!")
                continue
            
            # Check if email already exists
            existing = User.query.filter_by(email=email).first()
            if existing:
                print_error(f"Já existe um usuário com o email: {email}")
                continue
            
            break
        
        # Full name
        full_name = get_input("Nome completo")
        if not full_name:
            full_name = email.split('@')[0]
            print_info(f"Nome definido como: {full_name}")
        
        # Password
        password = get_password()
        
        # Role
        role = get_role()
        
        # Confirmation
        print(f"\n{Colors.BOLD}Confirme os dados:{Colors.ENDC}")
        print(f"  Email: {Colors.OKCYAN}{email}{Colors.ENDC}")
        print(f"  Nome: {Colors.OKCYAN}{full_name}{Colors.ENDC}")
        print(f"  Função: {Colors.OKCYAN}{role.value}{Colors.ENDC}")
        
        confirm = input(f"\n{Colors.BOLD}Criar usuário? (s/N):{Colors.ENDC} ").strip().lower()
        
        if confirm != 's':
            print_warning("Operação cancelada.")
            return False
        
        # Create user
        try:
            user = User(
                email=email,
                full_name=full_name,
                password_hash=generate_password_hash(password),
                role=role
            )
            
            db.session.add(user)
            db.session.commit()
            
            print_success(f"Usuário '{full_name}' criado com sucesso!")
            print_info(f"ID: {user.id}")
            print_info(f"Email: {user.email}")
            print_info(f"Função: {user.role.value}")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print_error(f"Erro ao criar usuário: {e}")
            return False


def delete_user(app):
    """Delete a user"""
    with app.app_context():
        print_header("🗑️  Deletar Usuário")
        
        # List users
        users = User.query.all()
        if not users:
            print_warning("Nenhum usuário cadastrado para deletar.")
            return False
        
        print(f"\n{Colors.BOLD}Usuários disponíveis:{Colors.ENDC}")
        for user in users:
            print(f"  {user.id} - {user.email} ({user.full_name}) - {user.role.value}")
        
        # Get user ID
        user_id = input(f"\n{Colors.BOLD}Digite o ID do usuário para deletar (ou 'c' para cancelar):{Colors.ENDC} ").strip()
        
        if user_id.lower() == 'c':
            print_warning("Operação cancelada.")
            return False
        
        try:
            user_id = int(user_id)
        except ValueError:
            print_error("ID inválido!")
            return False
        
        user = User.query.get(user_id)
        if not user:
            print_error(f"Usuário com ID {user_id} não encontrado!")
            return False
        
        # Confirmation
        print(f"\n{Colors.WARNING}Você está prestes a deletar:{Colors.ENDC}")
        print(f"  Email: {user.email}")
        print(f"  Nome: {user.full_name}")
        print(f"  Função: {user.role.value}")
        
        confirm = input(f"\n{Colors.BOLD}{Colors.FAIL}Tem certeza? (digite 'DELETAR' para confirmar):{Colors.ENDC} ").strip()
        
        if confirm != 'DELETAR':
            print_warning("Operação cancelada.")
            return False
        
        try:
            db.session.delete(user)
            db.session.commit()
            print_success(f"Usuário '{user.email}' deletado com sucesso!")
            return True
        except Exception as e:
            db.session.rollback()
            print_error(f"Erro ao deletar usuário: {e}")
            return False


def main_menu(app):
    """Main menu"""
    while True:
        print_header("👥 Gerenciamento de Usuários")
        
        print(f"{Colors.BOLD}O que você deseja fazer?{Colors.ENDC}\n")
        print(f"  {Colors.OKGREEN}1{Colors.ENDC} - Criar novo usuário")
        print(f"  {Colors.OKBLUE}2{Colors.ENDC} - Listar usuários existentes")
        print(f"  {Colors.FAIL}3{Colors.ENDC} - Deletar usuário")
        print(f"  {Colors.WARNING}4{Colors.ENDC} - Sair")
        
        choice = input(f"\n{Colors.BOLD}Escolha (1-4):{Colors.ENDC} ").strip()
        
        if choice == "1":
            create_user(app)
            input(f"\n{Colors.OKCYAN}Pressione ENTER para continuar...{Colors.ENDC}")
        elif choice == "2":
            list_existing_users(app)
            input(f"\n{Colors.OKCYAN}Pressione ENTER para continuar...{Colors.ENDC}")
        elif choice == "3":
            delete_user(app)
            input(f"\n{Colors.OKCYAN}Pressione ENTER para continuar...{Colors.ENDC}")
        elif choice == "4":
            print_info("Saindo...")
            break
        else:
            print_error("Opção inválida!")


def main():
    """Main function"""
    app = create_app()
    
    print_header("🚀 Sistema de Gerenciamento de Usuários")
    print_info(f"Banco de dados: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    # Check if running in interactive mode or with arguments
    if len(sys.argv) > 1:
        # Quick mode - create user from command line arguments
        if sys.argv[1] == '--list':
            list_existing_users(app)
            return 0
        elif sys.argv[1] == '--quick':
            with app.app_context():
                if len(sys.argv) < 5:
                    print_error("Uso: python create_user.py --quick <email> <nome> <senha> <role>")
                    print_info("Role: admin, editor, ou viewer")
                    return 1
                
                email = sys.argv[2]
                full_name = sys.argv[3]
                password = sys.argv[4]
                role_str = sys.argv[5].lower()
                
                role_map = {
                    'admin': RoleEnum.ADMIN,
                    'editor': RoleEnum.EDITOR,
                    'viewer': RoleEnum.VIEWER,
                }
                
                if role_str not in role_map:
                    print_error("Role inválido! Use: admin, editor, ou viewer")
                    return 1
                
                user = User(
                    email=email,
                    full_name=full_name,
                    password_hash=generate_password_hash(password),
                    role=role_map[role_str]
                )
                
                db.session.add(user)
                db.session.commit()
                
                print_success(f"Usuário '{full_name}' criado com sucesso!")
                return 0
    else:
        # Interactive mode
        main_menu(app)
    
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

