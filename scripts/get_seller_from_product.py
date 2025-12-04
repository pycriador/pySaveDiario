"""
Find seller ID from a product URL - Most reliable method
This is the best way to avoid 403 errors
"""

import requests
import re
import sys


def extract_item_id_from_url(url: str) -> str:
    """
    Extract item ID from MercadoLivre URL
    
    Args:
        url: Product URL
        
    Returns:
        Item ID (e.g., MLB123456789)
    """
    # Pattern: MLB followed by numbers
    pattern = r'(MLB\d+)'
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    
    return None


def get_seller_from_product(product_url_or_id: str) -> dict:
    """
    Get seller information from a product URL or ID
    
    Args:
        product_url_or_id: Full product URL or just the MLB ID
        
    Returns:
        Dictionary with seller information
    """
    # Extract item ID if full URL was provided
    if 'http' in product_url_or_id:
        item_id = extract_item_id_from_url(product_url_or_id)
    else:
        item_id = product_url_or_id
    
    if not item_id:
        print("❌ Não foi possível extrair o ID do produto da URL")
        return None
    
    print(f"🔍 Buscando informações do produto: {item_id}")
    
    base_url = "https://api.mercadolibre.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
    }
    
    try:
        # Get product details
        url = f"{base_url}/items/{item_id}"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            seller_id = data.get('seller_id')
            
            if seller_id:
                # Get seller details
                seller_url = f"{base_url}/users/{seller_id}"
                seller_response = requests.get(seller_url, headers=headers, timeout=10)
                
                if seller_response.status_code == 200:
                    seller_data = seller_response.json()
                    
                    seller_info = {
                        'id': seller_data.get('id'),
                        'nickname': seller_data.get('nickname'),
                        'seller_reputation': seller_data.get('seller_reputation', {}).get('level_id'),
                        'registration_date': seller_data.get('registration_date'),
                        'permalink': seller_data.get('permalink'),
                        'total_items': seller_data.get('seller_reputation', {}).get('metrics', {}).get('sales', {}).get('completed'),
                    }
                    
                    return seller_info
            
        elif response.status_code == 404:
            print(f"❌ Produto não encontrado: {item_id}")
        else:
            print(f"❌ Erro ao buscar produto: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    return None


def main():
    """Main function"""
    print("=" * 70)
    print("🔎 MercadoLivre - Encontrar Vendedor pelo Produto")
    print("=" * 70)
    print("\nMétodo mais confiável para encontrar o ID do vendedor!\n")
    
    if len(sys.argv) > 1:
        product_input = sys.argv[1]
    else:
        print("📝 Cole a URL completa de QUALQUER produto do vendedor:")
        print("   Exemplo: https://produto.mercadolivre.com.br/MLB-123456789-produto")
        print("\n   OU apenas o código do produto:")
        print("   Exemplo: MLB123456789")
        product_input = input("\n➡️  ").strip()
    
    if not product_input:
        print("❌ URL/ID não pode estar vazio")
        return
    
    seller_info = get_seller_from_product(product_input)
    
    if seller_info and seller_info.get('id'):
        print("\n" + "=" * 70)
        print("✅ VENDEDOR ENCONTRADO COM SUCESSO!")
        print("=" * 70)
        print(f"\n🆔 ID NUMÉRICO: {seller_info['id']}")
        print(f"👤 Nickname: {seller_info.get('nickname', 'N/A')}")
        print(f"⭐ Reputação: {seller_info.get('seller_reputation', 'N/A')}")
        print(f"📦 Total de vendas: {seller_info.get('total_items', 'N/A')}")
        print(f"📅 Cadastro: {seller_info.get('registration_date', 'N/A')}")
        print(f"🔗 Perfil: {seller_info.get('permalink', 'N/A')}")
        print("\n" + "=" * 70)
        print(f"\n💡 COPIE ESTE ID PARA USAR NO SCRAPER:")
        print(f"\n   ➡️  {seller_info['id']}")
        print("\n" + "=" * 70)
        print("\n📋 Próximos passos:")
        print(f"   1. Execute: python3 scripts/mercadolivre_scraper.py")
        print(f"   2. Quando solicitado, digite: {seller_info['id']}")
        print(f"   3. Aguarde a coleta dos produtos")
        print("\n✅ Pronto!")
    else:
        print("\n❌ Não foi possível encontrar o vendedor")
        print("\n💡 Dicas:")
        print("1. Verifique se a URL está correta")
        print("2. Certifique-se de que o produto existe")
        print("3. Tente com outro produto do mesmo vendedor")


if __name__ == "__main__":
    main()

