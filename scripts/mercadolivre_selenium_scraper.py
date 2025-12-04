"""
MercadoLivre Product Scraper using Selenium
This method works around 403 errors by using a real browser
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import csv
from typing import List, Dict
from datetime import datetime


class MercadoLivreSeleniumScraper:
    """Selenium-based scraper for MercadoLivre"""
    
    def __init__(self, headless: bool = False, user_data_dir: str = None):
        """
        Initialize the scraper
        
        Args:
            headless: Run browser in headless mode (no window)
            user_data_dir: Path to Chrome user data directory for persistent sessions
        """
        print("🚀 Inicializando navegador...")
        
        options = Options()
        
        if headless:
            options.add_argument('--headless')
        
        # Use persistent user data directory to save login session
        if user_data_dir:
            import os
            # Create directory if it doesn't exist
            os.makedirs(user_data_dir, exist_ok=True)
            options.add_argument(f'--user-data-dir={user_data_dir}')
            print(f"📁 Usando perfil persistente: {user_data_dir}")
        
        # Additional options to avoid detection
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # User agent
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            
            # Remove automation flags
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                '''
            })
            
            print("✅ Navegador inicializado com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar navegador: {e}")
            print("\n💡 Certifique-se de ter instalado:")
            print("   pip3 install selenium webdriver-manager")
            raise
    
    def check_and_wait_for_login(self, seller_nickname: str):
        """
        Check if user is logged in and wait for manual login if needed
        
        Args:
            seller_nickname: Seller nickname to test access
        """
        print("\n🔐 Verificando se é necessário fazer login...")
        
        # Try to access seller page (Brazil store format)
        test_url = f"https://lista.mercadolivre.com.br/pagina/{seller_nickname}/"
        self.driver.get(test_url)
        time.sleep(3)
        
        # Check if we're redirected to login or verification page
        current_url = self.driver.current_url
        page_source = self.driver.page_source.lower()
        
        needs_login = False
        
        # Check for login/verification indicators
        if 'login' in current_url or 'account-verification' in current_url or 'webdevice' in current_url:
            needs_login = True
        elif 'faça login' in page_source or 'iniciar sessão' in page_source:
            needs_login = True
        elif 'verificação' in page_source or 'verification' in page_source:
            needs_login = True
        
        if needs_login:
            print("\n" + "=" * 70)
            print("⚠️  É NECESSÁRIO FAZER LOGIN NO MERCADOLIVRE")
            print("=" * 70)
            print("\n📝 INSTRUÇÕES:")
            print("   1. Uma janela do Chrome foi aberta")
            print("   2. Faça login na sua conta do MercadoLivre")
            print("   3. Aguarde até ver os produtos do vendedor")
            print("   4. Volte aqui e pressione ENTER para continuar")
            print("\n💡 DICA: A sessão será salva e você não precisará")
            print("   fazer login novamente nas próximas execuções!")
            print("\n" + "=" * 70)
            
            input("\n⏸️  Pressione ENTER após fazer login... ")
            
            # Verify login was successful
            self.driver.get(test_url)
            time.sleep(3)
            
            current_url = self.driver.current_url
            if 'login' in current_url or 'account-verification' in current_url:
                print("\n⚠️  Parece que ainda não está logado.")
                print("Continuando mesmo assim...")
            else:
                print("\n✅ Login realizado com sucesso!")
                print("🔐 Sessão salva localmente para próximas execuções")
        else:
            print("✅ Acesso OK - não é necessário login (ou já está logado)")
    
    def get_seller_products(self, seller_nickname: str, max_pages: int = None) -> List[Dict]:
        """
        Get products from a seller
        
        Args:
            seller_nickname: Seller nickname
            max_pages: Maximum number of pages to scrape (None = all pages)
            
        Returns:
            List of product dictionaries
        """
        all_products = []
        page = 1
        consecutive_empty_pages = 0  # Counter for empty pages
        MAX_EMPTY_PAGES = 3  # Stop after 3 consecutive empty pages
        
        print(f"\n🔍 Buscando produtos do vendedor: {seller_nickname}")
        if max_pages:
            print(f"📄 Limite: {max_pages} páginas")
        else:
            print(f"📄 Modo: TODAS as páginas (até o fim)")
        
        while True:
            # Check if we reached max_pages limit
            if max_pages and page > max_pages:
                print(f"\n✓ Limite de {max_pages} páginas atingido")
                break
            # Build URL (Brazil store page format)
            offset = (page - 1) * 50  # MercadoLivre shows ~50 items per page
            if page == 1:
                url = f"https://lista.mercadolivre.com.br/pagina/{seller_nickname}/"
            else:
                url = f"https://lista.mercadolivre.com.br/pagina/{seller_nickname}/_Desde_{offset + 1}"
            
            print(f"\n📄 Carregando página {page}...")
            
            try:
                self.driver.get(url)
                time.sleep(3)  # Wait for page to load
                
                # Scroll to load lazy images
                self._scroll_page()
                
                # Extract products
                products = self._extract_products_from_current_page()
                
                if not products:
                    consecutive_empty_pages += 1
                    print(f"⚠️ Página {page} vazia ({consecutive_empty_pages}/{MAX_EMPTY_PAGES})")
                    
                    if consecutive_empty_pages >= MAX_EMPTY_PAGES:
                        print(f"✓ Parando após {MAX_EMPTY_PAGES} páginas vazias consecutivas")
                        break
                    
                    # Try next page anyway (might be a loading issue)
                    page += 1
                    time.sleep(3)
                    continue
                
                # Reset empty page counter
                consecutive_empty_pages = 0
                
                print(f"📦 Encontrados {len(products)} produtos nesta página")
                print(f"📊 Total acumulado: {len(all_products) + len(products)} produtos")
                all_products.extend(products)
                
                # Check if there's a next page
                if not self._has_next_page():
                    print("✓ Última página alcançada - não há botão 'Próxima'")
                    break
                
                # Increment page counter
                page += 1
                
                time.sleep(2)  # Be nice to the server
                
            except Exception as e:
                print(f"⚠️ Erro na página {page}: {e}")
                print("Continuando com os produtos já coletados...")
                break
        
        print(f"\n✅ Total de produtos coletados: {len(all_products)}")
        return all_products
    
    def _scroll_page(self):
        """Scroll the page to load lazy-loaded content"""
        try:
            # Scroll in steps
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3 * {});".format(i + 1))
                time.sleep(0.5)
        except Exception as e:
            print(f"⚠️ Erro ao fazer scroll: {e}")
    
    def _has_next_page(self) -> bool:
        """Check if there is a next page button"""
        try:
            # Try multiple selectors for next page button
            selectors = [
                (By.CLASS_NAME, "andes-pagination__button--next"),
                (By.CSS_SELECTOR, "a.andes-pagination__button--next"),
                (By.CSS_SELECTOR, "li.andes-pagination__button--next a"),
                (By.XPATH, "//a[contains(@title, 'Siguiente') or contains(@title, 'Próxima')]"),
            ]
            
            for selector_type, selector_value in selectors:
                try:
                    next_buttons = self.driver.find_elements(selector_type, selector_value)
                    if next_buttons:
                        button = next_buttons[0]
                        # Check if button is enabled and visible
                        if button.is_displayed() and button.is_enabled():
                            return True
                except:
                    continue
            
            return False
        except Exception as e:
            print(f"⚠️ Erro ao verificar próxima página: {e}")
            return False
    
    def _extract_products_from_current_page(self) -> List[Dict]:
        """Extract products from the current page"""
        products = []
        
        try:
            # Wait for products to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ui-search-layout__item"))
            )
            
            # Find product items
            items = self.driver.find_elements(By.CLASS_NAME, "ui-search-layout__item")
            
            for item in items:
                try:
                    product = self._extract_product_data(item)
                    if product:
                        products.append(product)
                except Exception as e:
                    print(f"⚠️ Erro ao extrair produto: {e}")
                    continue
            
        except Exception as e:
            print(f"⚠️ Erro ao localizar produtos: {e}")
        
        return products
    
    def _extract_product_data(self, item) -> Dict:
        """Extract data from a product element"""
        try:
            # Title - try multiple selectors
            title = "N/A"
            try:
                title = item.find_element(By.CLASS_NAME, "ui-search-item__title").text
            except:
                try:
                    title = item.find_element(By.CSS_SELECTOR, "h2.poly-box").text
                except:
                    try:
                        # Alternative: get from link title attribute
                        title = item.find_element(By.TAG_NAME, "a").get_attribute("title")
                    except:
                        pass
            
            # Price - try multiple selectors
            price = 0.0
            try:
                price_int = item.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text
                price_int = price_int.replace(".", "").replace(",", ".")
                price = float(price_int)
            except:
                try:
                    price_elem = item.find_element(By.CSS_SELECTOR, "span.andes-money-amount__fraction")
                    price_int = price_elem.text.replace(".", "").replace(",", ".")
                    price = float(price_int)
                except:
                    pass
            
            # Link - try multiple selectors
            link = "N/A"
            try:
                link = item.find_element(By.CLASS_NAME, "ui-search-link").get_attribute("href")
            except:
                try:
                    link = item.find_element(By.CSS_SELECTOR, "a.ui-search-item__group__element").get_attribute("href")
                except:
                    try:
                        # Get any link in the item
                        link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                    except:
                        pass
            
            # Image
            try:
                image = item.find_element(By.TAG_NAME, "img").get_attribute("src")
            except:
                image = "N/A"
            
            # Extract ID from link or data attributes
            product_id = "N/A"
            if link and link != "N/A":
                import re
                match = re.search(r'MLB-?(\d+)', link)
                if match:
                    product_id = f"MLB{match.group(1)}"
            
            # Try to get ID from data attribute if link didn't work
            if product_id == "N/A":
                try:
                    product_id = item.get_attribute("data-id")
                except:
                    pass
            
            # Free shipping
            free_shipping = False
            try:
                shipping_elem = item.find_element(By.CLASS_NAME, "poly-component__shipping")
                if "grátis" in shipping_elem.text.lower():
                    free_shipping = True
            except:
                pass
            
            # Condition
            condition = "N/A"
            try:
                condition_text = item.text.lower()
                if "novo" in condition_text:
                    condition = "new"
                elif "usado" in condition_text:
                    condition = "used"
            except:
                pass
            
            product = {
                'id': product_id,
                'title': title,
                'price': price,
                'currency_id': 'BRL',
                'link': link,
                'image': image,
                'condition': condition,
                'free_shipping': free_shipping,
                'collected_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            
            return product
            
        except Exception as e:
            print(f"⚠️ Erro ao processar produto: {e}")
            return None
    
    def get_product_description(self, product_link: str) -> str:
        """
        Get detailed description of a product
        
        Args:
            product_link: Product URL
            
        Returns:
            Product description
        """
        try:
            self.driver.get(product_link)
            time.sleep(2)
            
            # Try to find description
            try:
                desc_elem = self.driver.find_element(By.CLASS_NAME, "ui-pdp-description__content")
                return desc_elem.text
            except:
                return "N/A"
                
        except Exception as e:
            print(f"⚠️ Erro ao buscar descrição: {e}")
            return "N/A"
    
    def close(self):
        """Close the browser"""
        try:
            self.driver.quit()
            print("\n✅ Navegador fechado")
        except:
            pass
    
    def save_to_json(self, products: List[Dict], filename: str):
        """Save products to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=2)
            print(f"💾 Dados salvos em: {filename}")
        except Exception as e:
            print(f"❌ Erro ao salvar JSON: {e}")
    
    def save_to_csv(self, products: List[Dict], filename: str):
        """Save products to CSV file"""
        if not products:
            print("⚠️ Nenhum produto para salvar")
            return
        
        try:
            keys = products[0].keys()
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(products)
            print(f"💾 Dados salvos em: {filename}")
        except Exception as e:
            print(f"❌ Erro ao salvar CSV: {e}")


def main():
    """Main function"""
    import os
    
    print("=" * 70)
    print("🛒 MercadoLivre Product Scraper - Selenium Edition")
    print("=" * 70)
    print("\n✨ Este método usa navegador real para evitar bloqueios!")
    print("💾 Sua sessão será salva e você não precisará fazer login novamente!")
    print("⚠️  Certifique-se de ter instalado: pip3 install selenium webdriver-manager\n")
    
    seller_nickname = input("📝 Digite o nickname do vendedor: ").strip()
    
    if not seller_nickname:
        print("❌ Nickname não pode estar vazio")
        return
    
    # Ask for headless mode
    headless_input = input("\n🖥️  Executar em modo invisível? (s/N): ").strip().lower()
    headless = headless_input == 's'
    
    if headless:
        print("\n⚠️  ATENÇÃO: Modo invisível não permite login manual!")
        print("Use modo visível (N) se precisar fazer login.")
        confirm = input("Continuar mesmo assim? (s/N): ").strip().lower()
        if confirm != 's':
            print("❌ Operação cancelada")
            return
    
    scraper = None
    
    try:
        # Create user data directory for persistent session
        script_dir = os.path.dirname(os.path.abspath(__file__))
        user_data_dir = os.path.join(script_dir, 'chrome_profile')
        
        scraper = MercadoLivreSeleniumScraper(headless=headless, user_data_dir=user_data_dir)
        
        # Check if login is needed and wait for manual login
        if not headless:
            scraper.check_and_wait_for_login(seller_nickname)
        
        # Ask how many pages to scrape
        print("\n" + "=" * 70)
        print("📄 Quantas páginas deseja coletar?")
        print("=" * 70)
        print("1. TODAS as páginas (recomendado)")
        print("2. Número específico de páginas")
        page_choice = input("\nEscolha (1-2): ").strip()
        
        max_pages = None  # Default: all pages
        if page_choice == '2':
            try:
                max_pages = int(input("Digite o número de páginas: ").strip())
                print(f"✓ Será coletado até {max_pages} páginas")
            except ValueError:
                print("⚠️ Valor inválido. Coletando TODAS as páginas.")
                max_pages = None
        else:
            print("✓ Será coletado TODAS as páginas disponíveis")
        
        # Get products
        products = scraper.get_seller_products(seller_nickname, max_pages=max_pages)
        
        if not products:
            print("\n⚠️ Nenhum produto encontrado")
            return
        
        # Show sample
        print("\n" + "=" * 70)
        print("📊 Amostra dos dados coletados:")
        print("=" * 70)
        
        for i, product in enumerate(products[:5], 1):
            print(f"\n{i}. {product['title'][:60]}")
            print(f"   💰 Preço: R$ {product['price']:.2f}")
            print(f"   🆔 ID: {product['id']}")
            print(f"   🚚 Frete grátis: {'Sim' if product['free_shipping'] else 'Não'}")
        
        # Save files
        print("\n" + "=" * 70)
        print("💾 Escolha o formato de exportação:")
        print("1. JSON")
        print("2. CSV")
        print("3. Ambos")
        choice = input("Escolha (1-3): ").strip()
        
        # Create result_data directory if it doesn't exist
        result_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'result_data')
        os.makedirs(result_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"ml_{seller_nickname}_{timestamp}"
        
        if choice in ['1', '3']:
            json_path = os.path.join(result_dir, f"{base_filename}.json")
            scraper.save_to_json(products, json_path)
        
        if choice in ['2', '3']:
            csv_path = os.path.join(result_dir, f"{base_filename}.csv")
            scraper.save_to_csv(products, csv_path)
        
        print("\n✅ Processo concluído!")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        
    finally:
        if scraper:
            scraper.close()
        print("=" * 70)


if __name__ == "__main__":
    main()

