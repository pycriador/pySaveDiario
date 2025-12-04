# 📊 Inventário Completo de APIs

**Data:** 3 de Dezembro, 2025

---

## 🎯 Entidades do Sistema

### 1. **Users** (Usuários)
### 2. **Groups** (Grupos)
### 3. **Products** (Produtos)
### 4. **Offers** (Ofertas)
### 5. **Templates** (Templates de Compartilhamento)
### 6. **Sellers** (Vendedores)
### 7. **Categories** (Categorias)
### 8. **Manufacturers** (Fabricantes)
### 9. **Coupons** (Cupons)
### 10. **Namespaces** (Variáveis de Template)
### 11. **Publications** (Publicações)
### 12. **Wishlists** (Listas de Desejos)

---

## ✅ APIs JÁ IMPLEMENTADAS

### Sellers
- ✅ GET /api/sellers - List all
- ✅ POST /api/sellers - Create
- ✅ GET /api/sellers/{id} - Get one
- ✅ PUT /api/sellers/{id} - Update
- ✅ DELETE /api/sellers/{id} - Delete

### Categories
- ✅ GET /api/categories - List all
- ✅ POST /api/categories - Create
- ✅ GET /api/categories/{id} - Get one
- ✅ PUT /api/categories/{id} - Update
- ✅ DELETE /api/categories/{id} - Delete

### Manufacturers
- ✅ GET /api/manufacturers - List all
- ✅ POST /api/manufacturers - Create
- ✅ GET /api/manufacturers/{id} - Get one
- ✅ PUT /api/manufacturers/{id} - Update
- ✅ DELETE /api/manufacturers/{id} - Delete

### Auth
- ✅ POST /api/auth/token - Get API token
- ✅ POST /api/auth/refresh - Refresh token

---

## ❌ APIs FALTANDO

### Users
- ❌ GET /api/users - List all users
- ❌ POST /api/users - Create user
- ❌ GET /api/users/{id} - Get user
- ❌ PUT /api/users/{id} - Update user
- ❌ DELETE /api/users/{id} - Delete user
- ❌ PATCH /api/users/{id}/role - Change user role

### Groups
- ❌ GET /api/groups - List all groups
- ❌ POST /api/groups - Create group
- ❌ GET /api/groups/{id} - Get group
- ❌ PUT /api/groups/{id} - Update group
- ❌ DELETE /api/groups/{id} - Delete group
- ❌ POST /api/groups/{id}/members - Add member
- ❌ DELETE /api/groups/{id}/members/{user_id} - Remove member

### Products
- ❌ GET /api/products - List all products
- ❌ POST /api/products - Create product
- ❌ GET /api/products/{id} - Get product
- ❌ GET /api/products/slug/{slug} - Get by slug
- ❌ PUT /api/products/{id} - Update product
- ❌ DELETE /api/products/{id} - Delete product

### Offers
- ❌ GET /api/offers - List all offers
- ❌ POST /api/offers - Create offer
- ❌ GET /api/offers/{id} - Get offer
- ❌ PUT /api/offers/{id} - Update offer
- ❌ DELETE /api/offers/{id} - Delete offer
- ❌ GET /api/offers/active - List active offers
- ❌ GET /api/offers/expired - List expired offers

### Templates
- ❌ GET /api/templates - List all templates
- ❌ POST /api/templates - Create template
- ❌ GET /api/templates/{id} - Get template
- ❌ PUT /api/templates/{id} - Update template
- ❌ DELETE /api/templates/{id} - Delete template

### Coupons
- ❌ GET /api/coupons - List all coupons
- ❌ POST /api/coupons - Create coupon
- ❌ GET /api/coupons/{id} - Get coupon
- ❌ PUT /api/coupons/{id} - Update coupon
- ❌ DELETE /api/coupons/{id} - Delete coupon
- ❌ PATCH /api/coupons/{id}/toggle - Toggle active status

### Namespaces
- ❌ GET /api/namespaces - List all namespaces
- ❌ POST /api/namespaces - Create namespace
- ❌ GET /api/namespaces/{id} - Get namespace
- ❌ PUT /api/namespaces/{id} - Update namespace
- ❌ DELETE /api/namespaces/{id} - Delete namespace

### Publications
- ❌ GET /api/publications - List all publications
- ❌ POST /api/publications - Create publication
- ❌ GET /api/publications/{id} - Get publication
- ❌ DELETE /api/publications/{id} - Delete publication

### Wishlists
- ❌ GET /api/wishlists - List all wishlists
- ❌ POST /api/wishlists - Create wishlist
- ❌ GET /api/wishlists/{id} - Get wishlist
- ❌ PUT /api/wishlists/{id} - Update wishlist
- ❌ DELETE /api/wishlists/{id} - Delete wishlist
- ❌ POST /api/wishlists/{id}/items - Add item
- ❌ DELETE /api/wishlists/{id}/items/{product_id} - Remove item

---

## 📊 Total de Rotas

| Status | Quantidade |
|--------|------------|
| ✅ Implementadas | 17 rotas |
| ❌ Faltando | **58 rotas** |
| **TOTAL** | **75 rotas** |

---

## 🎯 Prioridade de Implementação

### Prioridade Alta (Essenciais)
1. **Products API** - Base para ofertas
2. **Offers API** - Funcionalidade principal
3. **Templates API** - Compartilhamento social
4. **Coupons API** - Novo recurso

### Prioridade Média
5. **Users API** - Gerenciamento de usuários
6. **Groups API** - Organização
7. **Namespaces API** - Variáveis de template

### Prioridade Baixa
8. **Publications API** - Histórico
9. **Wishlists API** - Feature secundária

---

## 📝 Formato Padrão das Respostas

### Success Response
```json
{
  "id": 1,
  "name": "Item Name",
  "created_at": "2025-12-03T10:00:00",
  "updated_at": "2025-12-03T10:00:00"
}
```

### Error Response
```json
{
  "error": "Descrição do erro",
  "code": "ERROR_CODE",
  "details": {}
}
```

### List Response
```json
{
  "data": [...],
  "count": 10,
  "page": 1,
  "per_page": 20,
  "total_pages": 1
}
```

---

## 🔐 Autenticação

Todas as rotas (exceto `/api/auth/token`) requerem:

```
Authorization: Bearer <token>
```

---

## 📦 Próximos Passos

1. ✅ Completar sistema de cupons (FEITO)
2. ⏳ Implementar APIs de Products
3. ⏳ Implementar APIs de Offers  
4. ⏳ Implementar APIs de Templates
5. ⏳ Implementar APIs de Coupons
6. ⏳ Implementar APIs de Users
7. ⏳ Implementar APIs de Groups
8. ⏳ Implementar APIs de Namespaces
9. ⏳ Atualizar documentação interativa
10. ⏳ Criar README completo

---

**Última atualização:** 3 de Dezembro, 2025

