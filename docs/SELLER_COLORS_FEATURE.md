# Cores Personalizadas para Vendedores

## 📋 Visão Geral

Cada vendedor agora pode ter uma cor personalizada que será exibida em todos os templates do projeto, tornando a identificação visual muito mais intuitiva e profissional.

## 🎨 Funcionalidades

### 1. Colorpicker Completo

Ao cadastrar ou editar um vendedor, você tem 3 opções para escolher a cor:

#### **Cor Sólida**
- Colorpicker HTML5 nativo
- Input manual de código hexadecimal
- Preview em tempo real

#### **Gradientes Pré-definidos**
- Instagram (multi-color)
- Roxo
- Rosa
- Azul
- Verde
- Pôr do Sol

#### **CSS Customizado**
- Cole qualquer valor CSS válido
- Suporta gradientes lineares e radiais
- Possibilidade de efeitos avançados

### 2. Cores Padrão

Os seguintes vendedores já vêm com cores pré-configuradas:

| Vendedor | Cor |
|----------|-----|
| Mercado Livre | `#FFE600` (Amarelo) |
| Shopee | `#EE4D2D` (Laranja) |
| Amazon | `#FF9900` (Laranja Amazon) |
| Magazine Luiza | `#DC143C` (Vermelho) |
| AliExpress | `#E62129` (Vermelho) |
| Kabum | `#003DA5` (Azul) |
| Casas Bahia | `#0070C0` (Azul) |
| Extra | `#00A859` (Verde) |

### 3. Exibição nas Ofertas

A cor do vendedor é exibida automaticamente:
- ✅ Na listagem de ofertas (`/ofertas`)
- ✅ Nos cards de ofertas
- ✅ No badge do vendedor com fundo colorido e texto branco
- ✅ Ícone e texto sempre em branco para legibilidade

## 🔧 Implementação Técnica

### Banco de Dados

```sql
ALTER TABLE sellers ADD COLUMN color VARCHAR(255) DEFAULT '#6b7280';
```

### Modelo Python

```python
class Seller(TimestampMixin, db.Model):
    # ...campos existentes...
    color = db.Column(db.String(255), default='#6b7280')
```

### Template (Jinja2)

```html
<div class="vendor-badge" style="background: {{ offer.seller.color if offer.seller else '#6b7280' }};">
  <i class="bi bi-shop" style="color: white !important;"></i>
  <strong style="color: white !important;">{{ offer.vendor_name }}</strong>
</div>
```

## 📝 Scripts de Migração

### SQL
```bash
sqlite3 instance/database.db < scripts/add_color_to_sellers.sql
```

### Python
```bash
python scripts/add_color_to_sellers.py
```

## 🎯 Benefícios

1. **Identificação Visual Rápida**: Reconheça o vendedor instantaneamente pela cor
2. **Profissionalismo**: Interface mais moderna e organizada
3. **Flexibilidade**: Suporte a cores sólidas, gradientes e CSS personalizado
4. **Consistência**: Cor aplicada em todos os templates do projeto
5. **Acessibilidade**: Texto sempre em branco sobre fundo colorido para máxima legibilidade

## 🚀 Como Usar

### Criar Novo Vendedor com Cor

1. Acesse `/admin/sellers`
2. Clique em "Novo vendedor"
3. Preencha os dados básicos
4. Na seção "Cor do Vendedor":
   - Escolha uma cor sólida com o colorpicker
   - OU selecione um gradiente pré-definido
   - OU cole um CSS customizado
5. Veja a pré-visualização em tempo real
6. Salve o vendedor

### Atualizar Cor de Vendedor Existente

*Nota: Funcionalidade de edição será implementada em breve*

### API

```python
# Criar vendedor com cor via API
POST /api/sellers
{
    "name": "Novo Vendedor",
    "slug": "novo-vendedor",
    "color": "#FF5733",  # Cor em hexadecimal ou CSS
    "active": true
}
```

## 🔍 Exemplos de Cores

### Cores Sólidas
```css
#FFE600  /* Amarelo Mercado Livre */
#EE4D2D  /* Laranja Shopee */
#FF9900  /* Laranja Amazon */
```

### Gradientes
```css
/* Instagram */
linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%)

/* Pôr do Sol */
linear-gradient(135deg, #fa709a 0%, #fee140 100%)
```

## 📚 Referências

- Modelo: `app/models.py` → `Seller`
- Formulário: `app/forms.py` → `SellerForm`
- Template Admin: `app/templates/admin/sellers.html`
- Template Ofertas: `app/templates/offers_list.html`
- Script SQL: `scripts/add_color_to_sellers.sql`
- Script Python: `scripts/add_color_to_sellers.py`

---

**Data de Implementação**: 04/12/2025  
**Versão**: 1.0

