"""
MercadoLivre Product Scraper
Script to collect products from a MercadoLivre seller including price, description and title.
"""

import requests
import json
import csv
from typing import List, Dict, Optional
from datetime import datetime
import time


class MercadoLivreScraper:
    """Scraper for MercadoLivre products by seller"""
    
    BASE_URL = "https://api.mercadolibre.com"
    
    def __init__(self, country_code: str = "MLB"):
        """
        Initialize the scraper
        
        Args:
            country_code: Country code (MLB for Brazil, MLA for Argentina, etc.)
        """
        self.country_code = country_code
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.mercadolivre.com.br/',
            'Origin': 'https://www.mercadolivre.com.br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        })
    
    def get_seller_info(self, seller_nickname: str) -> Optional[Dict]:
        """
        Get seller information to obtain the numeric seller ID
        
        Args:
            seller_nickname: The seller nickname
            
        Returns:
            Seller information dictionary
        """
        try:
            url = f"{self.BASE_URL}/sites/{self.country_code}/search"
            params = {
                'nickname': seller_nickname,
                'limit': 1
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = data.get('results', [])
            if results:
                seller = results[0].get('seller', {})
                return seller
            
            return None
            
        except Exception as e:
            print(f"⚠️ Erro ao buscar informações do vendedor: {e}")
            return None
    
    def get_seller_items(self, seller_id: str, limit: int = 50) -> List[Dict]:
        """
        Get all items from a seller
        
        Args:
            seller_id: The seller ID or nickname
            limit: Number of items per page (max 50)
            
        Returns:
            List of product dictionaries
        """
        all_products = []
        offset = 0
        
        print(f"🔍 Buscando produtos do vendedor: {seller_id}")
        
        # Try to get numeric seller ID if nickname was provided
        seller_info = self.get_seller_info(seller_id)
        if seller_info:
            numeric_id = seller_info.get('id')
            if numeric_id:
                print(f"✓ ID numérico do vendedor: {numeric_id}")
                seller_id = str(numeric_id)
        
        while True:
            url = f"{self.BASE_URL}/sites/{self.country_code}/search"
            params = {
                'seller_id': seller_id,
                'limit': min(limit, 50),
                'offset': offset
            }
            
            try:
                response = self.session.get(url, params=params, timeout=15)
                
                # Handle 403 errors with more informative message
                if response.status_code == 403:
                    print(f"❌ Acesso negado (403). Tentando método alternativo...")
                    return self._get_items_alternative_method(seller_id)
                
                response.raise_for_status()
                data = response.json()
                
                results = data.get('results', [])
                if not results:
                    break
                
                print(f"📦 Coletados {len(results)} produtos (offset: {offset})")
                
                for item in results:
                    product_info = self._extract_product_info(item)
                    if product_info:
                        all_products.append(product_info)
                
                # Check if there are more pages
                paging = data.get('paging', {})
                total = paging.get('total', 0)
                
                if offset + limit >= total:
                    break
                
                offset += limit
                time.sleep(1)  # Increased delay to avoid rate limiting
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Erro ao buscar produtos: {e}")
                break
        
        print(f"✅ Total de produtos coletados: {len(all_products)}")
        return all_products
    
    def _get_items_alternative_method(self, seller_id: str) -> List[Dict]:
        """
        Alternative method to get items using different API endpoint
        
        Args:
            seller_id: The seller ID
            
        Returns:
            List of product dictionaries
        """
        all_products = []
        
        try:
            # Try using the users endpoint
            url = f"{self.BASE_URL}/users/{seller_id}/items/search"
            params = {'limit': 50, 'offset': 0}
            
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                item_ids = data.get('results', [])
                
                print(f"✓ Encontrados {len(item_ids)} IDs de produtos")
                print(f"⏳ Buscando detalhes dos produtos...")
                
                for item_id in item_ids[:50]:  # Limit to first 50 for testing
                    item_detail = self._get_item_detail(item_id)
                    if item_detail:
                        product_info = self._extract_product_info(item_detail)
                        if product_info:
                            all_products.append(product_info)
                    time.sleep(0.5)
                
                print(f"✅ Coletados {len(all_products)} produtos via método alternativo")
            else:
                print(f"❌ Método alternativo também falhou: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erro no método alternativo: {e}")
        
        return all_products
    
    def _get_item_detail(self, item_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific item
        
        Args:
            item_id: The item ID
            
        Returns:
            Item detail dictionary
        """
        try:
            url = f"{self.BASE_URL}/items/{item_id}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            
            return None
            
        except Exception as e:
            print(f"⚠️ Erro ao buscar detalhes do item {item_id}: {e}")
            return None
    
    def _extract_product_info(self, item: Dict) -> Optional[Dict]:
        """
        Extract relevant information from a product
        
        Args:
            item: Raw product data from API
            
        Returns:
            Dictionary with product information
        """
        try:
            product = {
                'id': item.get('id'),
                'title': item.get('title'),
                'price': item.get('price'),
                'currency_id': item.get('currency_id'),
                'available_quantity': item.get('available_quantity'),
                'sold_quantity': item.get('sold_quantity'),
                'condition': item.get('condition'),
                'permalink': item.get('permalink'),
                'thumbnail': item.get('thumbnail'),
                'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Get detailed description if needed
            description = self._get_product_description(item.get('id'))
            product['description'] = description
            
            return product
            
        except Exception as e:
            print(f"⚠️ Erro ao processar produto: {e}")
            return None
    
    def _get_product_description(self, item_id: str) -> str:
        """
        Get the full description of a product
        
        Args:
            item_id: Product ID
            
        Returns:
            Product description text
        """
        try:
            url = f"{self.BASE_URL}/items/{item_id}/description"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('plain_text', 'N/A')
            else:
                return 'N/A'
                
        except Exception as e:
            print(f"⚠️ Erro ao buscar descrição do produto {item_id}: {e}")
            return 'N/A'
    
    def save_to_json(self, products: List[Dict], filename: str):
        """
        Save products to JSON file
        
        Args:
            products: List of product dictionaries
            filename: Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=2)
            print(f"💾 Dados salvos em: {filename}")
        except Exception as e:
            print(f"❌ Erro ao salvar JSON: {e}")
    
    def save_to_csv(self, products: List[Dict], filename: str):
        """
        Save products to CSV file
        
        Args:
            products: List of product dictionaries
            filename: Output filename
        """
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
    """Main function to run the scraper"""
    print("=" * 60)
    print("🛒 MercadoLivre Product Scraper")
    print("=" * 60)
    print("\n💡 Dica: Use o ID numérico do vendedor para melhores resultados")
    print("   Exemplo: 123456789 (não o nickname)")
    print("   Para encontrar o ID: acesse o perfil e veja na URL")
    
    # Get seller ID from user
    seller_id = input("\n📝 Digite o ID numérico ou nickname do vendedor: ").strip()
    
    if not seller_id:
        print("❌ ID do vendedor não pode estar vazio")
        return
    
    # Initialize scraper
    scraper = MercadoLivreScraper(country_code="MLB")  # MLB = MercadoLivre Brasil
    
    # Collect products
    products = scraper.get_seller_items(seller_id)
    
    if not products:
        print("⚠️ Nenhum produto encontrado para este vendedor")
        return
    
    # Display sample
    print("\n" + "=" * 60)
    print("📊 Amostra dos dados coletados:")
    print("=" * 60)
    
    for i, product in enumerate(products[:3], 1):
        print(f"\n{i}. {product['title']}")
        print(f"   💰 Preço: {product['currency_id']} {product['price']}")
        print(f"   📦 Disponível: {product['available_quantity']}")
        print(f"   ✅ Vendidos: {product['sold_quantity']}")
        print(f"   📝 Descrição: {product['description'][:100]}...")
        print(f"   🔗 Link: {product['permalink']}")
    
    # Ask for export format
    print("\n" + "=" * 60)
    print("💾 Escolha o formato de exportação:")
    print("1. JSON")
    print("2. CSV")
    print("3. Ambos")
    choice = input("Escolha (1-3): ").strip()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = f"mercadolivre_{seller_id}_{timestamp}"
    
    if choice in ['1', '3']:
        scraper.save_to_json(products, f"{base_filename}.json")
    
    if choice in ['2', '3']:
        scraper.save_to_csv(products, f"{base_filename}.csv")
    
    print("\n✅ Processo concluído com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    main()

