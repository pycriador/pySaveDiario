"""
Quick test to validate the correct URL format for MercadoLivre seller pages
"""

import os
from mercadolivre_selenium_scraper import MercadoLivreSeleniumScraper
from selenium.webdriver.common.by import By
import time

def test_url_formats():
    """Test different URL formats to find the correct one"""
    
    print("=" * 70)
    print("🧪 TESTE - Formato de URL do MercadoLivre")
    print("=" * 70)
    
    seller = "videogstore"
    
    # URLs to test
    urls_to_test = [
        f"https://lista.mercadolivre.com.br/pagina/{seller}/",
        f"https://lista.mercadolivre.com.br/{seller}",
        f"https://lista.mercadolivre.com.br/_Tienda_{seller}",
    ]
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    user_data_dir = os.path.join(script_dir, 'chrome_profile')
    
    scraper = None
    
    try:
        print("\n🚀 Inicializando navegador...")
        scraper = MercadoLivreSeleniumScraper(
            headless=False,
            user_data_dir=user_data_dir
        )
        
        for i, url in enumerate(urls_to_test, 1):
            print(f"\n📝 Teste {i}/{len(urls_to_test)}")
            print(f"🔗 URL: {url}")
            
            scraper.driver.get(url)
            time.sleep(5)  # Wait for page to load
            
            # Check final URL after redirects
            final_url = scraper.driver.current_url
            print(f"✓ URL final: {final_url}")
            
            # Check if products are visible
            try:
                items = scraper.driver.find_elements(By.CLASS_NAME, "ui-search-layout__item")
                if not items:
                    # Try alternative selector
                    items = scraper.driver.find_elements(By.CSS_SELECTOR, "li[class*='ui-search']")
                
                if items:
                    print(f"✅ SUCESSO! Encontrados {len(items)} produtos")
                    print(f"✅ URL CORRETA: {url}")
                    
                    # Show first product title as proof
                    try:
                        first_title = items[0].text.split('\n')[0]
                        print(f"📦 Primeiro produto: {first_title[:60]}...")
                    except:
                        pass
                    
                    break
                else:
                    print(f"⚠️ Nenhum produto encontrado")
                    
            except Exception as e:
                print(f"❌ Erro ao buscar produtos: {e}")
            
            # Check if login is required
            page_source = scraper.driver.page_source.lower()
            if 'login' in final_url or 'faça login' in page_source:
                print(f"🔐 Página requer login")
            
            time.sleep(2)
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        
    finally:
        if scraper:
            input("\n⏸️  Pressione ENTER para fechar o navegador...")
            scraper.close()


if __name__ == "__main__":
    test_url_formats()

