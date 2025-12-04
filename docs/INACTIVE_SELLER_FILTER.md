# Filtro de Vendedores Inativos

## 📋 Visão Geral

Quando um vendedor é desativado, todas as suas ofertas ficam automaticamente invisíveis em todas as listagens do sistema (web, dashboard e API).

## 🎯 Funcionalidade

### Comportamento

- ✅ **Vendedor ativo**: Todas as suas ofertas aparecem normalmente
- ❌ **Vendedor inativo**: Todas as suas ofertas ficam ocultas automaticamente
- ℹ️ **Sem vendedor**: Ofertas sem vendedor associado continuam visíveis

### Onde o filtro é aplicado

1. **Página Inicial** (`/`)
   - Últimas 6 ofertas exibidas
   - Apenas de vendedores ativos

2. **Dashboard** (`/dashboard`)
   - Últimas 5 ofertas do usuário
   - Apenas de vendedores ativos

3. **Listagem de Ofertas** (`/ofertas`)
   - Todas as ofertas com filtros
   - Apenas de vendedores ativos

4. **API REST** (`GET /api/offers`)
   - Listagem via API
   - Apenas de vendedores ativos

### Onde o filtro NÃO é aplicado

As seguintes rotas não são afetadas pelo status do vendedor:

- ✅ **Edição de Oferta** (`/ofertas/<id>/editar`)
  - Admins/Editores podem editar ofertas de vendedores inativos

- ✅ **Compartilhamento** (`/ofertas/<id>/compartilhar`)
  - É possível compartilhar ofertas de vendedores inativos se você tiver o link direto

- ✅ **Deleção** (`/ofertas/<id>/delete`)
  - Admins podem deletar ofertas de vendedores inativos

## 🔧 Implementação Técnica

### Query SQL

```python
# Filtro aplicado em todas as listagens
query = Offer.query.outerjoin(Seller, Offer.seller_id == Seller.id)\
    .filter(
        db.or_(
            Seller.active == True,
            Offer.seller_id.is_(None)  # Ofertas sem vendedor
        )
    )
```

### Lógica

1. **LEFT JOIN** com a tabela `sellers`
2. Filtra apenas registros onde:
   - `seller.active = True` (vendedor ativo)
   - OU `seller_id IS NULL` (sem vendedor associado)

## 📝 Casos de Uso

### Caso 1: Desativar Mercado Livre temporariamente

```python
# 1. Desativar o vendedor
seller = Seller.query.filter_by(name='Mercado Livre').first()
seller.active = False
db.session.commit()

# 2. Resultado: Todas as ofertas do Mercado Livre ficam ocultas
# - Não aparecem em /
# - Não aparecem em /ofertas
# - Não aparecem em /dashboard
# - Não aparecem na API
```

### Caso 2: Reativar vendedor

```python
# 1. Reativar o vendedor
seller.active = True
db.session.commit()

# 2. Resultado: Todas as ofertas voltam a aparecer imediatamente
```

### Caso 3: Ofertas sem vendedor

```python
# Ofertas sem seller_id continuam visíveis
offer = Offer(
    product_id=123,
    vendor_name="Loja X",
    price=100.00,
    seller_id=None  # Sem vendedor associado
)
# Esta oferta sempre aparecerá nas listagens
```

## 🚀 Como Usar

### Web Interface

1. Acesse `/admin/sellers`
2. Clique no botão **amarelo** (pausar) para desativar
3. Todas as ofertas daquele vendedor ficam ocultas imediatamente
4. Clique no botão **verde** (play) para reativar
5. Ofertas voltam a aparecer

### API

```bash
# Desativar vendedor via API
PUT /api/sellers/1
{
  "active": false
}

# Reativar vendedor via API
PUT /api/sellers/1
{
  "active": true
}
```

## 💡 Benefícios

1. **Controle Total**: Oculte ofertas de vendedores problemáticos instantaneamente
2. **Reversível**: Reative quando resolver o problema
3. **Automático**: Não precisa ocultar/deletar ofertas manualmente
4. **Consistente**: Funciona em todo o sistema (web + API)
5. **Seguro**: Dados não são perdidos, apenas ficam ocultos

## ⚠️ Observações Importantes

- ⚠️ **Não deleta as ofertas**: Apenas as oculta das listagens
- ⚠️ **Links diretos**: Usuários com link direto ainda podem acessar a oferta
- ⚠️ **Editores**: Admins e Editores podem editar ofertas de vendedores inativos
- ⚠️ **Dados preservados**: Todas as informações permanecem no banco de dados

## 📚 Arquivos Modificados

- `app/routes/web.py`:
  - `index()` - Página inicial
  - `dashboard()` - Dashboard
  - `offers()` - Listagem de ofertas

- `app/routes/api.py`:
  - `list_offers()` - API de listagem

---

**Data de Implementação**: 04/12/2025  
**Versão**: 1.0

