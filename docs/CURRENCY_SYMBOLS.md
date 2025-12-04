# 💱 Sistema de Símbolos de Moeda

## 📋 Visão Geral

Sistema completo de símbolos de moeda implementado para exibir símbolos locais (R$, $, €) ao invés de códigos ISO (BRL, USD, EUR) em todas as interfaces do aplicativo.

---

## ✨ Motivação

**No Brasil**, quando indicamos preços, usamos:
- ✅ **R$ 100,00** (correto e natural)
- ❌ **BRL 100,00** (código ISO, formal demais)

**Solução:** Exibir símbolos de moeda nativos em todas as visualizações.

---

## 🌍 Moedas Suportadas

| Código | Símbolo | Nome Completo | Exemplo |
|--------|---------|---------------|---------|
| **BRL** | **R$** | Real Brasileiro | R$ 100,00 |
| USD | $ | Dólar Americano | $ 100.00 |
| EUR | € | Euro | € 100.00 |
| GBP | £ | Libra Esterlina | £ 100.00 |
| JPY | ¥ | Iene Japonês | ¥ 100 |
| CAD | CA$ | Dólar Canadense | CA$ 100.00 |
| AUD | AU$ | Dólar Australiano | AU$ 100.00 |
| CHF | CHF | Franco Suíço | CHF 100.00 |
| CNY | ¥ | Yuan Chinês | ¥ 100.00 |
| ARS | ARS$ | Peso Argentino | ARS$ 100.00 |
| MXN | MX$ | Peso Mexicano | MX$ 100.00 |
| CLP | CLP$ | Peso Chileno | CLP$ 100 |

---

## 🏗️ Arquitetura

### 1. Utilitário de Moeda

**Arquivo:** `app/utils/currency.py`

```python
# Currency symbols mapping
CURRENCY_SYMBOLS = {
    'BRL': 'R$',
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'JPY': '¥',
    # ... more currencies
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
```

**Funções disponíveis:**
- `get_currency_symbol(code)` - Retorna símbolo
- `get_currency_name(code)` - Retorna nome completo
- `format_price(value, code)` - Formata preço completo

---

### 2. Filtro Jinja2 Customizado

**Arquivo:** `app/__init__.py`

```python
def register_template_filters(app: Flask) -> None:
    """Register custom Jinja2 template filters."""
    from .utils.currency import get_currency_symbol
    
    @app.template_filter('currency_symbol')
    def currency_symbol_filter(currency_code):
        """Convert currency code to symbol (e.g., BRL -> R$)"""
        return get_currency_symbol(currency_code)
```

**Uso nos templates:**
```jinja2
{{ offer.currency|currency_symbol }}
```

**Resultado:**
```
BRL → R$
USD → $
EUR → €
```

---

## 📝 Uso nos Templates

### Antes

```html
<!-- ❌ Exibe código ISO -->
<span>{{ offer.currency }} {{ offer.price }}</span>
<!-- Resultado: BRL 100.00 -->
```

### Depois

```html
<!-- ✅ Exibe símbolo -->
<span>{{ offer.currency|currency_symbol }} {{ offer.price }}</span>
<!-- Resultado: R$ 100.00 -->
```

---

## 🎯 Onde Foi Implementado

### Templates HTML Atualizados

1. **`offers_list.html`** - Listagem de ofertas
   ```html
   {{ offer.currency|currency_symbol }} {{ '%.2f'|format(offer.price_value) }}
   {{ offer.currency|currency_symbol }} {{ '%.2f'|format(offer.old_price) }}
   ```

2. **`offer_share.html`** - Página de compartilhamento
   ```html
   {{ offer.currency|currency_symbol }} {{ "%.2f"|format(offer.price) }}
   {{ offer.currency|currency_symbol }} {{ "%.2f"|format(offer.old_price) }}
   ```

3. **`dashboard.html`** - Dashboard principal
   ```html
   {{ offer.currency|currency_symbol }} {{ '%.2f'|format(offer.price_value) }}
   ```

4. **`index.html`** - Página inicial
   ```html
   {{ offer.currency|currency_symbol }} {{ '%.2f'|format(offer.price_value) }}
   ```

---

### JavaScript Atualizado

**`offer_share.html` - Geração de texto para redes sociais**

```javascript
const offerData = {
  // ... outros campos ...
  currency: 'BRL',           // Código ISO (armazenado no banco)
  currency_symbol: 'R$',     // Símbolo (para exibição)
  // ... outros campos ...
};

// Uso no texto de parcelamento
const installmentFull = `${offerData.installment_count}x de ${offerData.currency_symbol} ${offerData.installment_value} ${interestText}`;
// Resultado: "5x de R$ 72.00 sem juros"
```

**Antes:**
```
5x de BRL 72.00 sem juros
```

**Depois:**
```
5x de R$ 72.00 sem juros
```

---

### Formulários Atualizados

**`app/forms.py` - SelectField de moedas**

**Antes:**
```python
choices=[
    ('BRL', 'BRL - Real Brasileiro'),
    ('USD', 'USD - Dólar Americano'),
    ('EUR', 'EUR - Euro'),
]
```

**Depois:**
```python
choices=[
    ('BRL', 'R$ - Real Brasileiro'),
    ('USD', '$ - Dólar Americano'),
    ('EUR', '€ - Euro'),
]
```

**Visualização no formulário:**

```
┌────────────────────────────────┐
│ Moeda: [R$ - Real Brasileiro ▼]│
└────────────────────────────────┘
```

---

## 💻 Exemplos de Uso

### Template (HTML)

```jinja2
<!-- Preço simples -->
<p>Preço: {{ offer.currency|currency_symbol }} {{ offer.price }}</p>

<!-- Preço antigo com desconto -->
{% if offer.old_price %}
<s>{{ offer.currency|currency_symbol }} {{ offer.old_price }}</s>
<strong>{{ offer.currency|currency_symbol }} {{ offer.price }}</strong>
{% endif %}

<!-- Parcelamento -->
<p>Em até {{ offer.installment_count }}x de 
   {{ offer.currency|currency_symbol }} {{ offer.installment_value }}
</p>
```

---

### Python (Backend)

```python
from app.utils.currency import get_currency_symbol, format_price

# Obter símbolo
symbol = get_currency_symbol('BRL')  # Retorna: 'R$'

# Formatar preço completo
price_text = format_price(100.00, 'BRL')  # Retorna: 'R$ 100.00'
```

---

### JavaScript (Frontend)

```javascript
// Dados da oferta
const offerData = {
  currency: 'BRL',
  currency_symbol: 'R$',
  price: 100.00
};

// Criar texto formatado
const priceText = `${offerData.currency_symbol} ${offerData.price.toFixed(2)}`;
// Resultado: "R$ 100.00"
```

---

## 🔧 Como Adicionar Novas Moedas

### Passo 1: Adicionar ao Dicionário

**Arquivo:** `app/utils/currency.py`

```python
CURRENCY_SYMBOLS = {
    'BRL': 'R$',
    'USD': '$',
    # ... moedas existentes ...
    'NEW': 'NEW$',  # ← Nova moeda
}

CURRENCY_NAMES = {
    'BRL': 'Real Brasileiro',
    'USD': 'Dólar Americano',
    # ... nomes existentes ...
    'NEW': 'Nova Moeda',  # ← Nome completo
}
```

---

### Passo 2: Adicionar ao Formulário

**Arquivo:** `app/forms.py`

```python
currency = SelectField("Moeda", validators=[DataRequired()], 
                      choices=[
                          ('BRL', 'R$ - Real Brasileiro'),
                          ('USD', '$ - Dólar Americano'),
                          # ... moedas existentes ...
                          ('NEW', 'NEW$ - Nova Moeda'),  # ← Nova opção
                      ],
                      default='BRL')
```

---

### Passo 3: Pronto!

O filtro Jinja2 e o JavaScript automaticamente reconhecerão a nova moeda!

---

## 📊 Antes vs Depois

### Interface de Listagem

#### ❌ Antes
```
┌────────────────────────────┐
│ iPhone 15                  │
│ BRL 4999.00               │  ← Código ISO
│ [Ver detalhes]             │
└────────────────────────────┘
```

#### ✅ Depois
```
┌────────────────────────────┐
│ iPhone 15                  │
│ R$ 4999.00                │  ← Símbolo brasileiro
│ [Ver detalhes]             │
└────────────────────────────┘
```

---

### Formulário de Seleção

#### ❌ Antes
```
Moeda: [BRL - Real Brasileiro ▼]
       [USD - Dólar Americano  ]
       [EUR - Euro             ]
```

#### ✅ Depois
```
Moeda: [R$ - Real Brasileiro ▼]
       [$ - Dólar Americano   ]
       [€ - Euro              ]
```

---

### Texto de Compartilhamento

#### ❌ Antes
```
🔥 PROMOÇÃO!

iPhone 15 por apenas BRL 4999.00
Parcele em 5x de BRL 999.80 sem juros

Compre agora!
```

#### ✅ Depois
```
🔥 PROMOÇÃO!

iPhone 15 por apenas R$ 4999.00
Parcele em 5x de R$ 999.80 sem juros

Compre agora!
```

---

## 🎨 Visualização em Todas as Telas

### 1. Dashboard

```
┌─────────────────────────────────┐
│ 📊 Ofertas Ativas               │
├─────────────────────────────────┤
│ • iPhone 15                     │
│   R$ 4999.00                    │  ✅
│                                 │
│ • Galaxy S24                    │
│   R$ 3599.00                    │  ✅
└─────────────────────────────────┘
```

---

### 2. Listagem de Ofertas

```
┌────────────────────┬────────────────────┐
│ 📱 iPhone 15       │ 📱 Galaxy S24      │
│ R$ 4999.00         │ R$ 3599.00         │  ✅
│ [Ver] [Editar]     │ [Ver] [Editar]     │
└────────────────────┴────────────────────┘
```

---

### 3. Página de Compartilhamento

```
┌─────────────────────────────────┐
│ 🔗 Compartilhar Oferta          │
├─────────────────────────────────┤
│ Produto: iPhone 15              │
│ Preço: R$ 4999.00               │  ✅
│ Preço Antigo: R$ 5499.00        │  ✅
│ Desconto: -9%                   │
│                                 │
│ Parcele em:                     │
│ 5x de R$ 999.80 sem juros       │  ✅
│                                 │
│ [📱 WhatsApp] [📷 Instagram]   │
└─────────────────────────────────┘
```

---

### 4. Formulário de Criação

```
┌─────────────────────────────────┐
│ 📝 Nova Oferta                  │
├─────────────────────────────────┤
│ Nome: [________________]        │
│ Preço: [________]               │
│ Moeda: [R$ - Real Brasileiro ▼] │  ✅
│                                 │
│ [Salvar] [Cancelar]             │
└─────────────────────────────────┘
```

---

## 🧪 Como Testar

### 1. Testar Listagem

```bash
# Acesse
http://localhost:5000/ofertas

# Verifique
✅ Preços exibem "R$ 100.00" (não "BRL 100.00")
✅ Preços antigos exibem "R$ 150.00"
✅ Desconto calculado corretamente
```

---

### 2. Testar Compartilhamento

```bash
# Acesse
http://localhost:5000/ofertas/1/compartilhar

# Verifique
✅ Preço exibe "R$ 100.00"
✅ Preço antigo exibe "R$ 150.00"
✅ Parcelamento exibe "5x de R$ 20.00 sem juros"
✅ Texto gerado usa "R$" (não "BRL")
```

---

### 3. Testar Formulário

```bash
# Acesse
http://localhost:5000/ofertas/nova

# Verifique
✅ Dropdown de moeda exibe "R$ - Real Brasileiro"
✅ Outras moedas exibem símbolos ($ - Dólar, € - Euro)
✅ Seleção funciona normalmente
```

---

### 4. Testar Dashboard

```bash
# Acesse
http://localhost:5000/dashboard

# Verifique
✅ Ofertas recentes exibem "R$ 100.00"
✅ Gráficos usam "R$" nos rótulos (se houver)
```

---

## 🔍 Troubleshooting

### Problema: Símbolo não aparece

**Causa:** Filtro não registrado

**Solução:**
```python
# Verifique em app/__init__.py
def create_app():
    # ...
    register_template_filters(app)  # ← Deve estar aqui
    # ...
```

---

### Problema: Moeda desconhecida retorna código

**Comportamento esperado:** Se a moeda não existe no dicionário, retorna o código original

```python
get_currency_symbol('XYZ')  # Retorna: 'XYZ'
```

**Solução:** Adicionar moeda ao dicionário

---

### Problema: JavaScript não usa símbolo

**Causa:** `currency_symbol` não está no `offerData`

**Solução:**
```javascript
const offerData = {
  currency: {{ offer.currency|tojson }},
  currency_symbol: {{ (offer.currency|currency_symbol)|tojson }},  // ← Adicionar
  // ...
};
```

---

## 📁 Estrutura de Arquivos

```
app/
├── __init__.py                    ✅ Registra filtro Jinja2
├── forms.py                       ✅ Atualiza choices do SelectField
├── utils/
│   ├── __init__.py               ✅ Exporta funções
│   └── currency.py               ✅ Dicionário e utilitários
└── templates/
    ├── offers_list.html          ✅ Usa |currency_symbol
    ├── offer_share.html          ✅ Usa |currency_symbol + JS
    ├── dashboard.html            ✅ Usa |currency_symbol
    └── index.html                ✅ Usa |currency_symbol

docs/
└── CURRENCY_SYMBOLS.md           ✅ Esta documentação
```

---

## ✅ Checklist de Implementação

### Backend
- [x] Criar `app/utils/currency.py`
- [x] Definir `CURRENCY_SYMBOLS` dict
- [x] Definir `CURRENCY_NAMES` dict
- [x] Criar `get_currency_symbol()` function
- [x] Criar `get_currency_name()` function
- [x] Criar `format_price()` function
- [x] Exportar em `app/utils/__init__.py`
- [x] Registrar filtro Jinja2 em `app/__init__.py`
- [x] Atualizar choices em `app/forms.py`

### Templates
- [x] Atualizar `offers_list.html`
- [x] Atualizar `offer_share.html`
- [x] Atualizar `dashboard.html`
- [x] Atualizar `index.html`
- [x] Atualizar JavaScript em `offer_share.html`

### Moedas Suportadas
- [x] BRL (R$)
- [x] USD ($)
- [x] EUR (€)
- [x] GBP (£)
- [x] JPY (¥)
- [x] CAD (CA$)
- [x] AUD (AU$)
- [x] CHF (CHF)
- [x] CNY (¥)
- [x] ARS (ARS$)
- [x] MXN (MX$)
- [x] CLP (CLP$)

### Documentação
- [x] Criar `CURRENCY_SYMBOLS.md`
- [x] Exemplos de uso
- [x] Guia de troubleshooting
- [x] Como adicionar novas moedas

---

## 🎯 Benefícios

### Para Usuários Brasileiros
- ✅ Interface natural com "R$"
- ✅ Não confunde com códigos ISO
- ✅ Fácil leitura de preços
- ✅ Experiência localizada

### Para Usuários Internacionais
- ✅ Símbolos reconhecidos ($, €, £)
- ✅ Suporte a 12 moedas
- ✅ Fácil adição de novas moedas
- ✅ Consistência em toda interface

### Para Desenvolvedores
- ✅ Código centralizado
- ✅ Fácil manutenção
- ✅ Reutilizável
- ✅ Extensível
- ✅ Bem documentado

---

## 🚀 Próximos Passos (Opcional)

### Melhorias Futuras

1. **Formatação Completa de Número**
   ```python
   # BR: R$ 1.234,56
   # US: $ 1,234.56
   # EU: € 1.234,56
   ```

2. **Conversão de Moeda**
   ```python
   convert_currency(100, 'BRL', 'USD')  # R$ 100 → $ 20
   ```

3. **Cache de Taxas**
   ```python
   # Atualizar taxas diariamente via API
   ```

4. **Símbolos Customizados por Usuário**
   ```python
   # Permitir usuário definir preferência
   user.currency_preference = 'BRL'
   user.currency_symbol = 'R$'
   ```

---

## 📚 Referências

### Códigos ISO 4217
- **BRL** - Brazilian Real
- **USD** - United States Dollar
- **EUR** - Euro
- Lista completa: https://en.wikipedia.org/wiki/ISO_4217

### Símbolos Unicode
- **R$** - U+0052 U+0024
- **$** - U+0024
- **€** - U+20AC
- **£** - U+00A3
- **¥** - U+00A5

---

## 🎉 Conclusão

Sistema completo de símbolos de moeda implementado com sucesso!

- ✅ **12 moedas suportadas** (BRL, USD, EUR, GBP, etc.)
- ✅ **Filtro Jinja2** (`|currency_symbol`)
- ✅ **5 templates atualizados** (listagem, share, dashboard, index, forms)
- ✅ **JavaScript atualizado** (geração de texto)
- ✅ **Formulários atualizados** (SelectField com símbolos)
- ✅ **Utilitários Python** (funções helper)
- ✅ **Totalmente documentado**
- ✅ **Fácil extensão** (adicionar novas moedas)

**Status:** 🟢 **COMPLETO E PRONTO PARA USO**

---

**Última atualização:** 04/12/2025

