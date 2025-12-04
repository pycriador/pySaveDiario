# 👤 Cadastro Completo de Usuários

## 📋 Visão Geral

O sistema permite o cadastro completo de usuários com informações de contato e perfis de redes sociais. Esses dados podem ser usados em templates através de **namespaces globais**, permitindo personalização avançada das mensagens de ofertas e cupons.

---

## 🆕 Campos Adicionados ao Modelo User

### Informações de Contato
- **`phone`** (VARCHAR 20): Telefone/celular do usuário
- **`address`** (VARCHAR 255): Endereço completo
- **`website`** (VARCHAR 255): Website ou blog pessoal

### Redes Sociais
- **`instagram`** (VARCHAR 255): Perfil do Instagram (@usuario ou URL)
- **`facebook`** (VARCHAR 255): Perfil do Facebook (URL)
- **`twitter`** (VARCHAR 255): Perfil do Twitter/X (@usuario ou URL)
- **`linkedin`** (VARCHAR 255): Perfil do LinkedIn (URL)
- **`youtube`** (VARCHAR 255): Canal do YouTube (URL)
- **`tiktok`** (VARCHAR 255): Perfil do TikTok (@usuario ou URL)

---

## 🖥️ Interface Web

### Formulário de Cadastro (`/usuarios`)

O formulário de criação de usuários foi expandido com:

#### Seção: Informações de Contato
```
📞 Celular: (11) 98765-4321
🌐 Website: https://seusite.com.br
📍 Endereço: Rua, número, bairro, cidade - UF
```

#### Seção: Redes Sociais
```
📷 Instagram: @usuario ou URL completa
📘 Facebook: @usuario ou URL completa
🐦 Twitter/X: @usuario ou URL completa
💼 LinkedIn: URL do perfil
🎥 YouTube: URL do canal
🎵 TikTok: @usuario ou URL completa
```

### Exibição na Listagem

Os cards de usuários exibem:
- ✅ Telefone (se cadastrado)
- ✅ Website com link clicável (se cadastrado)
- ✅ Status (Ativo/Inativo)
- ✅ Botões de acesso rápido às redes sociais (ícones clicáveis)

---

## 🔌 API REST

### Registro de Usuário

**Endpoint:** `POST /api/users`

**Campos Obrigatórios:**
- `email` (string)
- `password` (string)
- `display_name` (string)

**Campos Opcionais:**
- `role` (string): "member", "editor", "admin"
- `phone` (string)
- `address` (string)
- `website` (string)
- `instagram` (string)
- `facebook` (string)
- `twitter` (string)
- `linkedin` (string)
- `youtube` (string)
- `tiktok` (string)

**Exemplo de Request:**
```json
{
  "email": "usuario@email.com",
  "password": "senha123",
  "display_name": "Nome Completo",
  "role": "member",
  "phone": "(11) 98765-4321",
  "address": "Rua Exemplo, 123 - São Paulo, SP",
  "website": "https://meusite.com.br",
  "instagram": "@meuinstagram",
  "facebook": "https://facebook.com/meuperfil",
  "twitter": "@meutwitter",
  "linkedin": "https://linkedin.com/in/meuperfil",
  "youtube": "https://youtube.com/@meucanal",
  "tiktok": "@meutiktok"
}
```

**Resposta (200 Created):**
```json
{
  "id": 1,
  "email": "usuario@email.com",
  "display_name": "Nome Completo",
  "role": "member",
  "bio": null,
  "avatar_url": null,
  "phone": "(11) 98765-4321",
  "address": "Rua Exemplo, 123 - São Paulo, SP",
  "website": "https://meusite.com.br",
  "instagram": "@meuinstagram",
  "facebook": "https://facebook.com/meuperfil",
  "twitter": "@meutwitter",
  "linkedin": "https://linkedin.com/in/meuperfil",
  "youtube": "https://youtube.com/@meucanal",
  "tiktok": "@meutiktok",
  "created_at": "2025-12-04T10:30:00Z"
}
```

---

### Atualização de Perfil

**Endpoint:** `PUT /api/users/<id>` ou `PATCH /api/users/<id>`

**Permissões:**
- ✅ Usuário pode atualizar seu **próprio** perfil
- ✅ Admin pode atualizar **qualquer** perfil
- ⚠️ Apenas admins podem alterar `role`

**Exemplo de Request:**
```json
{
  "phone": "(11) 91234-5678",
  "website": "https://novosite.com.br",
  "instagram": "@novoinstagram"
}
```

**Resposta (200 OK):**
```json
{
  "id": 1,
  "email": "usuario@email.com",
  "display_name": "Nome Completo",
  "role": "member",
  "phone": "(11) 91234-5678",
  "website": "https://novosite.com.br",
  "instagram": "@novoinstagram",
  ...
}
```

---

## 🎨 Namespaces Globais

As informações do usuário podem ser inseridas em templates através de namespaces:

### Contato

| Namespace | Alias | Exemplo |
|-----------|-------|---------|
| `{user_phone}` | `{telefone}`, `{celular}` | (11) 98765-4321 |
| `{user_address}` | `{endereco}` | Rua Exemplo, 123 - SP |
| `{user_website}` | `{site}` | https://meusite.com.br |

### Redes Sociais

| Namespace | Alias | Exemplo |
|-----------|-------|---------|
| `{user_instagram}` | `{instagram}` | @meuinstagram |
| `{user_facebook}` | `{facebook}` | facebook.com/meuperfil |
| `{user_twitter}` | `{twitter}` | @meutwitter |
| `{user_linkedin}` | `{linkedin}` | linkedin.com/in/meuperfil |
| `{user_youtube}` | `{youtube}` | youtube.com/@meucanal |
| `{user_tiktok}` | `{tiktok}` | @meutiktok |

---

## 📝 Exemplos de Uso em Templates

### Exemplo 1: Template de Oferta com Contato

**Template:**
```
🔥 OFERTA ESPECIAL!

{product_name}
💰 R$ {price}

📞 Dúvidas? Chame no {celular}
🌐 Mais informações: {site}
```

**Resultado:**
```
🔥 OFERTA ESPECIAL!

Controle PS5 DualSense
💰 R$ 399,00

📞 Dúvidas? Chame no (11) 98765-4321
🌐 Mais informações: https://meusite.com.br
```

---

### Exemplo 2: Template com Redes Sociais

**Template:**
```
{product_name}
De: R$ {old_price}
Por: R$ {price}

📱 Siga nas redes sociais:
Instagram: {instagram}
TikTok: {tiktok}
YouTube: {youtube}
```

**Resultado:**
```
Controle PS5 DualSense
De: R$ 499,00
Por: R$ 399,00

📱 Siga nas redes sociais:
Instagram: @meuinstagram
TikTok: @meutiktok
YouTube: youtube.com/@meucanal
```

---

### Exemplo 3: Assinatura de Mensagens

**Template:**
```
{product_name} - {price}

Use o cupom: {coupon_code}

━━━━━━━━━━━━━━━━━━
📍 {endereco}
📞 {celular}
🌐 {site}
📷 {instagram}
```

**Resultado:**
```
Controle PS5 DualSense - R$ 399,00

Use o cupom: DESC10

━━━━━━━━━━━━━━━━━━
📍 Rua Exemplo, 123 - São Paulo, SP
📞 (11) 98765-4321
🌐 https://meusite.com.br
📷 @meuinstagram
```

---

## 🗄️ Migração do Banco de Dados

### Script: `scripts/add_user_contact_fields.py`

Este script adiciona as 9 novas colunas à tabela `users`:

```bash
python scripts/add_user_contact_fields.py
```

**Colunas Adicionadas:**
1. `phone` (VARCHAR 20)
2. `address` (VARCHAR 255)
3. `website` (VARCHAR 255)
4. `instagram` (VARCHAR 255)
5. `facebook` (VARCHAR 255)
6. `twitter` (VARCHAR 255)
7. `linkedin` (VARCHAR 255)
8. `youtube` (VARCHAR 255)
9. `tiktok` (VARCHAR 255)

---

## 🔧 Namespaces Criados

### Script: `scripts/add_user_global_namespaces.py`

Este script adiciona 19 namespaces globais ao banco:

```bash
python scripts/add_user_global_namespaces.py
```

**Namespaces Principais:**
- `user_phone`, `telefone`, `celular`
- `user_address`, `endereco`
- `user_website`, `site`
- `user_instagram`, `instagram`
- `user_facebook`, `facebook`
- `user_twitter`, `twitter`
- `user_linkedin`, `linkedin`
- `user_youtube`, `youtube`
- `user_tiktok`, `tiktok`

---

## 🎯 Casos de Uso

### 1. Divulgador de Ofertas
Um divulgador pode cadastrar seu WhatsApp, Instagram e site no perfil. Ao criar templates de ofertas, essas informações aparecem automaticamente em todas as mensagens, facilitando o contato e aumentando o engajamento.

### 2. Loja Física
Uma loja pode cadastrar seu endereço e telefone. Templates de cupons podem incluir automaticamente essas informações, incentivando visitas à loja física.

### 3. Influenciador Digital
Um influenciador pode cadastrar todos os seus perfis sociais. Templates podem incluir chamadas para seguir em múltiplas plataformas, aumentando o alcance.

### 4. Afiliado Profissional
Um afiliado pode ter website próprio para reviews. Templates podem direcionar tráfego para seu site, além das ofertas.

---

## ✅ Vantagens

1. **Centralização**: Todas as informações de contato em um só lugar
2. **Automação**: Namespaces preenchem automaticamente os dados
3. **Consistência**: Mesmas informações em todos os templates
4. **Flexibilidade**: Aliases permitem usar nomes mais curtos e intuitivos
5. **Escalabilidade**: Fácil adicionar novos campos no futuro
6. **API Completa**: Gerenciamento via API REST para integrações
7. **Segurança**: Controle de permissões (próprio perfil vs. admin)

---

## 🔒 Segurança e Privacidade

- ✅ Todos os campos de contato são **opcionais**
- ✅ Usuário controla quais informações deseja preencher
- ✅ Apenas o próprio usuário e admins podem ver/editar perfis completos
- ✅ Senhas são hash criptografadas (nunca retornadas na API)
- ✅ Validação de e-mail único para evitar duplicatas

---

## 📚 Documentação Relacionada

- [README.md](../README.md) - Documentação principal
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Referência rápida
- [API Documentation](http://localhost:5000/api-docs) - Documentação interativa da API
- [COUPON_NAMESPACES_GUIDE.md](COUPON_NAMESPACES_GUIDE.md) - Guia de namespaces de cupons

---

**Última Atualização:** 04/12/2025  
**Versão:** 1.0  
**Status:** ✅ Completo e Funcional

