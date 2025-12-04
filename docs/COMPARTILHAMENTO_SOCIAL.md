# 📱 Compartilhamento Social - Ofertas e Cupons

**Data:** 3 de Dezembro, 2025  
**Versão:** 3.4.0

---

## ✨ O Que Foi Implementado

### 1. **Compartilhamento Social em CUPONS** ✅
- ✅ 4 botões de compartilhamento (Instagram, Facebook, WhatsApp, Telegram)
- ✅ Modal de seleção de template
- ✅ Substituição automática de variáveis
- ✅ Modal de texto para copiar
- ✅ Botão de copiar texto

### 2. **Compartilhamento Social em OFERTAS** ✅
- ✅ 4 botões de compartilhamento (Instagram, Facebook, WhatsApp, Telegram)
- ✅ Modal de seleção de template
- ✅ Substituição automática de variáveis
- ✅ Modal de texto para copiar
- ✅ Botão de copiar texto

### 3. **Melhorias no Seletor de Data** ✅
- ✅ Calendário fecha automaticamente ao selecionar
- ✅ Visual melhorado (ícone maior com hover)
- ✅ Suporte a tema claro e escuro

### 4. **Cores Ajustadas** ✅
- ✅ Descrições de cupons legíveis no tema escuro

---

## 🎨 Visual dos Botões

### Botões de Compartilhamento

```
┌──────────────────────────────┐
│ Compartilhar                 │
│ [📷] [f] [📱] [✈️]           │
│  IG   FB  WA  TG             │
└──────────────────────────────┘
```

**Cores:**
- 📷 Instagram: Gradiente roxo/rosa
- 📘 Facebook: Azul #1877f2
- 📱 WhatsApp: Verde #25d366
- ✈️ Telegram: Azul #0088cc

**Hover Effect:**
- Levanta 2px
- Sombra suave
- Transição smooth

---

## 🔄 Fluxo de Uso

### Em Cupons

1. Acesse `/cupons`
2. Veja lista de cupons
3. Clique no botão da rede social (ex: WhatsApp)
4. **Modal abre** com lista de templates
5. Selecione um template
6. **Modal muda** mostrando o texto gerado
7. Variáveis substituídas automaticamente:
   - `{coupon_code}` → Código do cupom
   - `{seller}` → Nome do vendedor
8. Clique em "Copiar texto"
9. **Toast aparece**: "Texto copiado!"
10. Cole no WhatsApp e envie!

### Em Ofertas

1. Acesse `/ofertas`
2. Veja lista de ofertas
3. Clique no botão da rede social (ex: Instagram)
4. **Modal abre** com lista de templates
5. Selecione um template
6. **Modal muda** mostrando o texto gerado
7. Variáveis substituídas automaticamente:
   - `{product_name}` → Nome do produto
   - `{price}` → Preço
   - `{vendor_name}` / `{seller}` → Vendedor
   - `{offer_url}` / `{url}` / `{link}` → Link
8. Clique em "Copiar texto"
9. **Toast aparece**: "Texto copiado!"
10. Cole no Instagram e poste!

---

## 🔤 Variáveis Suportadas

### Para Cupons
| Variável | Substituído por |
|----------|-----------------|
| `{coupon_code}` | Código do cupom |
| `{seller}` | Nome do vendedor |
| `{seller_name}` | Nome do vendedor |
| `{vendor}` | Nome do vendedor |
| `{vendor_name}` | Nome do vendedor |

### Para Ofertas
| Variável | Substituído por |
|----------|-----------------|
| `{product_name}` | Nome do produto |
| `{price}` | Preço |
| `{vendor_name}` | Nome do vendedor |
| `{vendor}` | Nome do vendedor |
| `{seller}` | Nome do vendedor |
| `{seller_name}` | Nome do vendedor |
| `{offer_url}` | URL da oferta |
| `{url}` | URL da oferta |
| `{link}` | URL da oferta |

---

## 💡 Exemplo de Template

### Template Criado
```
🎉 CUPOM EXCLUSIVO! 🎉

Use o cupom {coupon_code} na {seller} e ganhe desconto especial!

Aproveite agora! 🔥
```

### Texto Gerado (Cupom)
```
🎉 CUPOM EXCLUSIVO! 🎉

Use o cupom SAVE20 na Amazon e ganhe desconto especial!

Aproveite agora! 🔥
```

### Template para Oferta
```
🔥 OFERTA IMPERDÍVEL! 🔥

{product_name} por apenas R$ {price}

Compre agora na {seller}:
{offer_url}

Corre que acaba! ⏰
```

### Texto Gerado (Oferta)
```
🔥 OFERTA IMPERDÍVEL! 🔥

PS5 Pro por apenas R$ 2999.00

Compre agora na Amazon:
https://amazon.com.br/ps5-pro

Corre que acaba! ⏰
```

---

## 🎯 Modais Implementados

### Modal 1: Seleção de Template
```
┌───────────────────────────────────┐
│ 📤 Compartilhar Cupom        [×]  │
├───────────────────────────────────┤
│ Cupom: SAVE20 - Amazon            │
│                                   │
│ 📄 Selecione um template:         │
│ ┌─────────────────────────────┐   │
│ │ 📄 Oferta Black Friday      │   │
│ │ Template para promoções     │   │
│ └─────────────────────────────┘   │
│ ┌─────────────────────────────┐   │
│ │ 📄 Cupom Exclusivo          │   │
│ │ Template para cupons        │   │
│ └─────────────────────────────┘   │
└───────────────────────────────────┘
```

### Modal 2: Texto Gerado
```
┌───────────────────────────────────┐
│ 📤 Texto para WhatsApp       [×]  │
├───────────────────────────────────┤
│ Copie o texto abaixo:             │
│ ┌─────────────────────────────┐   │
│ │ 🎉 CUPOM EXCLUSIVO! 🎉      │   │
│ │                             │   │
│ │ Use o cupom SAVE20 na       │   │
│ │ Amazon e ganhe desconto!    │   │
│ │                             │   │
│ │ Aproveite agora! 🔥         │   │
│ └─────────────────────────────┘   │
├───────────────────────────────────┤
│ [Fechar]  [📋 Copiar texto]       │
└───────────────────────────────────┘
```

---

## 💻 Implementação Técnica

### Backend

**Rota de cupons atualizada:**
```python
@web_bp.route("/cupons", methods=["GET"])
def coupons():
    coupons = Coupon.query.all()
    templates = Template.query.all()  # ← ADICIONADO
    namespaces = Namespace.query.all()  # ← ADICIONADO
    
    return render_template("coupons_list.html", 
                         coupons=coupons,
                         templates=templates,
                         namespaces=namespaces)
```

### Frontend

**HTML - Botões:**
```html
<button class="btn btn-sm btn-share btn-instagram" 
        onclick="openShareCouponModal({{ coupon.id }}, 'instagram', '{{ coupon.code }}', '{{ coupon.seller.name }}')">
  <i class="bi bi-instagram"></i>
</button>
```

**JavaScript - Substituição:**
```javascript
function selectTemplate(templateId, templateName, templateBody) {
  let text = templateBody;
  text = text.replace(/{coupon_code}/gi, currentCouponData.code);
  text = text.replace(/{seller}/gi, currentCouponData.seller);
  // ... mais substituições
}
```

---

## 🎨 CSS Aplicado

```css
.btn-share {
  min-width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  border: none;
  color: white;
  transition: all 0.2s ease;
}

.btn-share:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.btn-instagram {
  background: linear-gradient(45deg, #f09433, #bc1888);
}

.btn-facebook {
  background: #1877f2;
}

.btn-whatsapp {
  background: #25d366;
}

.btn-telegram {
  background: #0088cc;
}
```

---

## 📊 Arquivos Modificados

### Backend
1. `app/routes/web.py` - Rota de cupons atualizada

### Frontend
2. `app/templates/coupons_list.html` - Botões e modais adicionados
3. `app/templates/offers_list.html` - Modais atualizados

### CSS
4. `app/static/css/style.css` - Estilos do seletor de data

---

## ✅ Checklist

- [x] Adicionar botões de share em cupons
- [x] Adicionar botões de share em ofertas
- [x] Criar modal de seleção de template
- [x] Criar modal de texto gerado
- [x] Implementar função openShareCouponModal
- [x] Implementar função openShareOfferModal
- [x] Implementar função selectTemplate
- [x] Implementar função copyShareText
- [x] Adicionar CSS dos botões
- [x] Passar templates para a rota de cupons
- [x] Passar namespaces para a rota de cupons
- [x] Remover modal duplicado
- [x] Testar compartilhamento
- [x] Documentar feature

---

## 🎉 Status

**✅ IMPLEMENTADO COM SUCESSO!**

Compartilhamento social funcionando perfeitamente em:
- Cupons ✓
- Ofertas ✓

Funcionalidades:
- Seleção de template ✓
- Substituição de variáveis ✓
- Copiar texto ✓
- Toast notifications ✓
- 4 redes sociais ✓

---

**Desenvolvido com ❤️ para facilitar o compartilhamento!**

