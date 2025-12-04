"""
Currency utilities and symbols

Provides currency symbols and formatting utilities for the application.
"""

# Currency symbols mapping
CURRENCY_SYMBOLS = {
    'BRL': 'R$',      # Real Brasileiro
    'USD': '$',       # Dólar Americano
    'EUR': '€',       # Euro
    'GBP': '£',       # Libra Esterlina
    'JPY': '¥',       # Iene Japonês
    'CAD': 'CA$',     # Dólar Canadense
    'AUD': 'AU$',     # Dólar Australiano
    'CHF': 'CHF',     # Franco Suíço
    'CNY': '¥',       # Yuan Chinês
    'ARS': 'ARS$',    # Peso Argentino
    'MXN': 'MX$',     # Peso Mexicano
    'CLP': 'CLP$',    # Peso Chileno
}

# Currency names (full)
CURRENCY_NAMES = {
    'BRL': 'Real Brasileiro',
    'USD': 'Dólar Americano',
    'EUR': 'Euro',
    'GBP': 'Libra Esterlina',
    'JPY': 'Iene Japonês',
    'CAD': 'Dólar Canadense',
    'AUD': 'Dólar Australiano',
    'CHF': 'Franco Suíço',
    'CNY': 'Yuan Chinês',
    'ARS': 'Peso Argentino',
    'MXN': 'Peso Mexicano',
    'CLP': 'Peso Chileno',
}


def get_currency_symbol(currency_code: str) -> str:
    """
    Get currency symbol from code
    
    Args:
        currency_code: Currency code (e.g., 'BRL', 'USD')
        
    Returns:
        Currency symbol (e.g., 'R$', '$')
    """
    return CURRENCY_SYMBOLS.get(currency_code.upper(), currency_code)


def get_currency_name(currency_code: str) -> str:
    """
    Get full currency name from code
    
    Args:
        currency_code: Currency code (e.g., 'BRL')
        
    Returns:
        Full currency name (e.g., 'Real Brasileiro')
    """
    return CURRENCY_NAMES.get(currency_code.upper(), currency_code)


def format_price(value: float, currency_code: str) -> str:
    """
    Format price with currency symbol
    
    Args:
        value: Price value
        currency_code: Currency code
        
    Returns:
        Formatted price (e.g., 'R$ 100.00')
    """
    symbol = get_currency_symbol(currency_code)
    return f"{symbol} {value:.2f}"


def get_currency_choices():
    """
    Get list of currency choices for SelectField
    
    Returns:
        List of tuples (code, display_text)
    """
    return [
        (code, f"{symbol} - {name}")
        for code, (symbol, name) in 
        [(code, (CURRENCY_SYMBOLS[code], CURRENCY_NAMES[code])) for code in CURRENCY_SYMBOLS.keys()]
    ]

