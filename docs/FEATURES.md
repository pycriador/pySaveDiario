# ✨ Funcionalidades Completas do pySaveDiário

## 📋 Índice

- [Gestão de Ofertas](#-gestão-de-ofertas)
- [Sistema de Cupons](#-sistema-de-cupons)
- [Templates e Compartilhamento](#-templates-e-compartilhamento)
- [Vendedores Personalizados](#-vendedores-personalizados)
- [Administração](#-administração)
- [Interface e UX](#-interface-e-ux)
- [API REST](#-api-rest)
- [Segurança](#-segurança)

---

## 🏷️ Gestão de Ofertas

### Funcionalidades Principais

1. **CRUD Completo**
   - ✅ Criar ofertas
   - ✅ Editar ofertas
   - ✅ Deletar ofertas
   - ✅ Listar ofertas

2. **Upload de Imagens** 🖼️
   - ✅ Upload seguro (7 camadas de validação)
   - ✅ Validação de extensão (.jpg, .png, .gif, .webp)
   - ✅ Validação de conteúdo com Pillow
   - ✅ Limite de tamanho (5MB)
   - ✅ Nome de arquivo seguro
   - ✅ Preview antes de salvar
   - ✅ Lazy loading nas listagens
   - ✅ Placeholder quando não há imagem

3. **Editor HTML** ✍️
   - ✅ Editor Quill.js WYSIWYG
   - ✅ Barra de ferramentas completa
   - ✅ Compatível com temas claro e escuro
   - ✅ Salvamento como texto puro
   - ✅ Conversão automática para redes sociais

4. **Sistema de Preços** 💰
   - ✅ Preço atual
   - ✅ Preço antigo (old_price)
   - ✅ **Cálculo automático de desconto**
   - ✅ Badge visual com percentual (-20%)
   - ✅ Multi-moedas (12 moedas disponíveis)
   - ✅ Símbolos de moeda (R$, $, €, £, etc.)

5. **Sistema de Parcelas** 💳
   - ✅ Quantidade de parcelas
   - ✅ Valor por parcela
   - ✅ Com/sem juros
   - ✅ Namespace automático: `{installment_full}`
   - ✅ Exemplo: "5x de R$ 72 sem juros"

6. **Filtros Dinâmicos** 🔍
   - ✅ Busca geral (nome, slug, vendedor)
   - ✅ Filtro por fabricante
   - ✅ Filtro por categoria
   - ✅ Filtro por vendedor
   - ✅ Faixa de preço (min/max)
   - ✅ Apenas ofertas ativas
   - ✅ Atualização em tempo real (500ms debounce)
   - ✅ URL compartilhável

7. **Compartilhamento Social** 📤
   - ✅ Página dedicada (`/ofertas/<id>/compartilhar`)
   - ✅ Seleção de rede social
   - ✅ Seleção de template
   - ✅ Seleção múltipla de cupons
   - ✅ Cálculo de preço com cupom
   - ✅ Geração automática de texto
   - ✅ Formatação específica por rede
   - ✅ Botão de copiar
   - ✅ Preview em tempo real

8. **Associações**
   - ✅ Vendedor (seller_id)
   - ✅ Categoria (category_id)
   - ✅ Fabricante (manufacturer_id)
   - ✅ Produto (product_id)
   - ✅ Data de expiração (expires_at)

---

## 🎫 Sistema de Cupons

### Funcionalidades Principais

1. **CRUD Completo**
   - ✅ Criar cupons
   - ✅ Editar cupons
   - ✅ Deletar cupons
   - ✅ Listar cupons
   - ✅ Ativar/desativar cupons

2. **Tipos de Desconto** 💸
   
   **Porcentagem (%)**
   - ✅ Desconto percentual (ex: 10%)
   - ✅ **Limite máximo** (ex: até R$ 50)
   - ✅ Cálculo automático respeitando limite
   
   **Valor Fixo (R$)**
   - ✅ Desconto em valor absoluto (ex: R$ 20)
   - ✅ Aplicado diretamente no preço

3. **Editor HTML** ✍️
   - ✅ Descrição rica com formatação
   - ✅ Conversão para texto puro

4. **Namespaces** 🔖
   - ✅ `{coupon_code}` - Código do cupom
   - ✅ `{all_coupons}` - Todos os cupons selecionados
   - ✅ `{price_with_coupon}` - Preço com desconto aplicado
   - ✅ Formato: `CUPONS: CUPOM1, CUPOM2, CUPOM3`

5. **Filtros Dinâmicos** 🔍
   - ✅ Busca por código do cupom
   - ✅ Filtro por vendedor
   - ✅ Filtro por tipo de desconto
   - ✅ Apenas cupons ativos (padrão)
   - ✅ Atualização em tempo real
   - ✅ URL compartilhável

6. **Integração**
   - ✅ Associação com vendedores
   - ✅ Data de expiração
   - ✅ Seleção múltipla em compartilhamento
   - ✅ Cálculo automático do melhor desconto
   - ✅ Compartilhamento em redes sociais

---

## 📝 Templates e Compartilhamento

### Funcionalidades Principais

1. **CRUD Completo**
   - ✅ Criar templates
   - ✅ Editar templates
   - ✅ Deletar templates
   - ✅ Listar templates

2. **Editor HTML** ✍️
   - ✅ Editor Quill.js rico
   - ✅ Compatível com temas
   - ✅ Salvamento como texto puro

3. **Variáveis Dinâmicas** (50+ Namespaces)

   **Produto/Oferta:**
   - `{product_name}` - Nome do produto
   - `{product_description}` - Descrição formatada
   - `{price}` - Preço com símbolo (R$ 100,00)
   - `{old_price}` - Preço antigo
   - `{discount}` - Desconto percentual (-20%)
   - `{vendor_name}` / `{seller}` - Vendedor
   - `{offer_url}` - Link
   - `{category}` - Categoria
   - `{manufacturer}` - Fabricante

   **Parcelas:**
   - `{installment_count}` - Quantidade (5)
   - `{installment_value}` - Valor (R$ 72,00)
   - `{installment_interest_free}` - Sim/Não
   - `{installment_full}` - "5x de R$ 72 sem juros"
   - `{parcelamento}` - Alias de installment_full

   **Cupons:**
   - `{coupon_code}` - Código do cupom
   - `{all_coupons}` - Todos selecionados
   - `{price_with_coupon}` - Preço com desconto

   **Globais:**
   - `{site_name}` - Nome do site
   - `{site_url}` - URL do site
   - E mais...

4. **Redes Sociais** 📱
   - ✅ Instagram
   - ✅ Facebook
   - ✅ WhatsApp
   - ✅ Telegram
   - ✅ Twitter/X
   - ✅ LinkedIn

5. **Configuração por Rede** ⚙️
   - ✅ Prefixo customizado
   - ✅ Sufixo customizado
   - ✅ **Colorpicker visual** (hex ou gradiente)
   - ✅ Ativar/desativar por rede
   - ✅ Preview em tempo real

6. **Formatação Automática** 🔄
   
   **WhatsApp:**
   ```
   *Negrito*
   _Itálico_
   ~Tachado~
   ```
   
   **Telegram:**
   ```
   **Negrito**
   __Itálico__
   ```
   
   **Instagram/Facebook:**
   ```
   Texto puro sem formatação
   ```

7. **Filtros** 🔍
   - ✅ Busca por nome, slug ou descrição
   - ✅ Filtro por rede social
   - ✅ Atualização dinâmica
   - ✅ URL compartilhável

---

## 🏪 Vendedores Personalizados

### Funcionalidades Principais

1. **CRUD Completo**
   - ✅ Criar vendedores
   - ✅ **Editar vendedores** (página dedicada)
   - ✅ Deletar vendedores
   - ✅ Listar vendedores
   - ✅ Ativar/desativar

2. **Cores Personalizadas** 🎨

   **Colorpicker com 3 Modos:**
   
   **Modo 1: Cor Sólida**
   - HTML5 colorpicker nativo
   - Input hexadecimal manual
   - Preview em tempo real
   
   **Modo 2: Gradientes Pré-definidos**
   - Instagram (multi-color)
   - Roxo
   - Rosa
   - Azul
   - Verde
   - Pôr do Sol
   
   **Modo 3: CSS Customizado**
   - Cole qualquer CSS
   - linear-gradient, radial-gradient
   - Efeitos avançados

3. **Cores Padrão** 🎨
   ```
   Mercado Livre: #FFE600 (Amarelo)
   Amazon: #FF9900 (Laranja)
   Shopee: #EE4D2D (Laranja avermelhado)
   Magazine Luiza: #DC143C (Vermelho)
   AliExpress: #E62129 (Vermelho)
   Kabum: #003DA5 (Azul)
   Casas Bahia: #0070C0 (Azul claro)
   Extra: #00A859 (Verde)
   ```

4. **Aplicação Automática**
   - ✅ Badge colorido nas ofertas
   - ✅ Texto sempre branco
   - ✅ Funciona em ambos os temas
   - ✅ Identificação visual instantânea

5. **Filtro de Inativos** 👁️
   - ✅ Vendedor inativo = ofertas ocultas
   - ✅ Aplicado em:
     - Página inicial
     - Dashboard
     - Listagem de ofertas
     - API REST
   - ✅ Reversível (ativar/desativar)

---

## ⚙️ Administração

### Menu Organizado

```
Administração ▼
  ├─ 📊 Painel
  ├─ ───────────
  ├─ 👥 Usuários
  ├─ 👨‍👩‍👧‍👦 Grupos
  ├─ ───────────
  ├─ 🏪 Vendedores
  ├─ 🏷️ Categorias
  ├─ 🏭 Fabricantes
  ├─ ───────────
  ├─ 📱 Redes Sociais
  └─ ⚙️ Configurações
```

### Vendedores

- ✅ CRUD completo
- ✅ **Colorpicker visual**
- ✅ Página de edição dedicada
- ✅ Ativar/desativar
- ✅ Slug único
- ✅ Website opcional
- ✅ Descrição

### Categorias

- ✅ CRUD completo
- ✅ Página de edição dedicada
- ✅ Ativar/desativar
- ✅ Ícone Bootstrap
- ✅ Slug único

### Fabricantes

- ✅ CRUD completo
- ✅ Página de edição dedicada
- ✅ Ativar/desativar
- ✅ Website opcional

### Redes Sociais

- ✅ Configurar prefixo/sufixo
- ✅ **Colorpicker para botões**
- ✅ Ativar/desativar
- ✅ Preview em tempo real
- ✅ Hashtags específicas por rede

### Configurações

- ✅ **Moeda padrão** do sistema
- ✅ Tabela com 12 moedas
- ✅ Símbolos exibidos
- ✅ Seleção visual

---

## 🎨 Interface e UX

### Design Moderno

1. **Tema Escuro Completo** 🌙
   - ✅ Toggle no header
   - ✅ Todas as páginas adaptadas
   - ✅ Cores otimizadas para legibilidade
   - ✅ CSS centralizado (theme.css)
   - ✅ Variáveis CSS dinâmicas

2. **Toast Notifications** 🔔
   - ✅ Estilo macOS
   - ✅ Posicionadas abaixo do menu
   - ✅ 5 segundos de duração
   - ✅ **Fadeout suave (sem piscadas)**
   - ✅ Tipos: Success, Error, Warning, Info
   - ✅ Ícones coloridos

3. **Componentes Visuais**
   - ✅ **Colorpicker** (3 modos)
   - ✅ **Editor HTML** (Quill.js)
   - ✅ **Seletor de data/hora** separados
   - ✅ Modals elegantes
   - ✅ Cards com hover effects
   - ✅ Gradientes modernos
   - ✅ Ícones Bootstrap em toda interface

4. **Responsividade** 📱
   - ✅ Mobile-first design
   - ✅ Grid system adaptativo
   - ✅ Menu colapsável
   - ✅ Cards reorganizáveis
   - ✅ Tabelas com scroll horizontal

5. **Home Page** 🏠
   - ✅ Hero section com gradiente
   - ✅ **Estatísticas em tempo real**:
     - Total de ofertas
     - Cupons ativos
     - Economia total gerada
     - Templates disponíveis
   - ✅ Seção de funcionalidades (6 cards)
   - ✅ Ofertas em destaque
   - ✅ Call-to-action
   - ✅ Footer informativo

6. **Quick-Create** ⚡
   - ✅ Modal inline
   - ✅ Criação sem sair da página
   - ✅ **Atualização automática** de dropdown
   - ✅ **Item já selecionado** após criar
   - ✅ Disponível para:
     - Vendedores (em ofertas e cupons)
     - Categorias (em ofertas)
     - Fabricantes (em ofertas)

---

## 🔌 API REST

### Características

- ✅ **35+ endpoints** disponíveis
- ✅ **Autenticação Bearer Token**
- ✅ HTTP Basic Auth alternativo
- ✅ **Documentação interativa** (`/api-docs`)
- ✅ Exemplos em **4 linguagens**:
  - Python (requests)
  - Node.js (axios)
  - PHP (cURL)
  - cURL (bash)

### Principais Recursos

- ✅ Endpoint `/health` para monitoramento
- ✅ Filtros via query parameters
- ✅ Paginação (planejado)
- ✅ Rate limiting (planejado)
- ✅ CORS configurável
- ✅ Respostas JSON padronizadas
- ✅ Códigos HTTP adequados
- ✅ Tratamento de erros consistente

### Endpoints por Categoria

**Autenticação (2)**
- POST `/api/auth/token`
- POST `/api/auth/login`

**Vendedores (5)**
- GET/POST `/api/sellers`
- GET/PUT/DELETE `/api/sellers/<id>`

**Categorias (5)**
- GET/POST `/api/categories`
- GET/PUT/DELETE `/api/categories/<id>`

**Fabricantes (5)**
- GET/POST `/api/manufacturers`
- GET/PUT/DELETE `/api/manufacturers/<id>`

**Ofertas (2)**
- GET/POST `/api/offers`

**Templates (2)**
- GET/POST `/api/templates`

**Usuários (4)**
- GET/POST `/api/users`
- GET/PUT `/api/users/<id>`

**Grupos (2)**
- GET/POST `/api/groups`

**Wishlists (3)**
- GET/POST `/api/wishlists`
- POST `/api/wishlists/<id>/items`

**Namespaces (2)**
- GET/POST `/api/namespaces`

**Publications (2)**
- GET/POST `/api/publications`

---

## 🔒 Segurança

### Camadas de Proteção

1. **Autenticação**
   - ✅ Flask-Login para sessões
   - ✅ JWT tokens para API
   - ✅ HTTP Basic Auth
   - ✅ Senhas hasheadas (Werkzeug)

2. **Autorização**
   - ✅ **Role-Based Access Control**:
     - Admin (acesso total)
     - Editor (criar/editar)
     - Viewer (apenas visualizar)
   - ✅ Decoradores `@login_required`
   - ✅ Decoradores `@role_required`

3. **CSRF Protection**
   - ✅ Tokens em todos os formulários
   - ✅ Flask-WTF integration
   - ✅ Validação automática

4. **Upload Seguro** (7 Camadas)
   - ✅ Validação de extensão
   - ✅ Validação de content-type
   - ✅ Validação com Pillow (imagem real)
   - ✅ Limite de tamanho (5MB)
   - ✅ Nome de arquivo seguro
   - ✅ Diretório isolado
   - ✅ Permissões corretas (755/644)

5. **Validação de Dados**
   - ✅ WTForms validators
   - ✅ SQLAlchemy constraints
   - ✅ Sanitização de inputs
   - ✅ Proteção contra SQL Injection

6. **Configuração**
   - ✅ Secrets em variáveis de ambiente
   - ✅ `.env` não commitado
   - ✅ `env.example` como template
   - ✅ SECRET_KEY obrigatória

---

## 💡 Recursos Especiais

### 1. Filtro de Vendedores Inativos

- ✅ **Automático** em todas listagens
- ✅ Vendedor inativo = ofertas ocultas
- ✅ **Reversível** (nada é deletado)
- ✅ Aplicado em:
  - Home
  - Dashboard
  - Ofertas
  - API

### 2. Símbolos de Moedas

- ✅ 12 moedas suportadas
- ✅ Símbolos corretos (R$, $, €, £, ¥)
- ✅ Filtro Jinja2: `{{ currency|currency_symbol }}`
- ✅ Exibição em todas as páginas

### 3. Conversão HTML → Texto

- ✅ **Automática** ao compartilhar
- ✅ Formatação específica por rede:
  - WhatsApp: `*negrito*`, `_itálico_`
  - Telegram: `**negrito**`, `__itálico__`
  - Instagram: texto puro
- ✅ Listas convertidas para bullets
- ✅ Quebras de linha preservadas

### 4. Cálculo de Desconto com Cupom

- ✅ Calcula melhor desconto entre cupons
- ✅ Respeita limite máximo (%)
- ✅ Nunca resulta em preço negativo
- ✅ Exibição opcional (checkbox)
- ✅ Namespace `{price_with_coupon}`

### 5. Menu Sempre no Topo

- ✅ `z-index: 9999` garantido
- ✅ Toasts abaixo do menu
- ✅ Modals abaixo do menu
- ✅ Sem sobreposição

---

## 📊 Estatísticas do Sistema

### Números do Projeto

- **Funcionalidades:** 40+
- **Rotas Web:** ~45
- **Rotas API:** ~35
- **Tabelas no Banco:** 17
- **Namespaces Disponíveis:** 50+
- **Moedas Suportadas:** 12
- **Redes Sociais:** 6+
- **Camadas de Segurança:** 7
- **Temas:** 2 (Claro + Escuro)

### Tecnologias

- **Backend:** Flask 3.0+ + SQLAlchemy
- **Frontend:** Bootstrap 5.3.3 + Vanilla JS
- **Editor:** Quill.js 1.3.6
- **Upload:** Pillow (PIL)
- **Auth:** Flask-Login + JWT
- **Database:** SQLite / PostgreSQL / MySQL

---

## 🎯 Casos de Uso

### Caso 1: Criar Oferta Completa

1. Acesse `/ofertas/nova`
2. Upload de imagem do produto
3. Preencha nome e descrição (com editor HTML)
4. Defina preços (atual + antigo)
5. Configure parcelas (quantidade, valor, juros)
6. Selecione vendedor (ou crie novo com quick-create)
7. Selecione categoria e fabricante
8. Defina data/hora de expiração
9. Salve
10. **Toast de sucesso** aparece

### Caso 2: Compartilhar em Redes Sociais

1. Na listagem de ofertas, clique em "Compartilhar"
2. Selecione a rede social (ou via URL: `?channel=whatsapp`)
3. Selecione um template
4. Escolha cupons ativos (todos selecionados por padrão)
5. Marque "Calcular preço com cupom" (opcional)
6. **Texto gerado automaticamente** com todas substituições
7. Clique em "Copiar"
8. Cole na rede social

### Caso 3: Configurar Vendedor com Cor

1. Acesse `/admin/sellers`
2. Clique em "Editar" no vendedor
3. Abra a aba "Cor do Vendedor"
4. Escolha um modo:
   - Cor sólida (colorpicker)
   - Gradiente pré-definido
   - CSS customizado
5. **Veja preview em tempo real**
6. Salve
7. Cor aplicada automaticamente em todas as ofertas

### Caso 4: Criar Cupom com Limite

1. Acesse `/cupons/novo`
2. Selecione vendedor
3. Digite código (ex: DESC10)
4. Escolha tipo: "Porcentagem (%)"
5. Valor: 10
6. **Desconto máximo**: R$ 50
7. Data de expiração (opcional)
8. Salve
9. Cupom disponível para uso em ofertas

---

## 🚀 Roadmap

### Em Desenvolvimento

- [ ] Paginação nas listagens
- [ ] Exportação (CSV, Excel, PDF)
- [ ] Dashboard com gráficos
- [ ] Histórico de alterações

### Planejado

- [ ] Notificações por email
- [ ] Auto-post em redes sociais
- [ ] PWA (offline-first)
- [ ] Multi-idioma (EN, ES)
- [ ] Sistema de favoritos
- [ ] Webhooks
- [ ] Integração com Google Sheets
- [ ] App móvel (React Native)

---

## 📚 Mais Informações

Consulte a pasta `/docs` para documentação técnica detalhada de cada funcionalidade.

---

**Última Atualização:** 04/12/2025  
**Versão do Sistema:** 2.0  
**Status:** Produção Ready ✅
