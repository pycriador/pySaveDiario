# 🛡️ Limite Máximo de Desconto em Cupons

## 📋 Visão Geral

Sistema de **limite máximo de desconto** para cupons com desconto por porcentagem. Permite definir um teto de desconto em reais, garantindo que descontos percentuais não ultrapassem um valor específico.

---

## 🎯 Caso de Uso

### Problema

```
Cupom: 10% de desconto
Produto R$ 500: desconto de R$ 50 ✅
Produto R$ 1.000: desconto de R$ 100 ❌ (muito alto!)
```

### Solução

```
Cupom: 10% de desconto, MÁXIMO R$ 70
Produto R$ 500: desconto de R$ 50 ✅
Produto R$ 1.000: desconto limitado a R$ 70 ✅
```

---

## ✨ Como Funciona

### Exemplo Prático

**Cupom:** `DESCONTO10`
- **Tipo:** Porcentagem
- **Valor:** 10%
- **Desconto Máximo:** R$ 70,00

### Cálculos

| Preço Original | Desconto Calculado (10%) | Desconto Aplicado | Preço Final |
|----------------|--------------------------|-------------------|-------------|
| R$ 100,00 | R$ 10,00 | R$ 10,00 | R$ 90,00 |
| R$ 500,00 | R$ 50,00 | R$ 50,00 | R$ 450,00 |
| R$ 700,00 | R$ 70,00 | **R$ 70,00** | R$ 630,00 |
| R$ 1.000,00 | R$ 100,00 | **R$ 70,00** ⚠️ | R$ 930,00 |
| R$ 2.000,00 | R$ 200,00 | **R$ 70,00** ⚠️ | R$ 1.930,00 |

⚠️ = Desconto limitado ao valor máximo

---

## 🏗️ Implementação

### 1. Campo no Modelo

**Arquivo:** `app/models.py`

```python
class Coupon(TimestampMixin, db.Model):
    # ... existing fields ...
    
    discount_type = db.Column(db.String(20), default='percentage')
    discount_value = db.Column(db.Numeric(10, 2), nullable=True)
    max_discount_value = db.Column(db.Numeric(10, 2), nullable=True)  # ← NOVO
    
    def calculate_discount(self, original_price):
        """Calculate discounted price with max limit"""
        if not self.discount_value or original_price is None:
            return original_price
        
        discount_amount = 0
        
        if self.discount_type == 'percentage':
            discount_amount = (float(original_price) * float(self.discount_value)) / 100
            
            # Apply max discount limit if set
            if self.max_discount_value:
                discount_amount = min(discount_amount, float(self.max_discount_value))
        
        elif self.discount_type == 'fixed':
            discount_amount = float(self.discount_value)
        
        discounted_price = float(original_price) - discount_amount
        return max(0, discounted_price)
```

---

### 2. Formulário

**Arquivo:** `app/forms.py`

```python
class CouponForm(FlaskForm):
    # ... existing fields ...
    
    discount_type = SelectField("Tipo de desconto", 
                               choices=[('percentage', 'Porcentagem (%)'), 
                                       ('fixed', 'Valor fixo (R$)')])
    discount_value = DecimalField("Valor do desconto", places=2)
    max_discount_value = DecimalField("Desconto máximo (R$)", places=2)  # ← NOVO
```

---

### 3. Template de Criação/Edição

**Arquivo:** `coupon_create.html` / `coupon_edit.html`

```html
<div class="col-md-6">
  <label class="form-label">
    <i class="bi bi-cash-coin"></i> Valor do desconto
  </label>
  {{ form.discount_value(class="form-control", placeholder="Ex: 10") }}
  <small class="text-muted">
    <i class="bi bi-info-circle"></i> 10 para 10% de desconto
  </small>
</div>

<div class="col-md-6">
  <label class="form-label">
    <i class="bi bi-shield-fill-check"></i> Desconto máximo (opcional)
  </label>
  {{ form.max_discount_value(class="form-control", placeholder="Ex: 70") }}
  <small class="text-muted">
    <i class="bi bi-info-circle"></i> Limite máximo em R$ (ex: 70 para máx R$ 70)
  </small>
</div>
```

---

### 4. Página de Compartilhamento

**Arquivo:** `offer_share.html`

#### HTML - Data Attributes

```html
<input type="checkbox" 
       class="coupon-checkbox"
       data-coupon-code="{{ coupon.code }}"
       data-coupon-discount-type="{{ coupon.discount_type }}"
       data-coupon-discount-value="{{ coupon.discount_value }}"
       data-coupon-max-discount-value="{{ coupon.max_discount_value or 0 }}"
       checked>
```

#### JavaScript - Cálculo

```javascript
document.querySelectorAll('.coupon-checkbox:checked').forEach(checkbox => {
  const discountType = checkbox.getAttribute('data-coupon-discount-type');
  const discountValue = parseFloat(checkbox.getAttribute('data-coupon-discount-value')) || 0;
  const maxDiscountValue = parseFloat(checkbox.getAttribute('data-coupon-max-discount-value')) || 0;
  
  if (discountType === 'percentage') {
    let discountAmount = (price * discountValue) / 100;
    
    // Apply max discount limit if set
    if (maxDiscountValue > 0) {
      discountAmount = Math.min(discountAmount, maxDiscountValue);
    }
    
    discountedPrice = price - discountAmount;
  }
});
```

#### Badge Visual

```html
{% if coupon.discount_value %}
<span class="badge bg-success ms-2">
  {% if coupon.discount_type == 'percentage' %}
  -{{ coupon.discount_value }}%
  {% if coupon.max_discount_value %}
  <small>(máx R$ {{ "%.2f"|format(coupon.max_discount_value) }})</small>
  {% endif %}
  {% endif %}
</span>
{% endif %}
```

**Resultado visual:**
```
-10% (máx R$ 70.00)
```

---

## 📝 Rotas Atualizadas

### Criar Cupom

**Rota:** `POST /cupons/novo`

```python
@web_bp.route("/cupons/novo", methods=["GET", "POST"])
def create_coupon():
    # ... validation ...
    
    coupon = Coupon(
        seller_id=form.seller_id.data,
        code=form.code.data.upper(),
        discount_type=form.discount_type.data,
        discount_value=form.discount_value.data,
        max_discount_value=form.max_discount_value.data,  # ← NOVO
        created_by=current_user
    )
    
    db.session.add(coupon)
    db.session.commit()
```

---

### Editar Cupom

**Rota:** `POST /cupons/<id>/editar`

```python
@web_bp.route("/cupons/<int:coupon_id>/editar", methods=["GET", "POST"])
def edit_coupon(coupon_id):
    coupon = Coupon.query.get_or_404(coupon_id)
    
    if request.method == "GET":
        form.max_discount_value.data = float(coupon.max_discount_value) if coupon.max_discount_value else None
    
    if request.method == "POST":
        coupon.max_discount_value = form.max_discount_value.data if form.max_discount_value.data else None
        db.session.commit()
```

---

## 🗄️ Migração do Banco de Dados

### Script SQL

**Arquivo:** `scripts/add_max_discount_value_to_coupons.sql`

```sql
-- Add max_discount_value column to coupons table
ALTER TABLE coupons ADD COLUMN max_discount_value NUMERIC(10, 2);
```

### Script Python

**Arquivo:** `scripts/add_max_discount_value_to_coupons.py`

```python
from app import create_app, db

app = create_app()
with app.app_context():
    with db.engine.connect() as conn:
        conn.execute(db.text(
            "ALTER TABLE coupons ADD COLUMN max_discount_value NUMERIC(10, 2)"
        ))
        conn.commit()
```

**Executar:**
```bash
python scripts/add_max_discount_value_to_coupons.py
```

---

## 💡 Casos de Uso Reais

### 1. E-commerce de Eletrônicos

```
Cupom: TECH10
- 10% de desconto
- Máximo: R$ 200

Notebook R$ 5.000:
  10% = R$ 500, mas limitado a R$ 200
  Preço final: R$ 4.800

Mouse R$ 150:
  10% = R$ 15 (abaixo do limite)
  Preço final: R$ 135
```

---

### 2. Loja de Roupas

```
Cupom: VERÃO15
- 15% de desconto
- Máximo: R$ 100

Vestido R$ 800:
  15% = R$ 120, mas limitado a R$ 100
  Preço final: R$ 700

Camiseta R$ 80:
  15% = R$ 12 (abaixo do limite)
  Preço final: R$ 68
```

---

### 3. Marketplace

```
Cupom: PRIMEIRASCOMPRAS
- 20% de desconto
- Máximo: R$ 50

Para novos clientes, desconto generoso mas limitado
```

---

## 🎨 Interface do Usuário

### Formulário de Criação de Cupom

```
┌────────────────────────────────────┐
│ Novo Cupom                         │
├────────────────────────────────────┤
│ Vendedor: [Mercado Livre     ▼]   │
│ Código: [DESCONTO10________]       │
│                                    │
│ Tipo de desconto:                  │
│ ○ Porcentagem (%)                  │
│ ○ Valor fixo (R$)                  │
│                                    │
│ Valor do desconto: [10____]        │
│ 💡 10 para 10% de desconto         │
│                                    │
│ Desconto máximo: [70______]        │
│ 💡 Limite máximo em R$ (ex: 70)    │
│                                    │
│ [Salvar cupom]                     │
└────────────────────────────────────┘
```

---

### Lista de Cupons na Página de Compartilhamento

```
┌────────────────────────────────────┐
│ Cupons Disponíveis:                │
├────────────────────────────────────┤
│ ☑ DESCONTO10 - Mercado Livre       │
│   [-10% (máx R$ 70.00)]            │  ← Badge com limite
│                                    │
│ ☑ PRIMEIRACOMPRA - Shopee          │
│   [-20% (máx R$ 50.00)]            │
│                                    │
│ ☑ FIXO50 - Magazine Luiza          │
│   [-R$ 50.00]                      │  ← Sem limite (fixo)
└────────────────────────────────────┘
```

---

## 🧮 Algoritmo de Cálculo

### Fluxo Completo

```
1. Usuário marca checkbox "Aplicar desconto dos cupons"
2. Sistema coleta todos os cupons selecionados
3. Para cada cupom:
   a. Se tipo = 'percentage':
      - Calcula: discount_amount = price * (discount_value / 100)
      - Se max_discount_value existe:
        - discount_amount = min(discount_amount, max_discount_value)
   b. Se tipo = 'fixed':
      - discount_amount = discount_value
   c. Aplica desconto: new_price = price - discount_amount
4. Retorna o melhor preço (menor valor)
5. Substitui namespace {price_with_coupon}
```

---

### Pseudo-código

```python
def calculate_best_price_with_coupons(original_price, coupons):
    best_price = original_price
    
    for coupon in coupons:
        if coupon.discount_type == 'percentage':
            discount = (original_price * coupon.discount_value) / 100
            
            # Apply max limit
            if coupon.max_discount_value:
                discount = min(discount, coupon.max_discount_value)
            
            new_price = original_price - discount
        
        elif coupon.discount_type == 'fixed':
            new_price = original_price - coupon.discount_value
        
        # Track best price
        if new_price < best_price:
            best_price = new_price
    
    return max(0, best_price)  # Never negative
```

---

## 🧪 Exemplos de Teste

### Teste 1: Desconto Abaixo do Limite

```python
# Cupom: 10% max R$ 70
original_price = 500.00
discount_value = 10  # 10%
max_discount_value = 70.00

calculated_discount = 500 * 0.10 = 50.00
applied_discount = min(50.00, 70.00) = 50.00
final_price = 500.00 - 50.00 = 450.00 ✅
```

---

### Teste 2: Desconto Acima do Limite

```python
# Cupom: 10% max R$ 70
original_price = 1000.00
discount_value = 10  # 10%
max_discount_value = 70.00

calculated_discount = 1000 * 0.10 = 100.00
applied_discount = min(100.00, 70.00) = 70.00 ⚠️
final_price = 1000.00 - 70.00 = 930.00 ✅
```

---

### Teste 3: Sem Limite Definido

```python
# Cupom: 10% sem limite
original_price = 1000.00
discount_value = 10  # 10%
max_discount_value = None

calculated_discount = 1000 * 0.10 = 100.00
applied_discount = 100.00  # Sem limite
final_price = 1000.00 - 100.00 = 900.00 ✅
```

---

### Teste 4: Desconto Fixo (Ignora Limite)

```python
# Cupom: R$ 50 fixo (max_discount não se aplica)
original_price = 1000.00
discount_type = 'fixed'
discount_value = 50.00
max_discount_value = 70.00  # Ignorado

applied_discount = 50.00
final_price = 1000.00 - 50.00 = 950.00 ✅
```

---

## 📊 Comparação: Com e Sem Limite

### Produto: R$ 1.000,00

| Cupom | Sem Limite | Com Limite R$ 70 | Diferença |
|-------|------------|------------------|-----------|
| 5% | R$ 950,00 | R$ 950,00 | - |
| 10% | R$ 900,00 | R$ 930,00 | +R$ 30 |
| 15% | R$ 850,00 | R$ 930,00 | +R$ 80 |
| 20% | R$ 800,00 | R$ 930,00 | +R$ 130 |

**Conclusão:** O limite protege o vendedor em produtos de alto valor.

---

## ✅ Checklist de Implementação

### Backend
- [x] Adicionar coluna `max_discount_value` ao modelo `Coupon`
- [x] Atualizar método `calculate_discount()` com lógica de limite
- [x] Criar script de migração SQL
- [x] Executar migração no banco de dados
- [x] Adicionar campo ao formulário `CouponForm`
- [x] Atualizar rota `create_coupon`
- [x] Atualizar rota `edit_coupon`

### Frontend
- [x] Adicionar campo no template `coupon_create.html`
- [x] Adicionar campo no template `coupon_edit.html`
- [x] Adicionar `data-coupon-max-discount-value` em `offer_share.html`
- [x] Atualizar JavaScript para coletar `maxDiscountValue`
- [x] Atualizar lógica de cálculo no JavaScript
- [x] Adicionar badge visual com limite

### Documentação
- [x] Criar `MAX_DISCOUNT_LIMIT.md`
- [x] Atualizar `COUPON_DISCOUNT_FEATURE.md`
- [x] Adicionar exemplos práticos
- [x] Documentar casos de uso

---

## 🎯 Benefícios

### Para o Vendedor
- ✅ Controla o máximo de desconto em produtos caros
- ✅ Mantém margem de lucro
- ✅ Oferece desconto atrativo sem prejuízo
- ✅ Flexibilidade em campanhas

### Para o Comprador
- ✅ Desconto justo em qualquer produto
- ✅ Transparência no valor máximo
- ✅ Incentivo para compras menores

### Para o Sistema
- ✅ Cálculos precisos
- ✅ Regras de negócio claras
- ✅ Fácil manutenção
- ✅ Extensível

---

## 🚀 Como Usar

### 1. Criar Cupom com Limite

```bash
1. Acesse: http://localhost:5000/cupons/novo
2. Preencha:
   - Vendedor: Mercado Livre
   - Código: DESCONTO10
   - Tipo: Porcentagem (%)
   - Valor: 10
   - Desconto máximo: 70
3. Salvar
```

---

### 2. Testar na Página de Compartilhamento

```bash
1. Crie uma oferta de R$ 1.000
2. Acesse: /ofertas/1/compartilhar
3. Veja o cupom listado: -10% (máx R$ 70.00)
4. Marque "Aplicar desconto dos cupons"
5. Veja preço calculado: R$ 930,00 (limitado)
```

---

### 3. Verificar Badge Visual

```html
Na lista de cupons:
-10% (máx R$ 70.00)  ← Limite visível
```

---

## 🎉 Conclusão

Sistema de **limite máximo de desconto** implementado com sucesso!

- ✅ Campo `max_discount_value` adicionado
- ✅ Cálculo com limite implementado (backend + frontend)
- ✅ Interface atualizada com badge informativo
- ✅ Migração de banco executada
- ✅ Totalmente documentado

**Status:** 🟢 **COMPLETO E PRONTO PARA USO**

---

**Última atualização:** 04/12/2025

