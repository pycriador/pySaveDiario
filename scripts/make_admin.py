#!/usr/bin/env python3
"""
Script to promote any user to ADMIN role
Usage: python scripts/make_admin.py EMAIL
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def make_admin(email: str):
    """Promote user to ADMIN role"""
    from app import create_app, db
    from app.models import User, RoleEnum
    
    app = create_app()
    
    with app.app_context():
        # Find user by email
        user = User.query.filter_by(email=email.lower().strip()).first()
        
        if not user:
            print(f"❌ Usuário não encontrado: {email}")
            print("\n📋 Usuários disponíveis:")
            all_users = User.query.all()
            for u in all_users:
                role_str = u.role.value if hasattr(u.role, 'value') else str(u.role)
                print(f"   - {u.email} ({role_str})")
            return False
        
        # Check current role
        current_role = user.role.value if hasattr(user.role, 'value') else str(user.role)
        
        print(f"👤 Usuário: {user.display_name}")
        print(f"📧 Email: {user.email}")
        print(f"🎭 Papel atual: {current_role}")
        
        if user.role == RoleEnum.ADMIN:
            print(f"✅ Este usuário já é ADMIN!")
            return True
        
        # Promote to admin
        print(f"\n🔄 Promovendo para ADMIN...")
        user.role = RoleEnum.ADMIN
        db.session.commit()
        
        print(f"✅ {user.email} agora é ADMINISTRADOR!")
        print(f"🎉 Papel atualizado: {current_role} → ADMIN")
        return True

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("❌ Erro: Email não informado")
        print("\n📖 Uso:")
        print(f"   python {sys.argv[0]} EMAIL")
        print("\n📝 Exemplo:")
        print(f"   python {sys.argv[0]} usuario@gmail.com")
        sys.exit(1)
    
    email = sys.argv[1]
    
    print("🚀 Iniciando promoção para ADMIN...")
    print(f"📧 Email: {email}\n")
    
    success = make_admin(email)
    
    if success:
        print("\n✅ Operação concluída com sucesso!")
        sys.exit(0)
    else:
        print("\n❌ Operação falhou!")
        sys.exit(1)

if __name__ == '__main__':
    main()

