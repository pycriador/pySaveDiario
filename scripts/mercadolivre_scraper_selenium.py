"""
MercadoLivre Product Scraper using Web Scraping
Alternative method when API returns 403 errors
Uses BeautifulSoup for simple scraping without browser automation
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from typing import List, Dict, Optional
from datetime import datetime
import re


class MercadoLivreWebScraper:
    """Web scraper for MercadoLivre products"""
    
    def __init__(self):
        """Initialize the scraper"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
        })
    
    def get_seller_products(self, seller_nickname: str, max_pages: int = 10) -> List[Dict]:
        """
        Get products from seller using web scraping
        
        Args:
            seller_nickname: Seller nickname
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of product dictionaries
        """
        all_products = []
        
        print(f"🔍 Buscando produtos do vendedor: {seller_nickname}")
        print(f"📝 Método: Web Scraping (evita erro 403)")
        
        for page in range(1, max_pages + 1):
            # Build search URL
            offset = (page - 1) * 48  # MercadoLivre shows 48 items per page
            
            if page == 1:
                url = f"https://lista.mercadolivre.com.br/_Tienda_{seller_nickname}"
            else:
                url = f"https://lista.mercadolivre.com.br/_Tienda_{seller_nickname}_Desde_{offset + 1}"
            
            print(f"\n🔄 Página {page} - {url}")
            
            try:
                response = self.session.get(url, timeout=15)
                
                if response.status_code == 404:
                    print(f"⚠️ Vendedor não encontrado ou não tem mais produtos")
                    break
                
                if response.status_code != 200:
                    print(f"❌ Erro: Status {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find product listings
                products = self._extract_products_from_page(soup)
                
                if not products:
                    print(f"✓ Fim dos produtos (página {page})")
                    break
                
                print(f"📦 Encontrados {len(products)} produtos nesta página")
                all_products.extend(products)
                
                # Be nice to the server
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Erro ao processar página {page}: {e}")
                continue
        
        print(f"\n✅ Total de produtos coletados: {len(all_products)}")
        return all_products
    
    def _extract_products_from_page(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract product information from page HTML
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            List of product dictionaries
        """
        products = []
        
        # Try to find product items
        # MercadoLivre uses different class names, try multiple selectors
        items = soup.find_all('li', class_=re.compile(r'ui-search-layout__item'))
        
        if not items:
            items = soup.find_all('div', class_=re.compile(r'ui-search-result'))
        
        for item in items:
            try:
                product = self._extract_product_data(item)
                if product:
                    products.append(product)
            except Exception as e:
                print(f"⚠️ Erro ao extrair produto: {e}")
                continue
        
        return products
    
    def _extract_product_data(self, item) -> Optional[Dict]:
        """
        Extract data from a single product element
        
        Args:
            item: BeautifulSoup element
            
        Returns:
            Product dictionary
        """
        try:
            # Title
            title_elem = item.find('h2', class_=re.compile(r'ui-search-item__title'))
            if not title_elem:
                title_elem = item.find('a', class_=re.compile(r'ui-search-link'))
            title = title_elem.get_text(strip=True) if title_elem else 'N/A'
            
            # Price
            price_elem = item.find('span', class_=re.compile(r'andes-money-amount__fraction'))
            if price_elem:
                price_text = price_elem.get_text(strip=True).replace('.', '').replace(',', '.')
                try:
                    price = float(price_text)
                except:
                    price = 0
            else:
                price = 0
            
            # Link
            link_elem = item.find('a', class_=re.compile(r'ui-search-link'))
            link = link_elem.get('href') if link_elem else 'N/A'
            
            # Extract ID from link
            product_id = 'N/A'
            if link and link != 'N/A':
                match = re.search(r'MLB-?(\d+)', link)
                if match:
                    product_id = f"MLB{match.group(1)}"
            
            # Image
            img_elem = item.find('img', class_=re.compile(r'ui-search-result-image'))
            image = img_elem.get('src') if img_elem else 'N/A'
            
            # Condition (new/used)
            condition = 'N/A'
            condition_elem = item.find('span', class_=re.compile(r'ui-search-item__condition'))
            if condition_elem:
                cond_text = condition_elem.get_text(strip=True).lower()
                if 'novo' in cond_text:
                    condition = 'new'
                elif 'usado' in cond_text:
                    condition = 'used'
            
            # Shipping info
            free_shipping = False
            shipping_elem = item.find('p', class_=re.compile(r'ui-search-item__shipping'))
            if shipping_elem and 'frete grátis' in shipping_elem.get_text(strip=True).lower():
                free_shipping = True
            
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
                'description': 'N/A (use get_product_details para descrição completa)'
            }
            
            return product
            
        except Exception as e:
            print(f"⚠️ Erro ao processar item: {e}")
            return None
    
    def get_product_details(self, product_id: str) -> Optional[str]:
        """
        Get detailed description of a product
        
        Args:
            product_id: Product ID (e.g., MLB123456789)
            
        Returns:
            Product description
        """
        try:
            url = f"https://produto.mercadolivre.com.br/{product_id}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Try to find description
                desc_elem = soup.find('div', class_=re.compile(r'ui-pdp-description'))
                if desc_elem:
                    return desc_elem.get_text(strip=True)
                
                # Alternative selector
                desc_elem = soup.find('p', class_=re.compile(r'ui-pdp-description__content'))
                if desc_elem:
                    return desc_elem.get_text(strip=True)
            
            return 'N/A'
            
        except Exception as e:
            print(f"⚠️ Erro ao buscar descrição: {e}")
            return 'N/A'
    
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
    print("=" * 70)
    print("🛒 MercadoLivre Product Scraper - Web Scraping Edition")
    print("=" * 70)
    print("\n✨ Este script usa web scraping para evitar erros 403 da API")
    print("💡 Funciona com o nickname do vendedor diretamente!\n")
    
    seller_nickname = input("📝 Digite o nickname do vendedor: ").strip()
    
    if not seller_nickname:
        print("❌ Nickname não pode estar vazio")
        return
    
    scraper = MercadoLivreWebScraper()
    
    # Get products
    products = scraper.get_seller_products(seller_nickname, max_pages=5)
    
    if not products:
        print("\n⚠️ Nenhum produto encontrado")
        print("\n💡 Dicas:")
        print("1. Verifique se o nickname está correto")
        print("2. Acesse: https://listado.mercadolivre.com.br/SEU_NICKNAME")
        print("3. Veja se aparecem produtos")
        return
    
    # Show sample
    print("\n" + "=" * 70)
    print("📊 Amostra dos dados coletados:")
    print("=" * 70)
    
    for i, product in enumerate(products[:5], 1):
        print(f"\n{i}. {product['title'][:60]}...")
        print(f"   💰 Preço: R$ {product['price']:.2f}")
        print(f"   🆔 ID: {product['id']}")
        print(f"   🚚 Frete grátis: {'Sim' if product['free_shipping'] else 'Não'}")
        print(f"   🔗 {product['link'][:60]}...")
    
    # Save files
    print("\n" + "=" * 70)
    print("💾 Escolha o formato de exportação:")
    print("1. JSON")
    print("2. CSV")
    print("3. Ambos")
    choice = input("Escolha (1-3): ").strip()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = f"ml_{seller_nickname}_{timestamp}"
    
    if choice in ['1', '3']:
        scraper.save_to_json(products, f"{base_filename}.json")
    
    if choice in ['2', '3']:
        scraper.save_to_csv(products, f"{base_filename}.csv")
    
    print("\n✅ Processo concluído!")
    print("=" * 70)


if __name__ == "__main__":
    main()

