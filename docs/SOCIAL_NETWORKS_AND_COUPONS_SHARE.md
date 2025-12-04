# 🎯 Configuração de Redes Sociais e Integração de Cupons

**Data:** 3 de Dezembro, 2025  
**Versão:** 3.6.0

---

## 📋 Visão Geral

Esta atualização adiciona duas funcionalidades importantes:

1. **Configuração de Redes Sociais**: Permite definir textos iniciais e finais (hashtags) específicos para cada rede social
2. **Integração de Cupons**: Permite selecionar cupons ativos ao compartilhar ofertas, mesclando-os automaticamente no texto

---

## 🆕 Funcionalidades Implementadas

### 1. Configuração de Redes Sociais

#### Nova Tabela de Banco de Dados
```python
class SocialNetworkConfig(db.Model):
    id = Integer (PK)
    network = String(50) UNIQUE  # instagram, facebook, whatsapp, telegram
    prefix_text = Text           # Texto antes do template
    suffix_text = Text           # Texto depois do template (hashtags)
    active = Boolean             # Ativar/desativar rede
```

#### Interface de Administração
**Rota:** `/admin/social-networks`

**Acesso:** Menu Administração → Redes Sociais

**Funcionalidades:**
- ✅ Configurar texto inicial (prefixo) para cada rede
- ✅ Configurar texto final / hashtags (sufixo) para cada rede
- ✅ Ativar/desativar redes sociais
- ✅ Interface visual com ícones específicos de cada rede

**Exemplo de uso:**

**Instagram:**
- Prefixo: *(vazio)*
- Sufixo: `#ofertas #descontos #promoção`

**Facebook:**
- Prefixo: `🔥 OFERTA IMPERDÍVEL!\n\n`
- Sufixo: `\n\n👍 Curta nossa página para não perder promoções!`

**WhatsApp:**
- Prefixo: `💰 *PROMOÇÃO*\n\n`
- Sufixo: `\n\n_Compartilhe com quem precisa!_`

**Telegram:**
- Prefixo: `📢 NOVA OFERTA!\n\n`
- Sufixo: `\n\n🔔 Ative as notificações do canal!`

#### Como o Texto é Montado
```
[PREFIXO DA REDE]
[CONTEÚDO DO TEMPLATE]
[SUFIXO DA REDE]
```

**Exemplo Final (Instagram):**
```
Notebook Dell Inspiron por apenas R$ 2.499!

Aproveite essa oferta incrível no Mercado Livre:
https://...

#ofertas #descontos #promoção
```

---

### 2. Seleção de Cupons ao Compartilhar

#### Nova Seção no Modal de Compartilhamento
Ao clicar em um botão de compartilhamento (Instagram, Facebook, etc.) em uma oferta, agora aparece:

**Cupons Ativos (Opcional):**
- [ ] PRIMEIRACOMPRA - Mercado Livre
- [ ] FRETE10 - Shopee
- [ ] BLACK50 - Magazine Luiza

**Como funciona:**
1. Usuário clica no botão de rede social (ex: Instagram)
2. Abre o modal com a lista de templates
3. **NOVO:** Aparece a seção de cupons ativos disponíveis
4. Usuário marca os cupons que quer incluir
5. Usuário seleciona o template
6. Sistema gera o texto com os cupons no final

**Exemplo de texto gerado COM cupons:**
```
Notebook Dell Inspiron por apenas R$ 2.499!

Aproveite essa oferta incrível no Mercado Livre:
https://...

🎟️ CUPONS DISPONÍVEIS:
• PRIMEIRACOMPRA - Mercado Livre
• FRETE10 - Mercado Livre

#ofertas #descontos #promoção
```

---

## 🗂️ Arquivos Criados/Modificados

### Criados

1. **`migrations/versions/f8c2a9b4e5d7_add_social_network_configs_table.py`**
   - Migration para criar tabela `social_network_configs`

2. **`scripts/init_social_networks.py`**
   - Script para popular configurações iniciais das 4 redes sociais

3. **`app/templates/admin/social_networks.html`**
   - Interface de administração das configurações de redes sociais

4. **`docs/SOCIAL_NETWORKS_AND_COUPONS_SHARE.md`**
   - Esta documentação

### Modificados

1. **`app/models.py`**
   - Adicionado `SocialNetworkConfig` model

2. **`app/forms.py`**
   - Adicionado `SocialNetworkConfigForm`

3. **`app/routes/web.py`**
   - Importado `SocialNetworkConfig`
   - Adicionada rota `admin_social_networks()`
   - Modificada rota `offers()` para passar `active_coupons`

4. **`app/templates/base.html`**
   - Adicionado link "Redes Sociais" no menu Administração

5. **`app/templates/offers_list.html`**
   - Adicionada seção de seleção de cupons no modal `shareOfferModal`
   - Atualizada função `selectOfferTemplate()` para incluir cupons selecionados

---

## 🚀 Como Usar

### Passo 1: Aplicar Migration

```bash
cd /Users/willian.jesus/Downloads/pySaveDiario
python3 -m flask db upgrade
```

### Passo 2: Inicializar Configurações

```bash
python3 scripts/init_social_networks.py
```

**Saída esperada:**
```
✓ Created config for instagram
✓ Created config for facebook
✓ Created config for whatsapp
✓ Created config for telegram

✅ Social network configurations initialized successfully!
```

### Passo 3: Personalizar Configurações

1. Acesse: `http://localhost:5000/admin/social-networks`
2. Personalize os textos de cada rede social
3. Clique em "Salvar" em cada card

### Passo 4: Usar ao Compartilhar

1. Vá para `/ofertas`
2. Clique em um botão de rede social de uma oferta
3. Marque os cupons que deseja incluir (opcional)
4. Selecione um template
5. O texto será gerado com:
   - Prefixo da rede
   - Conteúdo do template
   - Cupons selecionados (se houver)
   - Sufixo da rede (hashtags)

---

## 🎨 Fluxo Visual

### Antes (Sem cupons, sem configuração de rede)
```
[Botão Instagram] → [Modal Templates] → [Texto simples]
```

### Depois (Com cupons e configuração)
```
[Botão Instagram] 
    ↓
[Modal com seleção de cupons + templates]
    ↓
[Texto = Prefixo + Template + Cupons + Sufixo]
```

---

## 📊 Estrutura de Dados

### Configuração de Rede Social
```json
{
  "id": 1,
  "network": "instagram",
  "prefix_text": "",
  "suffix_text": "#ofertas #descontos #promoção",
  "active": true
}
```

### Cupons Ativos (filtrados)
```python
# Query que busca apenas cupons ativos e não expirados
active_coupons = Coupon.query.filter_by(active=True).filter(
    db.or_(
        Coupon.expires_at.is_(None),
        Coupon.expires_at > datetime.utcnow()
    )
).order_by(Coupon.code).all()
```

---

## 🔍 Lógica JavaScript

### Coleta de Cupons Selecionados
```javascript
const selectedCoupons = [];
const couponCheckboxes = document.querySelectorAll('.coupon-checkbox:checked');
couponCheckboxes.forEach(checkbox => {
  selectedCoupons.push({
    code: checkbox.getAttribute('data-coupon-code'),
    seller: checkbox.getAttribute('data-coupon-seller')
  });
});
```

### Adição ao Texto
```javascript
if (selectedCoupons.length > 0) {
  text += '\n\n🎟️ CUPONS DISPONÍVEIS:\n';
  selectedCoupons.forEach(coupon => {
    text += `• ${coupon.code} - ${coupon.seller}\n`;
  });
}
```

---

## ⚙️ Configurações Padrão

Após executar `init_social_networks.py`:

| Rede      | Prefixo                         | Sufixo                                              |
|-----------|---------------------------------|-----------------------------------------------------|
| Instagram | *(vazio)*                       | `#ofertas #descontos #promoção`                     |
| Facebook  | `🔥 OFERTA IMPERDÍVEL!\n\n`     | `\n\n👍 Curta nossa página para não perder promoções!` |
| WhatsApp  | `💰 *PROMOÇÃO*\n\n`             | `\n\n_Compartilhe com quem precisa!_`               |
| Telegram  | `📢 NOVA OFERTA!\n\n`            | `\n\n🔔 Ative as notificações do canal!`             |

---

## 🧪 Testes

### Teste 1: Configuração de Redes Sociais
```
1. Acesse /admin/social-networks
2. Verifique que 4 redes aparecem (Instagram, Facebook, WhatsApp, Telegram)
3. Edite o sufixo do Instagram
4. Clique em "Salvar"
5. Verifique mensagem de sucesso ✅
6. Recarregue a página
7. Confirme que a mudança foi salva ✅
```

### Teste 2: Seleção de Cupons
```
1. Cadastre 2 cupons ativos em /cupons/novo
2. Acesse /ofertas
3. Clique no botão Instagram de uma oferta
4. Verifique que os 2 cupons aparecem no modal ✅
5. Marque 1 cupom
6. Selecione um template
7. Verifique que o cupom aparece no texto final ✅
8. Copie o texto
9. Confirme formatação: "🎟️ CUPONS DISPONÍVEIS:" ✅
```

### Teste 3: Integração Completa
```
1. Configure hashtags personalizadas para Instagram
2. Cadastre um cupom ativo
3. Crie uma oferta
4. Compartilhe no Instagram selecionando o cupom
5. Verifique texto final:
   - Template original ✅
   - Cupom incluído ✅
   - Hashtags no final ✅
```

---

## 🎯 Benefícios

### Para Administradores
✅ **Controle centralizado** de textos de redes sociais  
✅ **Personalização** específica por plataforma  
✅ **Fácil atualização** de hashtags sazonais  

### Para Usuários
✅ **Processo mais rápido** de compartilhamento  
✅ **Inclusão automática** de cupons relevantes  
✅ **Textos padronizados** e profissionais  

### Para o Negócio
✅ **Consistência** de marca nas redes sociais  
✅ **Maior engajamento** com hashtags otimizadas  
✅ **Cross-selling** de cupons em ofertas  

---

## 📝 Próximos Passos Sugeridos

### Melhorias Futuras
1. **Variáveis nas configurações de rede**: Permitir usar `{product_name}` nos prefixos/sufixos
2. **Filtro de cupons por vendedor**: Mostrar apenas cupons do mesmo vendedor da oferta
3. **Preview em tempo real**: Mostrar como o texto ficará antes de selecionar o template
4. **Histórico de compartilhamentos**: Rastrear quais cupons/ofertas foram mais compartilhados
5. **Importar/Exportar configurações**: Backup das configurações de redes sociais

---

## ✅ Checklist de Implementação

- [x] Criar model `SocialNetworkConfig`
- [x] Criar migration
- [x] Criar script de inicialização
- [x] Criar formulário `SocialNetworkConfigForm`
- [x] Criar rota `admin_social_networks`
- [x] Criar template `admin/social_networks.html`
- [x] Adicionar link no menu
- [x] Modificar rota `offers` para buscar cupons ativos
- [x] Adicionar seção de cupons no modal `shareOfferModal`
- [x] Atualizar JavaScript `selectOfferTemplate()`
- [ ] Aplicar migration no servidor de produção
- [ ] Executar script de inicialização
- [ ] Testar todas as funcionalidades
- [ ] Documentar para usuários finais

---

## 🎊 Status

**✅ IMPLEMENTAÇÃO COMPLETA!**

Funcionalidades prontas:
- Configuração de redes sociais ✓
- Seleção de cupons ao compartilhar ✓
- Interface de administração ✓
- Documentação completa ✓

**Próximo:** Aplicar migration e testar!

---

**Desenvolvido com ❤️ para otimizar o compartilhamento de ofertas!**

