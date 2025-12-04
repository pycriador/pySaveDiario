# 🎫 Namespaces Completos de Cupons

## 📋 Visão Geral

Lista completa de todos os namespaces disponíveis para cupons em templates.

---

## 🏷️ Namespaces Disponíveis

### 1. Código do Cupom

| Namespace | Descrição | Exemplo |
|-----------|-----------|---------|
| `{coupon_code}` | Código do cupom | DESC10 |
| `{code}` | Alias para código | DESC10 |

**Uso:**
```
Use o cupom {coupon_code} para ganhar desconto!
```

**Resultado:**
```
Use o cupom DESC10 para ganhar desconto!
```

---

### 2. Vendedor do Cupom

| Namespace | Descrição | Exemplo |
|-----------|-----------|---------|
| `{coupon_seller}` | Nome do vendedor associado | Mercado Livre |
| `{seller}` | Alias para vendedor | Mercado Livre |
| `{seller_name}` | Nome do vendedor | Mercado Livre |

**Uso:**
```
Cupom exclusivo da {coupon_seller}!
```

**Resultado:**
```
Cupom exclusivo da Mercado Livre!
```

---

### 3. Tipo de Desconto

| Namespace | Descrição | Exemplo |
|-----------|-----------|---------|
| `{coupon_discount_type}` | Tipo de desconto (traduzido) | Porcentagem (%) |
| `{tipo_desconto}` | Alias em português | Valor Fixo (R$) |

**Valores possíveis:**
- `Porcentagem (%)` - Para descontos percentuais
- `Valor Fixo (R$)` - Para descontos em valor absoluto

**Uso:**
```
Tipo de desconto: {coupon_discount_type}
```

**Resultado:**
```
Tipo de desconto: Porcentagem (%)
```

---

### 4. Valor do Desconto

| Namespace | Descrição | Exemplo |
|-----------|-----------|---------|
| `{coupon_discount_value}` | Valor do desconto formatado | 10% ou R$ 20,00 |
| `{valor_desconto}` | Alias em português | 10% ou R$ 20,00 |

**Formatação automática:**
- Percentual: `10%`
- Valor fixo: `R$ 20,00`

**Uso:**
```
Desconto de {coupon_discount_value}
```

**Resultado (percentual):**
```
Desconto de 10%
```

**Resultado (valor fixo):**
```
Desconto de R$ 20,00
```

---

### 5. Limite Máximo de Desconto ⭐ **NOVO**

| Namespace | Descrição | Exemplo |
|-----------|-----------|---------|
| `{max_discount_value}` | Valor máximo do desconto | R$ 50,00 |
| `{limite_desconto}` | Alias em português | R$ 50,00 |
| `{coupon_max_discount}` | Desconto máximo | R$ 50,00 |
| `{limite}` | Alias curto | R$ 50,00 |

**Comportamento:**
- Se houver limite: mostra `R$ XX,XX`
- Se não houver limite: mostra `Sem limite`

**Uso:**
```
10% de desconto (até {max_discount_value})
```

**Resultado (com limite):**
```
10% de desconto (até R$ 50,00)
```

**Resultado (sem limite):**
```
10% de desconto (até Sem limite)
```

---

### 6. Validade do Cupom ⭐ **CORRIGIDO**

| Namespace | Descrição | Exemplo |
|-----------|-----------|---------|
| `{coupon_expires}` | Data de expiração | 31/12/2025 |
| `{validade_cupom}` | Validade do cupom | 31/12/2025 |
| `{expira_em}` | Data de expiração | 31/12/2025 |

**Formato:** `DD/MM/YYYY`

**Comportamento:**
- Se houver validade: mostra a data
- Se não houver validade: mostra `Sem validade`

**Uso:**
```
Válido até {coupon_expires}
```

**Resultado (com validade):**
```
Válido até 31/12/2025
```

**Resultado (sem validade):**
```
Válido até Sem validade
```

---

### 7. Lista de Todos os Cupons

| Namespace | Descrição | Exemplo |
|-----------|-----------|---------|
| `{all_coupons}` | Todos os cupons selecionados | CUPONS: DESC10, FRETE, NATAL |
| `{todos_cupons}` | Alias em português | CUPONS: DESC10, FRETE, NATAL |
| `{cupons}` | Alias curto | CUPONS: DESC10, FRETE, NATAL |

**Formato:** `CUPONS: CUPOM1, CUPOM2, CUPOM3`

**Uso:**
```
{all_coupons}
Aproveite!
```

**Resultado:**
```
CUPONS: DESC10, FRETE, NATAL
Aproveite!
```

---

### 8. Preço com Cupom Aplicado

| Namespace | Descrição | Exemplo |
|-----------|-----------|---------|
| `{price_with_coupon}` | Preço com desconto aplicado | 89.99 |
| `{preco_com_cupom}` | Alias em português | 89.99 |

**Cálculo:**
- Considera o **melhor desconto** entre os cupons selecionados
- Respeita o **limite máximo** de desconto
- Nunca resulta em preço negativo

**Uso:**
```
De R$ {price} por R$ {price_with_coupon} com cupom!
```

**Resultado:**
```
De R$ 99,90 por R$ 89,91 com cupom!
```

---

## 📝 Exemplo Completo

### Template:

```
🎁 OFERTA ESPECIAL!

Produto: {product_name}
Preço: R$ {price}

💰 CUPOM DISPONÍVEL:
Código: {coupon_code}
Desconto: {coupon_discount_value}
Limite: {max_discount_value}
Válido até: {coupon_expires}
Loja: {coupon_seller}

🔥 PREÇO COM CUPOM: R$ {price_with_coupon}

Todos os cupons disponíveis:
{all_coupons}

🛒 Link: {offer_url}
```

### Resultado (com cupom de 10% até R$ 50):

```
🎁 OFERTA ESPECIAL!

Produto: Controle PS5 DualSense
Preço: R$ 399,00

💰 CUPOM DISPONÍVEL:
Código: DESC10
Desconto: 10%
Limite: R$ 50,00
Válido até: 31/12/2025
Loja: Amazon

🔥 PREÇO COM CUPOM: R$ 359,10

Todos os cupons disponíveis:
CUPONS: DESC10, FRETEGRATIS

🛒 Link: https://exemplo.com/controle
```

---

## 🔍 Comportamento dos Namespaces

### Quando Múltiplos Cupons São Selecionados:

- **Namespaces individuais** (`{coupon_code}`, `{coupon_expires}`, etc.):
  - Usam dados do **primeiro cupom selecionado**
  
- **`{all_coupons}`**:
  - Lista **todos** os cupons selecionados
  
- **`{price_with_coupon}`**:
  - Calcula o **melhor desconto** entre todos os cupons

### Quando Nenhum Cupom É Selecionado:

- Todos os namespaces de cupom são **removidos** (substituídos por string vazia)
- Exceto `{price_with_coupon}` que mantém o preço original

---

## ⚙️ Configuração

### Adicionar Namespaces ao Banco de Dados:

```bash
python scripts/add_missing_coupon_namespaces.py
```

### Namespaces Adicionados:

1. ✅ `coupon_discount_type` - Tipo de desconto
2. ✅ `tipo_desconto` - Alias em português
3. ✅ `coupon_discount_value` - Valor do desconto
4. ✅ `valor_desconto` - Alias em português
5. ✅ `max_discount_value` - Limite máximo
6. ✅ `limite_desconto` - Alias em português
7. ✅ `coupon_max_discount` - Desconto máximo
8. ✅ `validade_cupom` - Validade do cupom
9. ✅ `expira_em` - Data de expiração

---

## 🐛 Correções Aplicadas

### `{coupon_expires}` não estava sendo substituído:

**Problema:**
- Namespace existia no banco de dados
- Mas não estava sendo coletado nem substituído no JavaScript

**Solução:**
1. ✅ Adicionado `data-coupon-expires` ao checkbox
2. ✅ Coletado no JavaScript (variável `expires`)
3. ✅ Adicionado ao objeto `selectedCoupons`
4. ✅ Substituição implementada com fallback "Sem validade"

---

## 📚 Documentação Relacionada

- [COUPON_DISCOUNT_FEATURE.md](COUPON_DISCOUNT_FEATURE.md) - Sistema de descontos
- [MAX_DISCOUNT_LIMIT.md](MAX_DISCOUNT_LIMIT.md) - Limite máximo de desconto
- [ALL_COUPONS_NAMESPACE.md](ALL_COUPONS_NAMESPACE.md) - Namespace `{all_coupons}`

---

## 🎯 Dicas de Uso

### 1. Cupom Simples:
```
Use o cupom {coupon_code} e ganhe {coupon_discount_value} de desconto!
```

### 2. Cupom com Limite:
```
{coupon_discount_value} OFF (máximo {max_discount_value})
Cupom: {coupon_code}
```

### 3. Cupom com Validade:
```
⏰ Cupom {coupon_code} válido até {coupon_expires}
💰 Desconto: {coupon_discount_value}
```

### 4. Comparação de Preço:
```
De: R$ {price}
Por: R$ {price_with_coupon}
Cupom: {all_coupons}
```

### 5. Informações Completas:
```
🎟️ CUPOM DISPONÍVEL
━━━━━━━━━━━━━━━━━━
Código: {coupon_code}
Desconto: {coupon_discount_value}
Limite: {max_discount_value}
Validade: {coupon_expires}
Loja: {coupon_seller}
Tipo: {coupon_discount_type}
```

---

**Última Atualização:** 04/12/2025  
**Status:** ✅ Completo e Funcional

