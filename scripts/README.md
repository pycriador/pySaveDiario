# 📁 Scripts Directory - pySaveDiario

> **Documentação completa de todos os scripts Python, SQL e Shell do projeto**  
> Última atualização: 04/12/2025

---

## 📊 Visão Geral

```
┌─────────────────────────────────────────────────────────┐
│  📦 ESTATÍSTICAS DO DIRETÓRIO /scripts                 │
├─────────────────────────────────────────────────────────┤
│  🐍 Scripts Python:           30+                      │
│  💾 Arquivos SQL:             8                        │
│  🔧 Scripts Shell:            1                        │
│  📄 Total de linhas doc:      1200+                    │
│                                                         │
│  📂 CATEGORIAS                                          │
│  ├─ 🗄️  Migração de DB        7 scripts               │
│  ├─ 🌱 Inicialização/Seed     5 scripts               │
│  ├─ 👤 Gerenciamento Users    4 scripts               │
│  ├─ 🏷️  Namespaces            6 scripts               │
│  ├─ 🧪 Teste e Debug          8 scripts               │
│  ├─ 🔧 Configuração Sistema   1 script                │
│  └─ 🕷️  Web Scraping          5 scripts               │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Índice

- [🗄️ Scripts de Migração de Banco de Dados](#-scripts-de-migração-de-banco-de-dados)
- [🌱 Scripts de Inicialização e Seed](#-scripts-de-inicialização-e-seed)
- [👤 Scripts de Gerenciamento de Usuários](#-scripts-de-gerenciamento-de-usuários)
- [🏷️ Scripts de Namespaces](#-scripts-de-namespaces)
- [🧪 Scripts de Teste e Debug](#-scripts-de-teste-e-debug)
- [🔧 Scripts de Configuração do Sistema](#-scripts-de-configuração-do-sistema)
- [🕷️ Scripts de Web Scraping](#-scripts-de-web-scraping)
- [📊 Arquivos SQL](#-arquivos-sql)
- [🚀 Como Usar](#-como-usar)

---

## ⚡ Quick Start

**Primeiro uso? Execute na ordem:**

```bash
# 1. Criar banco e tabelas
flask db upgrade

# 2. Popular dados básicos
python scripts/seed_namespaces.py
python scripts/seed_admin_data.py
python scripts/init_social_networks.py

# 3. Criar usuário admin
python scripts/create_admin.py --email admin@example.com

# 4. Pronto! Inicie o servidor
flask run
```

**Comandos mais comuns:**

```bash
# Promover usuário a admin
python scripts/make_admin.py email@usuario.com

# Verificar templates
python scripts/check_templates.py

# Debug de namespaces
python scripts/debug_namespaces.py

# Configurar permissões (produção)
./scripts/setup_upload_permissions.sh
```

---

## 🗄️ Scripts de Migração de Banco de Dados

### `add_color_to_sellers.py`
**Descrição:** Adiciona campo de cor aos vendedores para identificação visual.

**O que faz:**
- Adiciona coluna `color` na tabela `sellers`
- Define cores padrão para vendedores conhecidos (Mercado Livre, Shopee, Amazon, etc.)
- Verifica se a coluna já existe antes de adicionar

**Cores Padrão:**
```python
Mercado Livre: #FFE600 (amarelo)
Shopee:        #EE4D2D (laranja)
Amazon:        #FF9900 (laranja claro)
Magazine Luiza: #DC143C (vermelho)
AliExpress:    #E62129 (vermelho)
Kabum:         #003DA5 (azul)
Casas Bahia:   #0070C0 (azul claro)
Extra:         #00A859 (verde)
```

**Uso:**
```bash
python scripts/add_color_to_sellers.py
```

---

### `add_max_discount_value_to_coupons.py`
**Descrição:** Adiciona campo de valor máximo de desconto para cupons.

**O que faz:**
- Adiciona coluna `max_discount_value` na tabela `coupons`
- Campo armazena o limite máximo de desconto em reais
- Útil para cupons de porcentagem com limite

**Exemplo de uso:**
```
Cupom: 10% de desconto, máximo R$ 70
- Produto R$ 500 → 10% = R$ 50 → Final: R$ 450
- Produto R$ 1000 → 10% = R$ 100, mas limite R$ 70 → Final: R$ 930
```

**Uso:**
```bash
python scripts/add_max_discount_value_to_coupons.py
```

---

### `add_min_purchase_value_to_coupons.py`
**Descrição:** Adiciona campo de valor mínimo de compra para cupons.

**O que faz:**
- Adiciona coluna `min_purchase_value` na tabela `coupons`
- Define o valor mínimo que o cliente precisa comprar para usar o cupom
- Implementa validação de valor mínimo

**Uso:**
```bash
python scripts/add_min_purchase_value_to_coupons.py
```

---

### `add_user_contact_fields.py`
**Descrição:** Adiciona campos de contato e redes sociais aos usuários.

**O que faz:**
- Adiciona 9 campos à tabela `users`:
  - `phone` - Telefone/celular
  - `address` - Endereço completo
  - `website` - Website pessoal
  - `instagram` - Perfil do Instagram
  - `facebook` - Perfil do Facebook
  - `twitter` - Perfil do Twitter/X
  - `linkedin` - Perfil do LinkedIn
  - `youtube` - Canal do YouTube
  - `tiktok` - Perfil do TikTok

**Uso:**
```bash
python scripts/add_user_contact_fields.py
```

---

### `create_template_social_network_custom.py`
**Descrição:** Cria tabela para armazenar templates customizados por rede social.

**O que faz:**
- Cria tabela `template_social_network_custom`
- Permite salvar diferentes versões de um template para cada rede social
- Adiciona índices para melhor performance
- Constraint única: um template não pode ter duas customizações para a mesma rede

**Estrutura da tabela:**
```sql
- id: Chave primária
- template_id: Referência ao template
- social_network: Nome da rede (whatsapp, instagram, etc.)
- custom_body: Corpo customizado do template
- created_at, updated_at: Timestamps
```

**Uso:**
```bash
python scripts/create_template_social_network_custom.py
```

---

### `apply_migration.py`
**Descrição:** Aplica migrações pendentes do Alembic.

**O que faz:**
- Executa `flask db upgrade`
- Aplica todas as migrações pendentes
- Útil para atualizar o schema do banco de dados

**Uso:**
```bash
python scripts/apply_migration.py
```

---

## 🌱 Scripts de Inicialização e Seed

### `seed_admin_data.py`
**Descrição:** Popula o banco de dados com dados administrativos iniciais.

**O que faz:**
- **Vendedores:** Shopee, Mercado Livre, Amazon, Magazine Luiza, AliExpress, Kabum
- **Categorias:** Eletrônicos, Jogos, Casa, Decoração, Perfumes
- **Fabricantes:** Nintendo, Apple, Sony, PlayStation, Microsoft

**Características:**
- Verifica se os dados já existem (não duplica)
- Inclui descrições, websites e slugs
- Adiciona ícones do Bootstrap às categorias

**Uso:**
```bash
python scripts/seed_admin_data.py
```

**Saída esperada:**
```
🌱 SEED - Dados Administrativos
📦 Vendedores: 6 criados
🏷️  Categorias: 5 criadas
🏭 Fabricantes: 5 criados
✅ SUCESSO!
```

---

### `seed_namespaces.py`
**Descrição:** Popula namespaces padrão para templates.

**O que faz:**
- Cria namespaces de **OFFER** (11 namespaces):
  - `product_name`, `price`, `old_price`, `discount`
  - `vendor_name`, `offer_url`, `category`, `brand`
  - `description`, `expires_at`, `currency`

- Cria namespaces **GLOBAL** (3 namespaces):
  - `user_name`, `today`, `time`

**Uso:**
```bash
python scripts/seed_namespaces.py
```

---

### `init_default_settings.py`
**Descrição:** Inicializa configurações padrão do aplicativo.

**O que faz:**
- Define moeda padrão como `BRL`
- Cria entrada na tabela `app_settings`
- Verifica se já existe antes de criar

**Uso:**
```bash
python scripts/init_default_settings.py
```

---

### `init_social_networks.py`
**Descrição:** Inicializa configurações padrão de redes sociais.

**O que faz:**
- Cria configurações para 4 redes:
  - **Instagram:** Sufixo com hashtags
  - **Facebook:** Prefixo e sufixo motivacionais
  - **WhatsApp:** Formatação com negrito e itálico
  - **Telegram:** Emojis e call-to-action

**Configurações criadas:**
```python
Instagram: suffix = "#ofertas #descontos #promoção"
Facebook:  prefix = "🔥 OFERTA IMPERDÍVEL!\n\n"
           suffix = "\n\n👍 Curta nossa página..."
WhatsApp:  prefix = "💰 *PROMOÇÃO*\n\n"
           suffix = "\n\n_Compartilhe com quem precisa!_"
Telegram:  prefix = "📢 NOVA OFERTA!\n\n"
           suffix = "\n\n🔔 Ative as notificações..."
```

**Uso:**
```bash
python scripts/init_social_networks.py
```

---

### `setup_admin_module.py`
**Descrição:** Configuração inicial completa do módulo admin.

**O que faz:**
- Executa todos os scripts de seed em sequência
- Cria estrutura completa de dados administrativos
- Script mestre para inicialização

**Uso:**
```bash
python scripts/setup_admin_module.py
```

---

## 👤 Scripts de Gerenciamento de Usuários

### `create_admin.py`
**Descrição:** Cria usuário administrador via linha de comando.

**O que faz:**
- Cria usuário com papel Admin ou Editor
- Aceita argumentos via CLI ou solicita senha segura
- Verifica se o email já existe

**Uso:**
```bash
# Modo interativo (solicita senha)
python scripts/create_admin.py --email admin@example.com

# Com senha na linha de comando
python scripts/create_admin.py --email admin@example.com --password senha123

# Com nome personalizado
python scripts/create_admin.py \
  --email admin@example.com \
  --display-name "Super Admin" \
  --role admin
```

**Argumentos:**
- `--email` (obrigatório): Email do usuário
- `--display-name` (opcional): Nome de exibição
- `--password` (opcional): Senha (se omitido, solicita)
- `--role` (opcional): admin ou editor (padrão: admin)

---

### `create_user.py`
**Descrição:** Script interativo completo para gerenciamento de usuários.

**O que faz:**
- **Criar usuários:** Wizard interativo com confirmação
- **Listar usuários:** Exibe todos com cores por papel
- **Deletar usuários:** Com confirmação de segurança
- **Modo rápido:** Criação via CLI sem interação

**Características:**
- Interface colorida no terminal
- Validação de senha (mínimo 6 caracteres)
- Confirmação de senha
- Proteção contra exclusão acidental

**Uso:**
```bash
# Modo interativo (menu)
python scripts/create_user.py

# Listar usuários
python scripts/create_user.py --list

# Modo rápido (sem interação)
python scripts/create_user.py --quick \
  email@example.com \
  "Nome Completo" \
  senha123 \
  admin
```

**Menu Interativo:**
```
1 - Criar novo usuário
2 - Listar usuários existentes
3 - Deletar usuário
4 - Sair
```

---

### `fix_admin_user.py`
**Descrição:** Verifica e corrige papéis de usuários administradores.

**O que faz:**
- Lista todos os usuários e seus papéis
- Identifica usuários com papel Admin
- Permite promover usuário a Admin se nenhum existe
- Corrige papéis inválidos para Member

**Uso:**
```bash
python scripts/fix_admin_user.py
```

**Cenários de uso:**
1. Nenhum admin existe → Solicita email para promover
2. Admin foi rebaixado acidentalmente → Restaura papel
3. Papel inválido → Corrige para Member

---

### `make_admin.py`
**Descrição:** Promove qualquer usuário existente para Admin.

**O que faz:**
- Busca usuário por email
- Promove para papel ADMIN
- Exibe antes e depois da mudança
- Lista usuários disponíveis se email não encontrado

**Uso:**
```bash
python scripts/make_admin.py usuario@gmail.com
```

**Saída esperada:**
```
🚀 Iniciando promoção para ADMIN...
📧 Email: usuario@gmail.com

👤 Usuário: João Silva
📧 Email: usuario@gmail.com
🎭 Papel atual: member

🔄 Promovendo para ADMIN...
✅ usuario@gmail.com agora é ADMINISTRADOR!
🎉 Papel atualizado: member → ADMIN
```

---

## 🏷️ Scripts de Namespaces

### `add_coupon_namespaces.py`
**Descrição:** Adiciona namespaces específicos para cupons.

**Namespaces criados:**
- `coupon_code` / `code` - Código do cupom
- `seller` / `seller_name` - Nome do vendedor
- `coupon_expires` - Data de expiração

**Uso:**
```bash
python scripts/add_coupon_namespaces.py
```

---

### `add_description_namespaces.py`
**Descrição:** Adiciona namespaces para descrição de produtos.

**Namespaces criados:**
- `product_description` - Descrição completa (converte HTML)
- `description` - Atalho para descrição
- `descricao` - Versão em português

**Recursos:**
- Conversão automática de HTML para texto formatado
- Adaptação por rede social (WhatsApp, Telegram, Instagram)

**Uso:**
```bash
python scripts/add_description_namespaces.py
```

---

### `add_missing_coupon_namespaces.py`
**Descrição:** Adiciona namespaces faltantes para cupons.

**Namespaces criados:**
- `coupon_discount_type` / `tipo_desconto` - Tipo de desconto
- `coupon_discount_value` / `valor_desconto` - Valor do desconto
- `max_discount_value` / `limite_desconto` - Limite máximo
- `coupon_max_discount` - Desconto máximo
- `validade_cupom` / `expira_em` - Validade

**Uso:**
```bash
python scripts/add_missing_coupon_namespaces.py
```

---

### `add_min_purchase_namespaces.py`
**Descrição:** Adiciona namespaces para valor mínimo de compra.

**Namespaces criados:**
- `min_purchase_value` - Valor mínimo da compra
- `compra_minima` - Alias em português
- `valor_minimo` - Alias curto

**Uso:**
```bash
python scripts/add_min_purchase_namespaces.py
```

---

### `reorganize_coupon_namespaces.py`
**Descrição:** Reorganiza e adiciona namespaces mais claros para cupons.

**Namespaces criados:**
- **Porcentagem:** `porcentagem`, `desconto_porcentagem`, `percentual`
- **Valor mínimo:** `valor_minimo_compra`, `minimo`
- **Valor máximo:** `valor_maximo_desconto`, `maximo`, `limite`
- **Desconto fixo:** `desconto_fixo`, `valor_fixo`

**Uso:**
```bash
python scripts/reorganize_coupon_namespaces.py
```

---

### `add_user_global_namespaces.py`
**Descrição:** Adiciona namespaces globais para informações do usuário.

**Namespaces criados (17 no total):**

**Contato:**
- `user_phone` / `telefone` / `celular`
- `user_address` / `endereco`
- `user_website` / `site`

**Redes Sociais:**
- `user_instagram` / `instagram`
- `user_facebook` / `facebook`
- `user_twitter` / `twitter`
- `user_linkedin` / `linkedin`
- `user_youtube` / `youtube`
- `user_tiktok` / `tiktok`

**Uso:**
```bash
python scripts/add_user_global_namespaces.py
```

---

## 🧪 Scripts de Teste e Debug

### `check_templates.py`
**Descrição:** Verifica e exibe templates no banco de dados.

**O que faz:**
- Lista todos os templates com detalhes
- Mostra ID, slug, descrição, canais, corpo
- Exibe URI do banco de dados
- Pode criar template de teste

**Uso:**
```bash
# Listar templates
python scripts/check_templates.py

# Criar template de teste
python scripts/check_templates.py --create-test
```

**Saída esperada:**
```
📋 Templates no Banco de Dados
✅ Total de templates: 5

1. Template WhatsApp
   ID: 1
   Slug: whatsapp-oferta
   Descrição: Template para ofertas no WhatsApp
   Canais: whatsapp
   Corpo: 💰 *PROMOÇÃO*...
   Criado em: 2025-12-04 10:30:00
```

---

### `debug_namespaces.py`
**Descrição:** Debug detalhado de namespaces e enums.

**O que faz:**
- Exibe valores dos enums `NamespaceScope`
- Lista todos os namespaces do banco
- Testa queries com filtros
- Agrupa namespaces por scope
- Mostra tipos e valores

**Uso:**
```bash
python scripts/debug_namespaces.py
```

**Saída esperada:**
```
DEBUG: Namespace Query
1. Enum Values:
   NamespaceScope.OFFER = 'OFFER'
   NamespaceScope.COUPON = 'COUPON'
   NamespaceScope.GLOBAL = 'GLOBAL'

2. All Namespaces in DB:
   Total: 45
   - product_name: scope=OFFER
   - coupon_code: scope=COUPON

4. Grouped by Scope:
   Offer: 15
   Coupon: 20
   Global: 10
```

---

### `test_template_social_network.py`
**Descrição:** Testa criação de templates customizados por rede.

**O que faz:**
- Testa CRUD de `TemplateSocialNetwork`
- Verifica constraint única
- Valida relacionamentos
- Testa índices

**Uso:**
```bash
python scripts/test_template_social_network.py
```

---

### `test_api.py`
**Descrição:** Testes básicos da API REST.

**O que testa:**
- Endpoints de autenticação
- CRUD de recursos
- Validações
- Respostas JSON

**Uso:**
```bash
python scripts/test_api.py
```

---

### `test_quick_create.py` / `test_quick_create_debug.py`
**Descrição:** Testa funcionalidade de criação rápida.

**O que testa:**
- Quick create de ofertas
- Quick create de cupons
- Quick create de templates
- Validações de formulário

**Uso:**
```bash
python scripts/test_quick_create.py
python scripts/test_quick_create_debug.py  # Versão com mais logs
```

---

### `test_upload_security.py`
**Descrição:** Testa segurança de upload de arquivos.

**O que testa:**
- Validação de extensões permitidas
- Proteção contra path traversal
- Limite de tamanho de arquivo
- Tipos MIME válidos

**Uso:**
```bash
python scripts/test_upload_security.py
```

---

### `test_url_format.py`
**Descrição:** Testa formatação e validação de URLs.

**O que testa:**
- Parsing de URLs
- Validação de formato
- Extração de domínio
- Normalização de URLs

**Uso:**
```bash
python scripts/test_url_format.py
```

---

### `test_with_login.py`
**Descrição:** Testes que requerem autenticação.

**O que testa:**
- Login/logout
- Sessões
- Proteção de rotas
- Permissões

**Uso:**
```bash
python scripts/test_with_login.py
```

---

## 🔧 Scripts de Configuração do Sistema

### `setup_upload_permissions.sh`
**Descrição:** Script Bash para configurar permissões seguras da pasta de uploads.

**O que faz:**
- Detecta automaticamente o usuário do servidor web (www-data, nginx, apache)
- Define ownership correto para pasta de uploads
- Configura permissões seguras:
  - Diretórios: `755` (rwxr-xr-x)
  - Arquivos: `644` (rw-r--r--)
- Remove permissão de execução de arquivos
- Cria estrutura de diretórios se não existir
- Verifica e exibe permissões após configuração

**Características de Segurança:**
- Solicita confirmação antes de executar
- Detecta automaticamente se precisa de `sudo`
- Previne execução de scripts maliciosos em uploads
- Output colorido para fácil leitura

**Uso:**
```bash
# Dar permissão de execução
chmod +x scripts/setup_upload_permissions.sh

# Executar (pode precisar de sudo)
./scripts/setup_upload_permissions.sh

# Ou com sudo se necessário
sudo ./scripts/setup_upload_permissions.sh
```

**Saída esperada:**
```
=== Setup Upload Permissions ===

Project root: /path/to/pySaveDiario
Upload directory: /path/to/pySaveDiario/app/static/uploads

Web server user: www-data

Continue with permission setup? (y/n) y

Setting up permissions...
1. Setting ownership to www-data...
2. Setting directory permissions to 755...
3. Setting file permissions to 644...
4. Removing execute permission from files...

=== Verification ===
Upload directory permissions:
drwxr-xr-x  www-data  www-data  uploads/
drwxr-xr-x  www-data  www-data  uploads/products/

✓ Permissions setup complete!

Important:
1. Ensure your Flask app runs as user: www-data
2. Verify web server configuration blocks script execution in uploads/
3. Test with: python scripts/test_upload_security.py
```

**Quando usar:**
- Após clonar o repositório em produção
- Ao configurar servidor web (Nginx, Apache)
- Após mudança de usuário do servidor
- Se houver erros de permissão em uploads

---

## 🕷️ Scripts de Web Scraping

### `mercadolivre_scraper.py`
**Descrição:** Scraper básico para Mercado Livre (requests + BeautifulSoup).

**O que faz:**
- Extrai dados de produtos do ML
- Captura preço, título, imagem
- Não requer Selenium (mais rápido)
- **Limitação:** Pode não funcionar com proteções anti-bot

**Uso:**
```bash
python scripts/mercadolivre_scraper.py
```

---

### `mercadolivre_scraper_selenium.py`
**Descrição:** Scraper avançado com Selenium para Mercado Livre.

**O que faz:**
- Usa navegador real (Chrome/Firefox)
- Lida com JavaScript dinâmico
- Aguarda carregamento de elementos
- Pode resolver CAPTCHAs manualmente

**Requisitos:**
- Selenium instalado
- ChromeDriver ou GeckoDriver
- Chrome ou Firefox

**Uso:**
```bash
python scripts/mercadolivre_scraper_selenium.py
```

---

### `mercadolivre_selenium_scraper.py`
**Descrição:** Outra variante do scraper com Selenium.

**Diferenças:**
- Configurações diferentes de navegador
- Suporte a perfil do Chrome
- Opções de headless/headed

**Uso:**
```bash
python scripts/mercadolivre_selenium_scraper.py
```

---

### `get_seller_from_product.py`
**Descrição:** Extrai informações do vendedor a partir da URL do produto.

**O que faz:**
- Acessa página do produto
- Identifica vendedor
- Extrai reputação e avaliações
- Retorna dados estruturados

**Uso:**
```bash
python scripts/get_seller_from_product.py <URL_DO_PRODUTO>
```

---

### `get_seller_id.py`
**Descrição:** Obtém ID do vendedor no Mercado Livre.

**O que faz:**
- Extrai seller_id da API do ML
- Útil para construir URLs de busca
- Retorna informações básicas do vendedor

**Uso:**
```bash
python scripts/get_seller_id.py <URL_VENDEDOR>
```

---

### `exemplo_uso_mercadolivre.py`
**Descrição:** Exemplo de uso dos scrapers do Mercado Livre.

**O que faz:**
- Demonstra como usar os scrapers
- Mostra parsing de dados
- Exemplo de integração com banco de dados
- Tutorial comentado

**Uso:**
```bash
python scripts/exemplo_uso_mercadolivre.py
```

---

## 📊 Arquivos SQL

### `add_color_to_sellers.sql`
**Descrição:** Adiciona coluna de cor aos vendedores.

```sql
ALTER TABLE sellers ADD COLUMN color VARCHAR(255) DEFAULT '#6b7280';

UPDATE sellers SET color = '#FFE600' WHERE LOWER(name) = 'mercado livre';
UPDATE sellers SET color = '#EE4D2D' WHERE LOWER(name) = 'shopee';
-- ... (outros vendedores)
```

**Uso:**
```bash
sqlite3 instance/database.db < scripts/add_color_to_sellers.sql
```

---

### `add_coupon_namespaces.sql`
**Descrição:** Adiciona namespaces de cupons via SQL.

```sql
INSERT OR IGNORE INTO namespaces (name, label, description, scope) VALUES
('coupon_code', 'Código do Cupom', 'Código do cupom de desconto (ex: PRIMEIRACOMPRA)', 'coupon'),
('code', 'Código (Alias)', 'Código do cupom - forma abreviada (ex: FRETE10)', 'coupon'),
-- ...
```

**Uso:**
```bash
sqlite3 instance/database.db < scripts/add_coupon_namespaces.sql
```

---

### `add_description_namespaces.sql`
**Descrição:** Adiciona namespaces de descrição de produtos.

```sql
INSERT INTO namespaces (name, label, description, scope, created_at, updated_at)
SELECT 'product_description', 'Descrição do Produto', '...', 'OFFER', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM namespaces WHERE name = 'product_description');
```

**Uso:**
```bash
sqlite3 instance/database.db < scripts/add_description_namespaces.sql
```

---

### `add_installment_namespaces.sql`
**Descrição:** Adiciona namespaces para parcelamento.

**Namespaces criados:**
- `installment_count` - Quantidade de parcelas
- `installment_value` - Valor de cada parcela
- `installment_interest_free` - Com/sem juros
- `installment_full` - Texto completo formatado

**Uso:**
```bash
sqlite3 instance/database.db < scripts/add_installment_namespaces.sql
```

---

### `add_max_discount_value_to_coupons.sql`
**Descrição:** Adiciona coluna de desconto máximo.

```sql
ALTER TABLE coupons ADD COLUMN max_discount_value NUMERIC(10, 2);
```

**Uso:**
```bash
sqlite3 instance/database.db < scripts/add_max_discount_value_to_coupons.sql
```

---

### `add_price_with_coupon_namespace.sql`
**Descrição:** Adiciona namespace para preço com cupom aplicado.

```sql
INSERT OR IGNORE INTO namespaces (name, label, description, scope, created_at, updated_at)
VALUES ('price_with_coupon', 'Preço com Cupom', 'Preço do produto com o desconto do cupom aplicado (ex: R$ 90.00)', 'OFFER', datetime('now'), datetime('now'));
```

**Uso:**
```bash
sqlite3 instance/database.db < scripts/add_price_with_coupon_namespace.sql
```

---

### `add_template_social_networks.sql`
**Descrição:** Cria tabela de associação template-rede social.

```sql
CREATE TABLE IF NOT EXISTS template_social_networks (
    template_id INTEGER NOT NULL,
    social_network_id INTEGER NOT NULL,
    PRIMARY KEY (template_id, social_network_id),
    FOREIGN KEY (template_id) REFERENCES templates(id) ON DELETE CASCADE,
    FOREIGN KEY (social_network_id) REFERENCES social_network_configs(id) ON DELETE CASCADE
);
```

**Uso:**
```bash
sqlite3 instance/database.db < scripts/add_template_social_networks.sql
```

---

### `create_social_networks_table.sql`
**Descrição:** Cria tabela de configurações de redes sociais.

```sql
CREATE TABLE IF NOT EXISTS social_network_configs (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    network VARCHAR(50) NOT NULL UNIQUE,
    prefix_text TEXT,
    suffix_text TEXT,
    active BOOLEAN
);

INSERT OR IGNORE INTO social_network_configs (network, prefix_text, suffix_text, active) VALUES
('instagram', '', '#ofertas #descontos #promoção', 1),
('facebook', '🔥 OFERTA IMPERDÍVEL!\n\n', '\n\n👍 Curta nossa página...', 1),
-- ...
```

**Uso:**
```bash
sqlite3 instance/database.db < scripts/create_social_networks_table.sql
```

---

## 🚀 Como Usar

### Instalação Inicial Completa

Para configurar o projeto do zero, execute na ordem:

```bash
# 0. Configurar permissões de upload (se em produção)
chmod +x scripts/setup_upload_permissions.sh
./scripts/setup_upload_permissions.sh

# 1. Criar banco de dados e tabelas
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 2. Seed de dados básicos
python scripts/seed_namespaces.py
python scripts/seed_admin_data.py
python scripts/init_social_networks.py
python scripts/init_default_settings.py

# 3. Criar usuário admin
python scripts/create_admin.py \
  --email admin@example.com \
  --display-name "Administrador" \
  --password suasenha123

# 4. Adicionar campos extras (opcional, se migrando)
python scripts/add_color_to_sellers.py
python scripts/add_max_discount_value_to_coupons.py
python scripts/add_min_purchase_value_to_coupons.py
python scripts/add_user_contact_fields.py
python scripts/create_template_social_network_custom.py

# 5. Adicionar namespaces extras
python scripts/add_coupon_namespaces.py
python scripts/add_description_namespaces.py
python scripts/add_missing_coupon_namespaces.py
python scripts/add_min_purchase_namespaces.py
python scripts/add_user_global_namespaces.py
python scripts/reorganize_coupon_namespaces.py
```

---

### Scripts de Manutenção Comuns

#### Promover usuário a Admin
```bash
python scripts/make_admin.py usuario@email.com
```

#### Verificar e corrigir papéis de usuários
```bash
python scripts/fix_admin_user.py
```

#### Listar templates
```bash
python scripts/check_templates.py
```

#### Criar template de teste
```bash
python scripts/check_templates.py --create-test
```

#### Debug de namespaces
```bash
python scripts/debug_namespaces.py
```

---

### Scripts de Scraping

#### Scraper básico (rápido)
```bash
python scripts/mercadolivre_scraper.py
```

#### Scraper com Selenium (mais robusto)
```bash
python scripts/mercadolivre_scraper_selenium.py
```

#### Obter informações do vendedor
```bash
python scripts/get_seller_from_product.py "https://produto.mercadolivre.com.br/MLB-123456"
python scripts/get_seller_id.py "https://loja.mercadolivre.com.br/vendedor"
```

---

### Aplicar SQL Diretamente

Se preferir usar SQL puro ao invés dos scripts Python:

```bash
# Listar todas as tabelas
sqlite3 instance/database.db ".tables"

# Executar arquivo SQL
sqlite3 instance/database.db < scripts/nome_do_arquivo.sql

# Modo interativo
sqlite3 instance/database.db
sqlite> .read scripts/nome_do_arquivo.sql
sqlite> .exit
```

---

### Scripts de Teste

```bash
# Testar API
python scripts/test_api.py

# Testar upload de segurança
python scripts/test_upload_security.py

# Testar formatação de URL
python scripts/test_url_format.py

# Testar autenticação
python scripts/test_with_login.py

# Testar quick create
python scripts/test_quick_create.py
python scripts/test_quick_create_debug.py

# Testar template social network
python scripts/test_template_social_network.py
```

---

## 📝 Notas Importantes

### Ordem de Execução

Alguns scripts dependem de outros:

1. **Primeiro:** Scripts de criação de tabelas
2. **Depois:** Scripts de seed (namespaces, admin data)
3. **Por último:** Scripts de migração de colunas

### Segurança

- **Nunca** comite senhas em arquivos
- Use variáveis de ambiente para credenciais
- Scripts de scraping podem violar ToS de sites

### Performance

- Scripts de migração são idempotentes (podem ser executados múltiplas vezes)
- Scripts de seed verificam existência antes de criar
- Use SQL direto para operações em massa

### Backup

Sempre faça backup antes de executar migrações:

```bash
cp instance/database.db instance/database.db.backup
```

---

## 🆘 Troubleshooting

### "Column already exists"
```bash
# Normal! O script verifica e pula se já existe
✓ Coluna 'color' já existe na tabela 'sellers'
```

### "No such table"
```bash
# Execute as migrações primeiro
flask db upgrade
```

### "Permission denied"
```bash
# Torne o script executável
chmod +x scripts/nome_do_script.py
```

### Erros de import
```bash
# Certifique-se de estar no diretório raiz do projeto
cd /path/to/pySaveDiario
python scripts/nome_do_script.py
```

---

## 📚 Recursos Adicionais

- **Documentação Principal:** `/README.md`
- **Documentação da API:** `/docs/api-docs.html`
- **Guia de Features:** `/docs/FEATURES.md`
- **Referência Rápida:** `/docs/QUICK_REFERENCE.md`

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs: `logs/app.log`
2. Execute em modo debug: `FLASK_DEBUG=1 python scripts/script.py`
3. Consulte a documentação específica em `/docs/`

---

**Última atualização:** 04/12/2025  
**Total de scripts Python:** 30+  
**Total de arquivos SQL:** 8  
**Total de scripts Shell:** 1  
**Status:** ✅ Documentação completa e atualizada

