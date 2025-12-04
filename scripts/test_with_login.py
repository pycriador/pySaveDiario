"""
Quick test script to demonstrate login persistence
"""

import os
from mercadolivre_selenium_scraper import MercadoLivreSeleniumScraper

def test_login_persistence():
    """Test the login persistence feature"""
    
    print("=" * 70)
    print("🧪 TESTE - Login Persistente MercadoLivre")
    print("=" * 70)
    
    # Create profile directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    user_data_dir = os.path.join(script_dir, 'chrome_profile')
    
    print(f"\n📁 Diretório do perfil: {user_data_dir}")
    
    if os.path.exists(user_data_dir):
        print("✅ Perfil já existe - tentará usar sessão salva")
    else:
        print("📝 Perfil não existe - será criado após login")
    
    scraper = None
    
    try:
        # Initialize scraper with persistent profile
        print("\n🚀 Inicializando navegador com perfil persistente...")
        scraper = MercadoLivreSeleniumScraper(
            headless=False,
            user_data_dir=user_data_dir
        )
        
        # Test with a seller
        seller_nickname = "videogstore"
        
        print(f"\n🔍 Testando acesso ao vendedor: {seller_nickname}")
        
        # Check if login is needed
        scraper.check_and_wait_for_login(seller_nickname)
        
        # Try to get first 2 pages of products (for testing)
        print("\n📦 Coletando primeiras 2 páginas de produtos (teste)...")
        products = scraper.get_seller_products(seller_nickname, max_pages=2)
        
        if products:
            print(f"\n✅ SUCESSO! Coletados {len(products)} produtos")
            print("\n📊 Primeiros 3 produtos:")
            for i, p in enumerate(products[:3], 1):
                print(f"\n{i}. {p['title'][:60]}")
                print(f"   💰 R$ {p['price']:.2f}")
                print(f"   🔗 {p['link'][:50]}...")
            
            # Save test results
            result_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'result_data')
            os.makedirs(result_dir, exist_ok=True)
            
            output_path = os.path.join(result_dir, 'test_output.json')
            scraper.save_to_json(products, output_path)
            print(f"\n💾 Resultados salvos em: {output_path}")
        else:
            print("\n⚠️ Nenhum produto encontrado")
        
        print("\n" + "=" * 70)
        print("✅ TESTE CONCLUÍDO")
        print("=" * 70)
        print("\n💡 Se o login funcionou, nas próximas execuções")
        print("   você não precisará fazer login novamente!")
        
    except Exception as e:
        print(f"\n❌ Erro durante teste: {e}")
        
    finally:
        if scraper:
            scraper.close()


if __name__ == "__main__":
    test_login_persistence()

