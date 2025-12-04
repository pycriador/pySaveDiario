"""
Script to seed initial administration data
Creates sellers, categories, and manufacturers
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Seller, Category, Manufacturer
from app.utils import slugify


def seed_sellers():
    """Seed initial sellers/marketplaces"""
    sellers_data = [
        {
            "name": "Shopee",
            "slug": "shopee",
            "description": "Marketplace online com milhões de produtos",
            "website": "https://shopee.com.br",
        },
        {
            "name": "Mercado Livre",
            "slug": "mercado-livre",
            "description": "Maior marketplace da América Latina",
            "website": "https://www.mercadolivre.com.br",
        },
        {
            "name": "Amazon",
            "slug": "amazon",
            "description": "Marketplace global com entrega rápida",
            "website": "https://www.amazon.com.br",
        },
        {
            "name": "Magazine Luiza",
            "slug": "magazine-luiza",
            "description": "Varejista brasileira com loja online",
            "website": "https://www.magazineluiza.com.br",
        },
        {
            "name": "AliExpress",
            "slug": "aliexpress",
            "description": "Marketplace internacional com produtos da China",
            "website": "https://pt.aliexpress.com",
        },
        {
            "name": "Kabum",
            "slug": "kabum",
            "description": "Especialista em tecnologia e informática",
            "website": "https://www.kabum.com.br",
        },
    ]
    
    created = 0
    for data in sellers_data:
        existing = Seller.query.filter_by(slug=data["slug"]).first()
        if not existing:
            seller = Seller(**data)
            db.session.add(seller)
            created += 1
            print(f"✅ Vendedor criado: {data['name']}")
        else:
            print(f"⏭️  Vendedor já existe: {data['name']}")
    
    return created


def seed_categories():
    """Seed initial product categories"""
    categories_data = [
        {
            "name": "Eletrônicos",
            "slug": "eletronicos",
            "description": "Produtos eletrônicos e tecnologia",
            "icon": "bi bi-laptop",
        },
        {
            "name": "Jogos",
            "slug": "jogos",
            "description": "Videogames, consoles e acessórios",
            "icon": "bi bi-controller",
        },
        {
            "name": "Casa",
            "slug": "casa",
            "description": "Produtos para casa e utilidades domésticas",
            "icon": "bi bi-house-door",
        },
        {
            "name": "Decoração",
            "slug": "decoracao",
            "description": "Itens decorativos e mobiliário",
            "icon": "bi bi-palette",
        },
        {
            "name": "Perfumes",
            "slug": "perfumes",
            "description": "Fragrâncias e produtos de perfumaria",
            "icon": "bi bi-droplet",
        },
    ]
    
    created = 0
    for data in categories_data:
        existing = Category.query.filter_by(slug=data["slug"]).first()
        if not existing:
            category = Category(**data)
            db.session.add(category)
            created += 1
            print(f"✅ Categoria criada: {data['name']}")
        else:
            print(f"⏭️  Categoria já existe: {data['name']}")
    
    return created


def seed_manufacturers():
    """Seed initial manufacturers/brands"""
    manufacturers_data = [
        {
            "name": "Nintendo",
            "slug": "nintendo",
            "description": "Fabricante japonesa de consoles e jogos",
            "website": "https://www.nintendo.com",
        },
        {
            "name": "Apple",
            "slug": "apple",
            "description": "Fabricante de dispositivos eletrônicos e computadores",
            "website": "https://www.apple.com",
        },
        {
            "name": "Sony",
            "slug": "sony",
            "description": "Conglomerado japonês de eletrônicos e entretenimento",
            "website": "https://www.sony.com",
        },
        {
            "name": "PlayStation",
            "slug": "playstation",
            "description": "Marca de consoles de videogame da Sony",
            "website": "https://www.playstation.com",
        },
        {
            "name": "Microsoft",
            "slug": "microsoft",
            "description": "Empresa de tecnologia e software",
            "website": "https://www.microsoft.com",
        },
    ]
    
    created = 0
    for data in manufacturers_data:
        existing = Manufacturer.query.filter_by(slug=data["slug"]).first()
        if not existing:
            manufacturer = Manufacturer(**data)
            db.session.add(manufacturer)
            created += 1
            print(f"✅ Fabricante criado: {data['name']}")
        else:
            print(f"⏭️  Fabricante já existe: {data['name']}")
    
    return created


def main():
    """Main function to seed all admin data"""
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("🌱 SEED - Dados Administrativos")
        print("=" * 70)
        print()
        
        # Seed sellers
        print("📦 Vendedores:")
        print("-" * 70)
        sellers_created = seed_sellers()
        print()
        
        # Seed categories
        print("🏷️  Categorias:")
        print("-" * 70)
        categories_created = seed_categories()
        print()
        
        # Seed manufacturers
        print("🏭 Fabricantes:")
        print("-" * 70)
        manufacturers_created = seed_manufacturers()
        print()
        
        # Commit all changes
        try:
            db.session.commit()
            print("=" * 70)
            print("✅ SUCESSO!")
            print("=" * 70)
            print(f"📊 Resumo:")
            print(f"   • Vendedores criados: {sellers_created}")
            print(f"   • Categorias criadas: {categories_created}")
            print(f"   • Fabricantes criados: {manufacturers_created}")
            print()
            print("💡 Acesse /admin no navegador para ver os dados cadastrados")
            print("=" * 70)
        except Exception as e:
            db.session.rollback()
            print("=" * 70)
            print("❌ ERRO ao salvar no banco de dados:")
            print(f"   {e}")
            print("=" * 70)
            return 1
        
        return 0


if __name__ == "__main__":
    exit(main())

