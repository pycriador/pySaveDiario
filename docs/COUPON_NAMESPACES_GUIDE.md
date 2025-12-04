# 🎫 Guia Completo de Namespaces de Cupons

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Código do Cupom](#código-do-cupom)
- [Vendedor](#vendedor)
- [Desconto Percentual](#desconto-percentual)
- [Desconto Fixo](#desconto-fixo)
- [Valor Mínimo](#valor-mínimo)
- [Valor Máximo](#valor-máximo)
- [Validade](#validade)
- [Lista de Cupons](#lista-de-cupons)
- [Preço com Cupom](#preço-com-cupom)
- [Exemplos Práticos](#exemplos-práticos)

---

## 🎯 Visão Geral

Os namespaces de cupons permitem inserir dinamicamente informações dos cupons em templates de compartilhamento. Esta documentação apresenta **nomes mais intuitivos em português** para facilitar o uso.

---

## 🏷️ Código do Cupom

**Descrição:** O código que o cliente deve usar para aplicar o desconto.

| Namespace | Exemplo |
|-----------|---------|
| `{coupon_code}` | DESC10 |
| `{code}` | DESC10 |

**Exemplo de Uso:**
```
Use o cupom {coupon_code} para ganhar desconto!
```

**Resultado:**
```
Use o cupom DESC10 para ganhar desconto!
```

---

## 🏪 Vendedor

**Descrição:** Nome do vendedor associado ao cupom.

| Namespace | Exemplo |
|-----------|---------|
| `{coupon_seller}` | Amazon |
| `{seller}` | Mercado Livre |
| `{seller_name}` | Shopee |

**Exemplo de Uso:**
```
Cupom válido apenas na {coupon_seller}!
```

**Resultado:**
```
Cupom válido apenas na Amazon!
```

---

## 📊 Desconto Percentual

**Descrição:** Valor do desconto quando o cupom é do tipo porcentagem.

| Namespace | Exemplo |
|-----------|---------|
| `{porcentagem}` | 10% |
| `{desconto_porcentagem}` | 10% |
| `{percentual}` | 10% |

**⚠️ Importante:** Estes namespaces **só aparecem** quando o cupom é do tipo **Porcentagem (%)**. Para cupons de valor fixo, eles retornam vazio.

**Exemplo de Uso:**
```
Ganhe {porcentagem} de desconto em sua compra!
```

**Resultado (cupom de 10%):**
```
Ganhe 10% de desconto em sua compra!
```

**Resultado (cupom de R$ 20 fixo):**
```
Ganhe  de desconto em sua compra!
[vazio, use desconto_fixo ao invés]
```

---

## 💰 Desconto Fixo

**Descrição:** Valor do desconto quando o cupom é do tipo fixo em reais.

| Namespace | Exemplo |
|-----------|---------|
| `{desconto_fixo}` | R$ 20,00 |
| `{valor_fixo}` | R$ 20,00 |

**⚠️ Importante:** Estes namespaces **só aparecem** quando o cupom é do tipo **Valor Fixo (R$)**. Para cupons de porcentagem, eles retornam vazio.

**Exemplo de Uso:**
```
Ganhe {desconto_fixo} de desconto direto!
```

**Resultado (cupom de R$ 20):**
```
Ganhe R$ 20,00 de desconto direto!
```

**Resultado (cupom de 10%):**
```
Ganhe  de desconto direto!
[vazio, use porcentagem ao invés]
```

---

## 🛒 Valor Mínimo

**Descrição:** Valor mínimo que o cliente precisa comprar para aplicar o cupom.

| Namespace | Exemplo |
|-----------|---------|
| `{valor_minimo_compra}` | R$ 100,00 |
| `{minimo}` | R$ 100,00 |
| `{compra_minima}` | R$ 100,00 |
| `{valor_minimo}` | R$ 100,00 |
| `{min_purchase_value}` | R$ 100,00 |

**Comportamento:**
- **Com valor mínimo:** Exibe o valor formatado
- **Sem valor mínimo:** Exibe "Sem mínimo"

**Exemplo de Uso:**
```
⚠️ Válido para compras acima de {valor_minimo_compra}
```

**Resultado (com mínimo de R$ 100):**
```
⚠️ Válido para compras acima de R$ 100,00
```

**Resultado (sem mínimo):**
```
⚠️ Válido para compras acima de Sem mínimo
```

**💡 Recomendação:** Use namespace alternativo quando não há mínimo:
```
{% if minimo %}
Compra mínima: {minimo}
{% endif %}
```

---

## 🎁 Valor Máximo

**Descrição:** Limite máximo de desconto que o cupom pode aplicar (especialmente importante para cupons de porcentagem).

| Namespace | Exemplo |
|-----------|---------|
| `{valor_maximo_desconto}` | R$ 50,00 |
| `{maximo}` | R$ 50,00 |
| `{limite}` | R$ 50,00 |
| `{limite_desconto}` | R$ 50,00 |
| `{max_discount_value}` | R$ 50,00 |
| `{coupon_max_discount}` | R$ 50,00 |

**Comportamento:**
- **Com limite:** Exibe o valor formatado
- **Sem limite:** Exibe "Sem limite"

**Exemplo de Uso:**
```
10% de desconto (máximo de {valor_maximo_desconto})
```

**Resultado (com limite de R$ 50):**
```
10% de desconto (máximo de R$ 50,00)
```

**Resultado (sem limite):**
```
10% de desconto (máximo de Sem limite)
```

---

## 📅 Validade

**Descrição:** Data de validade/expiração do cupom.

| Namespace | Formato | Exemplo |
|-----------|---------|---------|
| `{coupon_expires}` | DD/MM/YYYY | 31/12/2025 |
| `{validade_cupom}` | DD/MM/YYYY | 31/12/2025 |
| `{expira_em}` | DD/MM/YYYY | 31/12/2025 |

**Comportamento:**
- **Com validade:** Exibe a data formatada
- **Sem validade:** Exibe "Sem validade"

**Exemplo de Uso:**
```
⏰ Válido até {coupon_expires}
```

**Resultado (com validade):**
```
⏰ Válido até 31/12/2025
```

**Resultado (sem validade):**
```
⏰ Válido até Sem validade
```

---

## 📋 Lista de Cupons

**Descrição:** Mostra todos os cupons selecionados de uma vez.

| Namespace | Formato |
|-----------|---------|
| `{all_coupons}` | CUPONS: COD1, COD2, COD3 |
| `{todos_cupons}` | CUPONS: COD1, COD2, COD3 |
| `{cupons}` | CUPONS: COD1, COD2, COD3 |

**Formato de Saída:**
```
CUPONS: DESC10, FRETEGRATIS, NATAL20
```

**Exemplo de Uso:**
```
🎟️ Use nossos cupons:
{all_coupons}
```

**Resultado:**
```
🎟️ Use nossos cupons:
CUPONS: DESC10, FRETEGRATIS, NATAL20
```

---

## 💸 Preço com Cupom

**Descrição:** Mostra o preço do produto com o melhor desconto aplicado automaticamente.

| Namespace | Exemplo |
|-----------|---------|
| `{price_with_coupon}` | 89.91 |
| `{preco_com_cupom}` | 89.91 |

**Lógica:**
1. Sistema calcula o desconto de **todos** os cupons selecionados
2. Aplica o **melhor desconto** (maior economia)
3. Respeita o **limite máximo** (se houver)
4. Valida o **valor mínimo** (se houver)
5. Nunca resulta em preço negativo

**Exemplo de Uso:**
```
De: R$ {price}
Por: R$ {price_with_coupon} com cupom!
```

**Resultado:**
```
De: R$ 99,90
Por: R$ 89,91 com cupom!
```

---

## 📝 Exemplos Práticos

### Exemplo 1: Cupom de Porcentagem

**Template:**
```
🎁 CUPOM ESPECIAL!

Código: {coupon_code}
Desconto: {porcentagem}
Compra mínima: {valor_minimo_compra}
Desconto máximo: {valor_maximo_desconto}
Válido até: {coupon_expires}
Loja: {coupon_seller}
```

**Cupom:**
- Código: DESC10
- Tipo: Porcentagem
- Desconto: 10%
- Mínimo: R$ 100,00
- Máximo: R$ 50,00
- Validade: 31/12/2025
- Vendedor: Amazon

**Resultado:**
```
🎁 CUPOM ESPECIAL!

Código: DESC10
Desconto: 10%
Compra mínima: R$ 100,00
Desconto máximo: R$ 50,00
Válido até: 31/12/2025
Loja: Amazon
```

---

### Exemplo 2: Cupom de Valor Fixo

**Template:**
```
💰 GANHE DESCONTO!

Use o cupom {code}
Ganhe {desconto_fixo} de desconto
Válido para compras acima de {minimo}
Na {seller}
```

**Cupom:**
- Código: GANHE20
- Tipo: Valor Fixo
- Desconto: R$ 20,00
- Mínimo: R$ 100,00
- Vendedor: Mercado Livre

**Resultado:**
```
💰 GANHE DESCONTO!

Use o cupom GANHE20
Ganhe R$ 20,00 de desconto
Válido para compras acima de R$ 100,00
Na Mercado Livre
```

---

### Exemplo 3: Template Universal (funciona para ambos os tipos)

**Template:**
```
🔥 OFERTA ESPECIAL!

{product_name}
De R$ {price}
Por R$ {price_with_coupon} com cupom

{all_coupons}

Aproveite!
```

**Resultado (com 2 cupons):**
```
🔥 OFERTA ESPECIAL!

Controle PS5 DualSense
De R$ 399,00
Por R$ 359,10 com cupom

CUPONS: DESC10, FRETEGRATIS

Aproveite!
```

---

### Exemplo 4: Template Detalhado

**Template:**
```
🎟️ CUPOM DISPONÍVEL
━━━━━━━━━━━━━━━━━━

📋 Código: {coupon_code}

💰 Desconto:
{% if porcentagem %}
   {porcentagem} (até {maximo})
{% else %}
   {desconto_fixo}
{% endif %}

🛒 Compra mínima: {valor_minimo_compra}
⏰ Válido até: {coupon_expires}
🏪 Loja: {coupon_seller}

━━━━━━━━━━━━━━━━━━
💵 PREÇO COM CUPOM: R$ {price_with_coupon}
```

**Resultado (cupom de 10% com limite):**
```
🎟️ CUPOM DISPONÍVEL
━━━━━━━━━━━━━━━━━━

📋 Código: DESC10

💰 Desconto:
   10% (até R$ 50,00)

🛒 Compra mínima: R$ 100,00
⏰ Válido até: 31/12/2025
🏪 Loja: Amazon

━━━━━━━━━━━━━━━━━━
💵 PREÇO COM CUPOM: R$ 359,10
```

---

## 📊 Tabela Resumo de Namespaces

| Categoria | Namespace Principal | Aliases | Formato |
|-----------|-------------------|---------|---------|
| **Código** | `{coupon_code}` | `{code}` | Texto |
| **Vendedor** | `{coupon_seller}` | `{seller}`, `{seller_name}` | Texto |
| **% Desconto** | `{porcentagem}` | `{percentual}`, `{desconto_porcentagem}` | XX% |
| **$ Desconto** | `{desconto_fixo}` | `{valor_fixo}` | R$ XX,XX |
| **Mínimo** | `{valor_minimo_compra}` | `{minimo}`, `{compra_minima}` | R$ XX,XX |
| **Máximo** | `{valor_maximo_desconto}` | `{maximo}`, `{limite}` | R$ XX,XX |
| **Validade** | `{coupon_expires}` | `{validade_cupom}`, `{expira_em}` | DD/MM/YYYY |
| **Lista** | `{all_coupons}` | `{todos_cupons}`, `{cupons}` | CUPONS: A, B |
| **Preço Final** | `{price_with_coupon}` | `{preco_com_cupom}` | XX.XX |

---

## 💡 Dicas de Uso

### 1. Use Nomes Intuitivos

**✅ Recomendado:**
```
Desconto: {porcentagem}
Mínimo: {minimo}
Máximo: {maximo}
```

**⚠️ Funciona mas menos intuitivo:**
```
Desconto: {coupon_discount_value}
Mínimo: {min_purchase_value}
Máximo: {max_discount_value}
```

### 2. Diferencie Tipo de Desconto

Para templates que precisam distinguir entre % e valor fixo:

```
{% if porcentagem %}
   Ganhe {porcentagem} de desconto!
{% else %}
   Ganhe {desconto_fixo} de desconto!
{% endif %}
```

### 3. Trate Valores Opcionais

Para campos que podem estar vazios:

```
{% if minimo != 'Sem mínimo' %}
   ⚠️ Compra mínima: {minimo}
{% endif %}
```

### 4. Combine com Namespaces de Oferta

```
🔥 {product_name}
💰 De R$ {old_price} por R$ {price}
🎟️ Com cupom {code}: R$ {price_with_coupon}
📦 {parcelamento}
```

---

## 🚀 Scripts de Setup

### Adicionar Novos Namespaces

```bash
python scripts/reorganize_coupon_namespaces.py
```

### Verificar Namespaces Existentes

```bash
sqlite3 instance/app.db "SELECT name, label FROM namespaces WHERE scope = 'COUPON' ORDER BY name;"
```

---

## 📚 Documentação Relacionada

- [COUPON_DISCOUNT_FEATURE.md](COUPON_DISCOUNT_FEATURE.md) - Sistema de descontos
- [MIN_PURCHASE_VALUE_FEATURE.md](MIN_PURCHASE_VALUE_FEATURE.md) - Valor mínimo
- [MAX_DISCOUNT_LIMIT.md](MAX_DISCOUNT_LIMIT.md) - Limite máximo
- [COUPON_SELLER_FILTER.md](COUPON_SELLER_FILTER.md) - Filtro por vendedor

---

**Última Atualização:** 04/12/2025  
**Versão:** 2.0  
**Status:** ✅ Completo e Atualizado

