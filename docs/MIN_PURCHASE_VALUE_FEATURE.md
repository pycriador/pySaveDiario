# 🛒 Valor Mínimo da Compra - Cupons

## 📋 Visão Geral

Funcionalidade que permite definir um **valor mínimo de compra** para aplicar cupons de desconto. Essencial para cupons de porcentagem, mas também aplicável a cupons de valor fixo.

---

## ✨ Funcionalidade

### Novo Campo: `min_purchase_value`

**Descrição:** Valor mínimo que o cliente precisa comprar para que o cupom seja aplicado.

**Tipo:** NUMERIC(10, 2)  
**Opcional:** Sim  
**Moeda:** R$ (Reais)

---

## 🎯 Casos de Uso

### Caso 1: Cupom de Porcentagem com Limite

```
Código: DESC10
Tipo: Porcentagem (%)
Desconto: 10%
Compra mínima: R$ 100,00
Desconto máximo: R$ 50,00
```

**Comportamento:**
- Compra de R$ 80 → Cupom **não** aplicável
- Compra de R$ 150 → Desconto de R$ 15 (10% de R$ 150)
- Compra de R$ 600 → Desconto de R$ 50 (limitado ao máximo, não R$ 60)

### Caso 2: Cupom de Valor Fixo

```
Código: GANHE20
Tipo: Valor Fixo (R$)
Desconto: R$ 20,00
Compra mínima: R$ 100,00
Desconto máximo: R$ 20,00
```

**Comportamento:**
- Compra de R$ 80 → Cupom **não** aplicável
- Compra de R$ 120 → Desconto de R$ 20 → Preço final R$ 100

**Nota:** Para valor fixo, geralmente `min_purchase_value` e `max_discount_value` têm o mesmo valor.

### Caso 3: Cupom sem Mínimo

```
Código: FRETE
Tipo: Valor Fixo (R$)
Desconto: R$ 10,00
Compra mínima: (vazio)
Desconto máximo: R$ 10,00
```

**Comportamento:**
- Qualquer valor de compra → Desconto de R$ 10

---

## 🔧 Implementação Técnica

### 1. Modelo (`app/models.py`)

```python
class Coupon(TimestampMixin, db.Model):
    # ... existing fields ...
    discount_type = db.Column(db.String(20), default='percentage')
    discount_value = db.Column(db.Numeric(10, 2), nullable=True)
    min_purchase_value = db.Column(db.Numeric(10, 2), nullable=True)  # NOVO
    max_discount_value = db.Column(db.Numeric(10, 2), nullable=True)
    
    def calculate_discount(self, original_price):
        """Calculate discounted price with min purchase validation"""
        if not self.discount_value or original_price is None:
            return original_price
        
        # Check minimum purchase requirement
        if self.min_purchase_value and float(original_price) < float(self.min_purchase_value):
            return original_price  # Coupon not applicable
        
        # ... rest of calculation ...
```

### 2. Formulário (`app/forms.py`)

```python
class CouponForm(FlaskForm):
    discount_value = DecimalField("Valor do desconto", ...)
    min_purchase_value = DecimalField("Valor mínimo da compra (R$)", 
                                      validators=[Optional(), NumberRange(min=0)], 
                                      places=2)
    max_discount_value = DecimalField("Desconto máximo (R$)", ...)
```

### 3. Rotas (`app/routes/web.py`)

**Criar cupom:**
```python
coupon = Coupon(
    # ... other fields ...
    discount_value=form.discount_value.data,
    min_purchase_value=form.min_purchase_value.data,  # NOVO
    max_discount_value=form.max_discount_value.data,
)
```

**Editar cupom:**
```python
# Load for editing
form.min_purchase_value.data = float(coupon.min_purchase_value) if coupon.min_purchase_value else None

# Save changes
coupon.min_purchase_value = form.min_purchase_value.data if form.min_purchase_value.data else None
```

---

## 🎨 Interface

### Formulário de Criação/Edição

```
┌─────────────────────────────────────────────────────────────┐
│ Tipo de Desconto                                            │
│ ┌─────────────────┐                                         │
│ │ Porcentagem (%) ▼│                                         │
│ └─────────────────┘                                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┬─────────────────┬─────────────────────────┐
│ Valor do Desc.  │ Compra Mínima   │ Desconto Máximo         │
├─────────────────┼─────────────────┼─────────────────────────┤
│ [      10      ]│ [     100      ]│ [       50            ] │
│ 10 para 10%     │ R$ 100 mínimo   │ Máx R$ 50               │
└─────────────────┴─────────────────┴─────────────────────────┘
```

### Listagem de Cupons

```
┌──────────────────────────────────────┐
│ DESC10                      [✓ Ativo]│
├──────────────────────────────────────┤
│ 🏪 Amazon                            │
│                                      │
│ % Desconto: 10% (máx R$ 50,00)      │
│ 🛒 Compra mínima: R$ 100,00         │  ← NOVO
│ 📅 Expira em: 31/12/2025            │
└──────────────────────────────────────┘
```

---

## 📝 Namespaces

### Novos Namespaces Disponíveis

| Namespace | Descrição | Exemplo |
|-----------|-----------|---------|
| `{min_purchase_value}` | Valor mínimo formatado | R$ 100,00 |
| `{compra_minima}` | Alias em português | R$ 100,00 |
| `{valor_minimo}` | Alias alternativo | R$ 100,00 |

### Comportamento

**Com valor mínimo:**
```
{min_purchase_value} → R$ 100,00
```

**Sem valor mínimo:**
```
{min_purchase_value} → Sem mínimo
```

### Exemplo de Template

```
🎁 CUPOM ESPECIAL!

Código: {coupon_code}
Desconto: {coupon_discount_value}
Compra mínima: {min_purchase_value}
Desconto máximo: {max_discount_value}
Válido até: {coupon_expires}

Use na loja: {coupon_seller}
```

**Resultado:**
```
🎁 CUPOM ESPECIAL!

Código: DESC10
Desconto: 10%
Compra mínima: R$ 100,00
Desconto máximo: R$ 50,00
Válido até: 31/12/2025

Use na loja: Amazon
```

---

## 🧮 Lógica de Cálculo

### Fluxo de Validação

```mermaid
graph TD
    A[Aplicar Cupom] --> B{Cupom tem discount_value?}
    B -->|Não| C[Retornar preço original]
    B -->|Sim| D{Cupom tem min_purchase_value?}
    D -->|Não| E[Calcular desconto]
    D -->|Sim| F{Preço >= min_purchase_value?}
    F -->|Não| C
    F -->|Sim| E
    E --> G{Tipo de desconto?}
    G -->|Porcentagem| H[Calcular % do preço]
    G -->|Fixo| I[Usar valor fixo]
    H --> J{Tem max_discount_value?}
    I --> K[Aplicar desconto]
    J -->|Sim| L[Min(desconto_calculado, max_value)]
    J -->|Não| K
    L --> K
    K --> M[Retornar preço com desconto]
```

### Exemplos de Cálculo

**Cupom: 10% de desconto, mínimo R$ 100, máximo R$ 50**

| Preço Original | Aplicável? | Desconto | Preço Final |
|----------------|------------|----------|-------------|
| R$ 50,00 | ❌ Não | - | R$ 50,00 |
| R$ 90,00 | ❌ Não | - | R$ 90,00 |
| R$ 100,00 | ✅ Sim | R$ 10,00 | R$ 90,00 |
| R$ 200,00 | ✅ Sim | R$ 20,00 | R$ 180,00 |
| R$ 500,00 | ✅ Sim | R$ 50,00 (limitado) | R$ 450,00 |
| R$ 800,00 | ✅ Sim | R$ 50,00 (limitado) | R$ 750,00 |

---

## 🗄️ Migração do Banco de Dados

### Script de Migração

```bash
python scripts/add_min_purchase_value_to_coupons.py
```

### SQL Executado

```sql
ALTER TABLE coupons ADD COLUMN min_purchase_value NUMERIC(10, 2);
```

### Adicionar Namespaces

```bash
python scripts/add_min_purchase_namespaces.py
```

**Namespaces adicionados:**
- `min_purchase_value`
- `compra_minima`
- `valor_minimo`

---

## 💡 Boas Práticas

### 1. Cupons de Porcentagem

**Recomendação:** Sempre defina `min_purchase_value` e `max_discount_value`

```
✅ BOM:
- Desconto: 10%
- Mínimo: R$ 100
- Máximo: R$ 50

❌ RUIM:
- Desconto: 50%
- Mínimo: (nenhum)
- Máximo: (nenhum)
```

**Motivo:** Evita descontos excessivos ou uso indevido.

### 2. Cupons de Valor Fixo

**Recomendação:** `min_purchase_value` ≥ `discount_value`

```
✅ BOM:
- Desconto: R$ 20
- Mínimo: R$ 100
- Máximo: R$ 20

❌ RUIM:
- Desconto: R$ 50
- Mínimo: R$ 30
- Máximo: R$ 50
```

**Motivo:** Cliente não deveria ganhar dinheiro aplicando o cupom.

### 3. Frete Grátis

**Recomendação:** Valor fixo sem mínimo ou com mínimo baixo

```
✅ BOM:
- Desconto: R$ 10 (valor médio do frete)
- Mínimo: (nenhum) ou R$ 50
- Máximo: R$ 10
```

---

## 🎯 Casos de Uso Práticos

### Black Friday
```
Código: BLACKFRIDAY
Desconto: 20%
Mínimo: R$ 200
Máximo: R$ 100
```

### Frete Grátis
```
Código: FRETEGRATIS
Desconto: R$ 15
Mínimo: R$ 100
Máximo: R$ 15
```

### Primeira Compra
```
Código: PRIMEIRACOMPRA
Desconto: 15%
Mínimo: R$ 50
Máximo: R$ 30
```

### Cupom Premium
```
Código: VIP50
Desconto: R$ 50
Mínimo: R$ 300
Máximo: R$ 50
```

---

## 🐛 Solução de Problemas

### Problema: Cupom não está sendo aplicado

**Verificar:**
1. O preço da oferta atende ao `min_purchase_value`?
2. O cupom está ativo?
3. O cupom pertence ao mesmo vendedor da oferta?

**Solução:**
```bash
# Verificar dados do cupom
sqlite3 instance/app.db "
  SELECT code, discount_value, min_purchase_value, max_discount_value 
  FROM coupons 
  WHERE id = 1;
"
```

---

## 📚 Arquivos Modificados

**Backend:**
- `app/models.py` - Adicionado campo `min_purchase_value` e validação
- `app/forms.py` - Adicionado campo ao formulário
- `app/routes/web.py` - Criação e edição de cupons

**Frontend:**
- `app/templates/coupon_create.html` - Campo no formulário
- `app/templates/coupon_edit.html` - Campo no formulário
- `app/templates/coupons_list.html` - Exibição na listagem
- `app/templates/offer_share.html` - Data attribute e substituição JS

**Scripts:**
- `scripts/add_min_purchase_value_to_coupons.py` - Migração do banco
- `scripts/add_min_purchase_namespaces.py` - Adicionar namespaces

**Documentação:**
- `docs/MIN_PURCHASE_VALUE_FEATURE.md` - Este arquivo

---

## 🚀 Próximas Melhorias

- [ ] Validação no frontend para garantir mínimo ≥ desconto (valor fixo)
- [ ] Alertas visuais quando cupom não for aplicável
- [ ] Histórico de uso de cupons
- [ ] Relatório de cupons mais usados
- [ ] Cupons por categoria de produto

---

**Data de Implementação:** 04/12/2025  
**Versão:** 1.0  
**Status:** ✅ Implementado e Funcional

