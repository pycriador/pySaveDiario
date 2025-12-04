# Sistema de Filtros Dinâmicos

## 📋 Visão Geral

Sistema completo de filtros para Templates e Cupons, similar ao implementado em Ofertas. Os filtros são aplicados dinamicamente via URL e atualizam automaticamente conforme o usuário digita ou seleciona opções.

## 🎯 Funcionalidades

### Templates (`/templates`)

#### Filtros Disponíveis:

1. **Buscar** 
   - Pesquisa em: Nome, Slug e Descrição
   - Atualização automática após 500ms de digitação
   - Parâmetro URL: `?search=texto`

2. **Rede Social**
   - Filtra por rede social específica
   - Opções: Todas, Instagram, Facebook, WhatsApp, Telegram, etc.
   - Parâmetro URL: `?social_network=instagram`

#### Exemplos de URLs:

```
/templates?search=promo
/templates?social_network=whatsapp
/templates?search=desconto&social_network=instagram
```

### Cupons (`/cupons`)

#### Filtros Disponíveis:

1. **Buscar**
   - Pesquisa em: Código do cupom
   - Atualização automática após 500ms
   - Parâmetro URL: `?search=texto`

2. **Vendedor**
   - Filtra por vendedor específico
   - Dropdown com todos os vendedores ativos
   - Parâmetro URL: `?seller=1`

3. **Tipo de Desconto**
   - Opções: Todos, Porcentagem (%), Valor Fixo (R$)
   - Parâmetro URL: `?discount_type=percentage` ou `?discount_type=fixed`

4. **Apenas Ativos**
   - Checkbox para mostrar apenas cupons ativos
   - Marcado por padrão
   - Parâmetro URL: `?active_only=true` (padrão) ou `?active_only=false`

#### Exemplos de URLs:

```
/cupons?search=DESC10
/cupons?seller=1
/cupons?discount_type=percentage
/cupons?search=natal&seller=2&active_only=true
```

## 🔧 Implementação Técnica

### Backend (Flask)

#### Templates Route:

```python
@web_bp.route("/templates", methods=["GET"])
def share_templates():
    # Get filter parameters
    search = request.args.get("search", "").strip()
    social_network = request.args.get("social_network", "").strip()
    
    # Build query with filters
    query = Template.query
    
    if search:
        query = query.filter(
            db.or_(
                Template.name.ilike(f"%{search}%"),
                Template.slug.ilike(f"%{search}%"),
                Template.description.ilike(f"%{search}%")
            )
        )
    
    if social_network:
        query = query.join(Template.social_networks).filter(
            TemplateSocialNetwork.network.ilike(f"%{social_network}%")
        )
    
    templates = query.order_by(Template.created_at.desc()).all()
    ...
```

#### Cupons Route:

```python
@web_bp.route("/cupons", methods=["GET"])
def coupons():
    # Get filter parameters
    search = request.args.get("search", "").strip()
    seller_id = request.args.get("seller", type=int)
    active_only = request.args.get("active_only", "true").lower() == "true"
    discount_type = request.args.get("discount_type", "").strip()
    
    # Build query with filters
    query = Coupon.query
    
    if search:
        query = query.filter(Coupon.code.ilike(f"%{search}%"))
    
    if seller_id:
        query = query.filter(Coupon.seller_id == seller_id)
    
    if active_only:
        query = query.filter(Coupon.active == True)
    
    if discount_type:
        query = query.filter(Coupon.discount_type == discount_type)
    
    # Filter only from active sellers
    query = query.outerjoin(Seller).filter(
        db.or_(Seller.active == True, Coupon.seller_id.is_(None))
    )
    
    coupons = query.order_by(Coupon.created_at.desc()).all()
    ...
```

### Frontend (JavaScript)

#### Filtros Dinâmicos:

```javascript
function applyFilters() {
  const params = new URLSearchParams();
  
  // Collect filter values
  const search = searchInput.value.trim();
  const seller = sellerSelect.value;
  const discountType = discountTypeSelect.value;
  const activeOnly = activeOnlyCheckbox.checked;
  
  // Build URL params
  if (search) params.append('search', search);
  if (seller) params.append('seller', seller);
  if (discountType) params.append('discount_type', discountType);
  if (!activeOnly) params.append('active_only', 'false');
  
  // Navigate to filtered URL
  const url = `${window.location.pathname}?${params.toString()}`;
  window.location.href = url;
}

// Debounce for search input
let searchTimeout;
searchInput.addEventListener('input', function() {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(applyFilters, 500);
});

// Immediate update for selects and checkboxes
sellerSelect.addEventListener('change', applyFilters);
discountTypeSelect.addEventListener('change', applyFilters);
activeOnlyCheckbox.addEventListener('change', applyFilters);
```

## 🎨 UI/UX

### Design Consistente

Todos os filtros seguem o mesmo padrão visual:

1. **Panel com formulário** - Card com fundo do tema
2. **Layout em grid** - Campos organizados em colunas
3. **Ícones descritivos** - Cada campo tem um ícone Bootstrap
4. **Botão de filtrar** - Azul, alinhado ao final
5. **Limpar filtros** - Link para remover todos os filtros

### Feedback Visual

- ✅ **Valores persistem** - Filtros aplicados permanecem nos campos
- ✅ **URL compartilhável** - Copie e cole a URL para compartilhar filtros
- ✅ **Botão "Limpar"** - Aparece apenas quando há filtros ativos

## 💡 Casos de Uso

### Templates

**Encontrar template para Instagram:**
```
1. Selecione "Instagram" no dropdown
2. Sistema filtra automaticamente
3. URL atualiza para: /templates?social_network=instagram
```

**Buscar por promoção:**
```
1. Digite "promo" no campo de busca
2. Aguarde 500ms
3. Sistema filtra automaticamente
4. URL atualiza para: /templates?search=promo
```

### Cupons

**Ver apenas cupons de desconto fixo:**
```
1. Selecione "Valor Fixo (R$)" em Tipo de Desconto
2. Sistema filtra automaticamente
3. URL: /cupons?discount_type=fixed
```

**Cupons do Mercado Livre:**
```
1. Selecione "Mercado Livre" no dropdown de vendedor
2. Sistema filtra automaticamente
3. URL: /cupons?seller=1
```

**Ver cupons inativos:**
```
1. Desmarque "Mostrar apenas cupons ativos"
2. Sistema filtra automaticamente
3. URL: /cupons?active_only=false
```

## ⚡ Performance

### Otimizações:

1. **Debounce no campo de busca** - 500ms para evitar queries excessivas
2. **Queries SQL otimizadas** - Usa `ILIKE` para busca case-insensitive
3. **Joins eficientes** - Apenas quando necessário
4. **Índices no banco** - Em campos frequentemente filtrados

### Filtragem de Vendedores Inativos:

Ambas as rotas automaticamente filtram:
- ✅ Templates de vendedores inativos (se aplicável)
- ✅ Cupons de vendedores inativos

Isso garante consistência com o resto do sistema.

## 📝 Comparação com Ofertas

| Funcionalidade | Ofertas | Templates | Cupons |
|----------------|---------|-----------|--------|
| Busca por texto | ✅ | ✅ | ✅ |
| Filtro por vendedor | ✅ | ❌ | ✅ |
| Filtro por categoria | ✅ | ❌ | ❌ |
| Filtro por fabricante | ✅ | ❌ | ❌ |
| Filtro por faixa de preço | ✅ | ❌ | ❌ |
| Filtro por rede social | ❌ | ✅ | ❌ |
| Filtro por tipo desconto | ❌ | ❌ | ✅ |
| Apenas ativos | ✅ | ❌ | ✅ |
| Atualização dinâmica | ✅ | ✅ | ✅ |
| Parâmetros na URL | ✅ | ✅ | ✅ |

## 🚀 Próximos Passos (Possíveis Melhorias)

- [ ] Adicionar filtro por data de criação
- [ ] Adicionar filtro por data de expiração (cupons)
- [ ] Adicionar ordenação (A-Z, Z-A, Mais recente, Mais antigo)
- [ ] Adicionar contador de resultados
- [ ] Implementar paginação para listas grandes
- [ ] Adicionar filtros salvos (favoritos)

## 📚 Arquivos Modificados

**Backend:**
- `app/routes/web.py` - Rotas `share_templates()` e `coupons()`

**Frontend:**
- `app/templates/templates_list.html` - UI de filtros + JavaScript
- `app/templates/coupons_list.html` - UI de filtros + JavaScript

---

**Data de Implementação**: 04/12/2025  
**Versão**: 1.0

