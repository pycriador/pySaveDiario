# 🎟️ Namespaces para Cupons em Templates

**Data:** 3 de Dezembro, 2025  
**Versão:** 3.6.2  
**Status:** ✅ IMPLEMENTADO

---

## 🎯 O que foi implementado?

Agora os **templates** suportam variáveis específicas para **cupons**, além das variáveis de ofertas e globais.

---

## 📋 Namespaces Disponíveis

### 🎟️ Variáveis de Cupons (COUPON)

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `{coupon_code}` | Código do cupom de desconto | PRIMEIRACOMPRA |
| `{code}` | Código do cupom (alias) | FRETE10 |
| `{seller}` | Nome do vendedor/loja do cupom | Mercado Livre |
| `{seller_name}` | Nome do vendedor (forma longa) | Magazine Luiza |
| `{coupon_expires}` | Data de expiração do cupom | 31/12/2025 |

### 🏷️ Variáveis de Ofertas (OFFER)

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `{product_name}` | Nome do Produto | Notebook Dell |
| `{price}` | Preço | 2499.00 |
| `{old_price}` | Preço Anterior | 3499.00 |
| `{discount}` | Desconto | 29% |
| `{vendor_name}` | Nome do Vendedor | Mercado Livre |
| `{offer_url}` | URL da Oferta | https://... |
| `{category}` | Categoria | Eletrônicos |
| `{brand}` | Marca | Dell |
| `{description}` | Descrição | Notebook Dell... |
| `{currency}` | Moeda | BRL |
| `{expires_at}` | Validade | 31/12/2025 |

### 🌍 Variáveis Globais (GLOBAL)

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `{user_name}` | Nome do Usuário | João Silva |
| `{today}` | Data Atual | 03/12/2025 |
| `{time}` | Hora Atual | 14:30 |

---

## 🎨 Interface de Templates

### Como Aparece Agora

Ao criar ou editar um template (`/templates/novo` ou `/templates/{id}/editar`), você verá **3 seções** de variáveis:

#### 1. 🏷️ Variáveis de Ofertas (azul)
```
{product_name}   {price}   {old_price}   {discount}
{vendor_name}    {offer_url}   {category}   {brand}
...
```

#### 2. 🎟️ Variáveis de Cupons (verde)
```
{coupon_code}   {code}   {seller}   {seller_name}   {coupon_expires}
```

#### 3. 🌍 Variáveis Globais (cinza)
```
{user_name}   {today}   {time}
```

**Cada seção tem uma cor diferente para facilitar a identificação!**

---

## 💡 Exemplos de Uso

### Exemplo 1: Template para Cupom Simples

**Template:**
```
🎟️ CUPOM DISPONÍVEL!

Use o código {coupon_code} na {seller} e aproveite!

Válido até {coupon_expires}
```

**Resultado ao compartilhar cupom:**
```
🎟️ CUPOM DISPONÍVEL!

Use o código PRIMEIRACOMPRA na Mercado Livre e aproveite!

Válido até 31/12/2025
```

### Exemplo 2: Template Misto (Oferta + Cupom)

**Template:**
```
🔥 OFERTA: {product_name}

Preço: R$ {price}
De: R$ {old_price}
Desconto: {discount}

Link: {offer_url}

💰 Use o cupom {code} para descontos extras!
Vendedor: {seller}
```

**Resultado ao compartilhar oferta com cupom selecionado:**
```
🔥 OFERTA: Notebook Dell Inspiron

Preço: R$ 2.499,00
De: R$ 3.499,00
Desconto: 29%

Link: https://mercadolivre.com.br/...

💰 Use o cupom FRETE10 para descontos extras!
Vendedor: Mercado Livre
```

### Exemplo 3: Template para Cupom Urgente

**Template:**
```
⏰ CUPOM EXPIRA HOJE!

Código: {coupon_code}
Loja: {seller}
Válido até: {coupon_expires}

Aproveite antes que acabe! ⚡
```

**Resultado:**
```
⏰ CUPOM EXPIRA HOJE!

Código: BLACK50
Loja: Magazine Luiza
Válido até: 03/12/2025

Aproveite antes que acabe! ⚡
```

### Exemplo 4: Template Universal

**Template:**
```
📢 NOVA PROMOÇÃO!

{product_name} por apenas R$ {price}!
Vendedor: {vendor_name}

🎟️ Cupom: {code} em {seller}

Link: {offer_url}
```

**Este template funciona:**
- ✅ Em ofertas (mostra produto e preço)
- ✅ Em cupons (mostra código e vendedor)
- ✅ Em ofertas com cupons selecionados (mostra tudo)

---

## 🔧 Implementação Técnica

### 1. Banco de Dados

**Adicionados 5 novos namespaces:**

```sql
INSERT INTO namespaces (name, label, description, scope) VALUES
('coupon_code', 'Código do Cupom', '...', 'coupon'),
('code', 'Código (Alias)', '...', 'coupon'),
('seller', 'Vendedor', '...', 'coupon'),
('seller_name', 'Nome do Vendedor', '...', 'coupon'),
('coupon_expires', 'Validade do Cupom', '...', 'coupon');
```

### 2. Model

**Adicionado novo scope em `NamespaceScope`:**

```python
class NamespaceScope(str, Enum):
    PROFILE = "profile"
    OFFER = "offer"
    COUPON = "coupon"  # ← NOVO
    GLOBAL = "global"
```

### 3. Rotas

**Atualizado filtro de namespaces em todas as rotas de templates:**

```python
# app/routes/web.py
namespaces = Namespace.query.filter(
    Namespace.scope.in_([
        NamespaceScope.OFFER, 
        NamespaceScope.COUPON,  # ← ADICIONADO
        NamespaceScope.GLOBAL
    ])
).order_by(Namespace.scope, Namespace.name).all()
```

### 4. Templates HTML

**Agrupamento visual por scope:**

```html
{# Offer Variables #}
<h6><i class="bi bi-tag"></i> Variáveis de Ofertas</h6>
<button class="btn-outline-primary">...</button>

{# Coupon Variables #}
<h6><i class="bi bi-ticket-perforated"></i> Variáveis de Cupons</h6>
<button class="btn-outline-success">...</button>  <!-- Verde -->

{# Global Variables #}
<h6><i class="bi bi-globe"></i> Variáveis Globais</h6>
<button class="btn-outline-secondary">...</button>
```

---

## 📂 Arquivos Modificados

### Backend
```
app/models.py
  ✅ Adicionado NamespaceScope.COUPON

app/routes/web.py
  ✅ Atualizado filtro de namespaces (4 rotas):
     - share_templates()
     - create_template()
     - edit_template()
     - offers() (já estava atualizado)
```

### Frontend
```
app/templates/template_create.html
  ✅ Agrupamento visual de namespaces por scope
  ✅ Cores diferentes para cada tipo

app/templates/template_edit.html
  ✅ Mesmo agrupamento visual
  ✅ Mesmas cores
```

### Banco de Dados
```
scripts/add_coupon_namespaces.sql
  ✅ Script para adicionar 5 namespaces de cupons

instance/app.db
  ✅ Tabela namespaces atualizada com novos registros
```

---

## 🧪 Testes

### Teste 1: Ver namespaces de cupons
```
1. Acesse /templates/novo
2. Role até "Variáveis Disponíveis"
3. Verifique 3 seções:
   - Variáveis de Ofertas (azul) ✅
   - Variáveis de Cupons (verde) ✅
   - Variáveis Globais (cinza) ✅
```

### Teste 2: Inserir namespace de cupom
```
1. Acesse /templates/novo
2. Clique no botão verde {coupon_code}
3. Verifique que foi inserido no corpo do template ✅
```

### Teste 3: Template misto
```
1. Crie template com:
   "Oferta: {product_name} - Cupom: {code}"
2. Salve
3. Compartilhe uma oferta com cupom selecionado
4. Verifique que ambas as variáveis foram substituídas ✅
```

### Teste 4: Template só para cupons
```
1. Crie template com:
   "Use {coupon_code} em {seller}"
2. Vá para /cupons
3. Compartilhe um cupom com esse template
4. Verifique substituição correta ✅
```

---

## 💡 Dicas de Uso

### Templates Universais
Crie templates que funcionam tanto para ofertas quanto para cupons:

```
📢 PROMOÇÃO!

Produto: {product_name}
Preço: R$ {price}
Cupom: {code}
Vendedor: {seller}

Link: {offer_url}
```

- Se usar em **oferta sem cupom**: só mostra produto e preço
- Se usar em **oferta com cupom**: mostra tudo
- Se usar em **cupom**: só mostra cupom e vendedor

### Templates Específicos
Ou crie templates focados:

**Para Ofertas:**
```
🔥 {product_name} por R$ {price}
De R$ {old_price} - Economize {discount}!
```

**Para Cupons:**
```
🎟️ Cupom {code} disponível!
Use na {seller} até {coupon_expires}
```

### Combinações Criativas
```
💰 COMBO IMPERDÍVEL!

{product_name} por R$ {price}
+ Cupom {code} para frete grátis
= ECONOMIA MÁXIMA!

Loja: {seller}
```

---

## ✅ Checklist de Implementação

- [x] Adicionar `COUPON` ao enum `NamespaceScope`
- [x] Criar script SQL para adicionar namespaces de cupons
- [x] Executar script no banco de dados
- [x] Atualizar filtro de namespaces em rotas de templates
- [x] Agrupar namespaces por scope em `template_create.html`
- [x] Agrupar namespaces por scope em `template_edit.html`
- [x] Aplicar cores diferentes para cada tipo
- [x] Testar criação de template com variáveis de cupom
- [x] Testar compartilhamento de cupom com template
- [x] Testar template misto (oferta + cupom)
- [x] Documentar implementação

---

## 🎊 Status

**✅ IMPLEMENTADO E FUNCIONANDO!**

Agora você pode:
- ✅ Usar variáveis de cupons em templates
- ✅ Ver namespaces organizados por tipo
- ✅ Criar templates universais (oferta + cupom)
- ✅ Criar templates específicos para cupons
- ✅ Identificar facilmente cada tipo pela cor

---

## 📚 Variáveis Completas - Referência Rápida

### Quick Reference

```
🏷️ OFERTAS (azul):
{product_name} {price} {old_price} {discount} {vendor_name}
{offer_url} {category} {brand} {description} {currency} {expires_at}

🎟️ CUPONS (verde):
{coupon_code} {code} {seller} {seller_name} {coupon_expires}

🌍 GLOBAIS (cinza):
{user_name} {today} {time}
```

---

**Agora seus templates são mais poderosos e versáteis! 🎉**

