"""
Helper script to find the numeric seller ID from a nickname
This helps avoid 403 errors when scraping MercadoLivre
"""

import requests
import sys


def get_seller_id_from_nickname(nickname: str, country_code: str = "MLB") -> dict:
    """
    Get seller numeric ID from nickname
    
    Args:
        nickname: Seller nickname (from profile URL)
        country_code: Country code (MLB for Brazil)
        
    Returns:
        Dictionary with seller information
    """
    base_url = "https://api.mercadolibre.com"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'pt-BR,pt;q=0.9',
    }
    
    print(f"🔍 Buscando ID do vendedor: {nickname}")
    print("-" * 50)
    
    # Method 1: Try direct users endpoint
    try:
        url = f"{base_url}/users/{nickname}"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            seller_info = {
                'id': data.get('id'),
                'nickname': data.get('nickname'),
                'seller_reputation': data.get('seller_reputation', {}).get('level_id'),
                'registration_date': data.get('registration_date'),
                'permalink': data.get('permalink'),
            }
            return seller_info
    except Exception as e:
        print(f"⚠️ Método 1 falhou: {e}")
    
    # Method 2: Search for products and extract seller info
    try:
        url = f"{base_url}/sites/{country_code}/search"
        params = {'nickname': nickname, 'limit': 1}
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            if results:
                seller = results[0].get('seller', {})
                seller_info = {
                    'id': seller.get('id'),
                    'nickname': seller.get('nickname'),
                    'seller_reputation': seller.get('seller_reputation', {}).get('level_id'),
                    'permalink': seller.get('permalink'),
                }
                return seller_info
    except Exception as e:
        print(f"⚠️ Método 2 falhou: {e}")
    
    return None


def main():
    """Main function"""
    print("=" * 60)
    print("🔎 MercadoLivre - Buscar ID Numérico do Vendedor")
    print("=" * 60)
    print("\nEste script ajuda a encontrar o ID numérico do vendedor")
    print("necessário para evitar erros 403 no scraper.\n")
    
    if len(sys.argv) > 1:
        nickname = sys.argv[1]
    else:
        nickname = input("📝 Digite o nickname do vendedor: ").strip()
    
    if not nickname:
        print("❌ Nickname não pode estar vazio")
        return
    
    seller_info = get_seller_id_from_nickname(nickname)
    
    if seller_info and seller_info.get('id'):
        print("\n✅ Vendedor encontrado!")
        print("=" * 60)
        print(f"🆔 ID Numérico: {seller_info['id']}")
        print(f"👤 Nickname: {seller_info.get('nickname', 'N/A')}")
        print(f"⭐ Reputação: {seller_info.get('seller_reputation', 'N/A')}")
        print(f"📅 Cadastro: {seller_info.get('registration_date', 'N/A')}")
        print(f"🔗 Perfil: {seller_info.get('permalink', 'N/A')}")
        print("=" * 60)
        print(f"\n💡 Use este ID no scraper: {seller_info['id']}")
        print(f"\nComando:")
        print(f"python scripts/mercadolivre_scraper.py")
        print(f"Quando solicitado, digite: {seller_info['id']}")
    else:
        print("\n❌ Não foi possível encontrar o vendedor")
        print("\n💡 Dicas:")
        print("1. Verifique se o nickname está correto")
        print("2. Acesse o perfil do vendedor no navegador")
        print("3. Na URL você verá: perfil.mercadolivre.com.br/NICKNAME")
        print("4. Use exatamente o NICKNAME da URL")
        print("\nAlternativamente:")
        print("1. Abra qualquer produto do vendedor")
        print("2. Clique no nome do vendedor")
        print("3. Veja o ID numérico na URL da página de perguntas")


if __name__ == "__main__":
    main()

