"""
Example usage of MercadoLivre Scraper
Demonstrates how to use the scraper programmatically
"""

from mercadolivre_scraper import MercadoLivreScraper
from datetime import datetime


def example_basic_usage():
    """Basic example: collect all products from a seller"""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # Initialize scraper for Brazil (MLB)
    scraper = MercadoLivreScraper(country_code="MLB")
    
    # Replace with actual seller ID
    seller_id = "EXEMPLO_VENDEDOR"
    
    # Collect products
    products = scraper.get_seller_items(seller_id)
    
    # Save to JSON
    scraper.save_to_json(products, f"products_{seller_id}.json")
    
    # Save to CSV
    scraper.save_to_csv(products, f"products_{seller_id}.csv")
    
    print(f"\n✅ Collected {len(products)} products")


def example_price_analysis():
    """Example: analyze prices from a seller"""
    print("\n" + "=" * 60)
    print("Example 2: Price Analysis")
    print("=" * 60)
    
    scraper = MercadoLivreScraper(country_code="MLB")
    seller_id = "EXEMPLO_VENDEDOR"
    
    products = scraper.get_seller_items(seller_id)
    
    if not products:
        print("No products found")
        return
    
    # Calculate statistics
    prices = [p['price'] for p in products]
    avg_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)
    
    print(f"\n📊 Price Statistics:")
    print(f"   Average: R$ {avg_price:.2f}")
    print(f"   Minimum: R$ {min_price:.2f}")
    print(f"   Maximum: R$ {max_price:.2f}")
    
    # Top 5 most expensive
    top_expensive = sorted(products, key=lambda x: x['price'], reverse=True)[:5]
    print(f"\n💎 Top 5 Most Expensive:")
    for i, product in enumerate(top_expensive, 1):
        print(f"   {i}. {product['title'][:50]}... - R$ {product['price']:.2f}")
    
    # Top 5 cheapest
    top_cheap = sorted(products, key=lambda x: x['price'])[:5]
    print(f"\n💰 Top 5 Cheapest:")
    for i, product in enumerate(top_cheap, 1):
        print(f"   {i}. {product['title'][:50]}... - R$ {product['price']:.2f}")


def example_sales_analysis():
    """Example: analyze sales performance"""
    print("\n" + "=" * 60)
    print("Example 3: Sales Analysis")
    print("=" * 60)
    
    scraper = MercadoLivreScraper(country_code="MLB")
    seller_id = "EXEMPLO_VENDEDOR"
    
    products = scraper.get_seller_items(seller_id)
    
    if not products:
        print("No products found")
        return
    
    # Top selling products
    top_sellers = sorted(products, key=lambda x: x['sold_quantity'], reverse=True)[:10]
    
    print(f"\n🏆 Top 10 Best Sellers:")
    for i, product in enumerate(top_sellers, 1):
        print(f"   {i}. {product['title'][:50]}...")
        print(f"      💰 Price: R$ {product['price']:.2f}")
        print(f"      📦 Sold: {product['sold_quantity']} units")
        print(f"      📊 Revenue: R$ {product['price'] * product['sold_quantity']:.2f}")
        print()
    
    # Total revenue estimation
    total_revenue = sum(p['price'] * p['sold_quantity'] for p in products)
    total_sold = sum(p['sold_quantity'] for p in products)
    
    print(f"📈 Overall Statistics:")
    print(f"   Total products: {len(products)}")
    print(f"   Total units sold: {total_sold}")
    print(f"   Estimated total revenue: R$ {total_revenue:.2f}")


def example_inventory_analysis():
    """Example: analyze inventory status"""
    print("\n" + "=" * 60)
    print("Example 4: Inventory Analysis")
    print("=" * 60)
    
    scraper = MercadoLivreScraper(country_code="MLB")
    seller_id = "EXEMPLO_VENDEDOR"
    
    products = scraper.get_seller_items(seller_id)
    
    if not products:
        print("No products found")
        return
    
    # Products with low stock
    low_stock = [p for p in products if p['available_quantity'] < 5]
    out_of_stock = [p for p in products if p['available_quantity'] == 0]
    
    print(f"\n⚠️  Low Stock Alert (< 5 units):")
    for product in low_stock[:10]:
        print(f"   📦 {product['title'][:50]}...")
        print(f"      Available: {product['available_quantity']} units")
        print(f"      Price: R$ {product['price']:.2f}")
        print()
    
    print(f"\n❌ Out of Stock ({len(out_of_stock)} products):")
    for product in out_of_stock[:5]:
        print(f"   - {product['title'][:50]}...")
    
    # Products by condition
    new_products = [p for p in products if p['condition'] == 'new']
    used_products = [p for p in products if p['condition'] == 'used']
    
    print(f"\n📊 Inventory Summary:")
    print(f"   Total products: {len(products)}")
    print(f"   New: {len(new_products)}")
    print(f"   Used: {len(used_products)}")
    print(f"   Low stock: {len(low_stock)}")
    print(f"   Out of stock: {len(out_of_stock)}")


def example_multi_seller_comparison():
    """Example: compare multiple sellers"""
    print("\n" + "=" * 60)
    print("Example 5: Multi-Seller Comparison")
    print("=" * 60)
    
    scraper = MercadoLivreScraper(country_code="MLB")
    
    # Replace with actual seller IDs
    sellers = ["VENDEDOR1", "VENDEDOR2", "VENDEDOR3"]
    
    comparison_data = []
    
    for seller_id in sellers:
        print(f"\n🔍 Analyzing seller: {seller_id}")
        products = scraper.get_seller_items(seller_id)
        
        if not products:
            continue
        
        avg_price = sum(p['price'] for p in products) / len(products)
        total_sold = sum(p['sold_quantity'] for p in products)
        
        comparison_data.append({
            'seller': seller_id,
            'total_products': len(products),
            'avg_price': avg_price,
            'total_sold': total_sold,
            'products': products
        })
    
    print("\n" + "=" * 60)
    print("📊 Comparison Results:")
    print("=" * 60)
    
    for data in comparison_data:
        print(f"\n🏪 {data['seller']}:")
        print(f"   Products: {data['total_products']}")
        print(f"   Avg Price: R$ {data['avg_price']:.2f}")
        print(f"   Total Sold: {data['total_sold']} units")


if __name__ == "__main__":
    print("🛒 MercadoLivre Scraper - Usage Examples")
    print("=" * 60)
    print("\n⚠️  Note: Replace 'EXEMPLO_VENDEDOR' with actual seller IDs")
    print("=" * 60)
    
    # Uncomment the examples you want to run:
    
    # example_basic_usage()
    # example_price_analysis()
    # example_sales_analysis()
    # example_inventory_analysis()
    # example_multi_seller_comparison()
    
    print("\n✅ Examples completed!")
    print("\n💡 Tip: Uncomment the examples in the code to run them")

