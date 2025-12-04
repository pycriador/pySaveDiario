#!/usr/bin/env python3
"""
Script to verify and fix admin user role
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def fix_admin_user():
    """Verify and fix admin user role"""
    from app import create_app, db
    from app.models import User, RoleEnum
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Verificando usuários...")
        
        # Get all users
        users = User.query.all()
        print(f"📊 Total de usuários: {len(users)}")
        
        admin_count = 0
        fixed_count = 0
        
        for user in users:
            role_str = user.role.value if hasattr(user.role, 'value') else str(user.role)
            print(f"   - {user.email}: {role_str} (ativo: {user.is_active})")
            
            if user.role == RoleEnum.ADMIN or role_str.upper() == 'ADMIN':
                admin_count += 1
        
        print(f"\n✅ Administradores encontrados: {admin_count}")
        
        # Ask if user wants to fix a specific user
        if admin_count == 0:
            print("\n⚠️  AVISO: Nenhum administrador encontrado!")
            email = input("Digite o email do usuário que deve ser ADMIN: ").strip()
            
            if email:
                user = User.query.filter_by(email=email.lower()).first()
                if user:
                    print(f"\n👤 Usuário encontrado: {user.display_name}")
                    print(f"   Papel atual: {user.role}")
                    
                    confirm = input(f"\nDeseja promover '{user.email}' para ADMIN? (s/n): ").strip().lower()
                    if confirm == 's':
                        user.role = RoleEnum.ADMIN
                        db.session.commit()
                        print(f"✅ {user.email} agora é ADMIN!")
                        fixed_count += 1
                    else:
                        print("❌ Operação cancelada")
                else:
                    print(f"❌ Usuário '{email}' não encontrado")
        
        # Check for users with invalid roles
        print("\n🔍 Verificando papéis inválidos...")
        for user in users:
            try:
                # Try to access role value
                role_value = user.role.value if hasattr(user.role, 'value') else str(user.role)
                if role_value.upper() not in ['ADMIN', 'EDITOR', 'MEMBER']:
                    print(f"⚠️  Papel inválido encontrado: {user.email} = {role_value}")
                    user.role = RoleEnum.MEMBER
                    db.session.commit()
                    print(f"   → Corrigido para MEMBER")
                    fixed_count += 1
            except Exception as e:
                print(f"❌ Erro ao verificar {user.email}: {e}")
        
        if fixed_count > 0:
            print(f"\n✅ {fixed_count} usuário(s) corrigido(s)!")
        else:
            print("\n✅ Todos os usuários estão OK!")

if __name__ == '__main__':
    fix_admin_user()

