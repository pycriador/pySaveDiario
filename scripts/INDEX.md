# 📑 Índice de Scripts - pySaveDiario

> **Lista completa de todos os arquivos em `/scripts` com descrições de uma linha**

---

## 🐍 Scripts Python (.py)

| Arquivo | Descrição |
|---------|-----------|
| `add_color_to_sellers.py` | Adiciona campo de cor aos vendedores para identificação visual |
| `add_coupon_namespaces.py` | Adiciona namespaces específicos para cupons (code, seller, expires) |
| `add_description_namespaces.py` | Adiciona namespaces para descrição de produtos (HTML → texto formatado) |
| `add_max_discount_value_to_coupons.py` | Adiciona campo de valor máximo de desconto para cupons |
| `add_min_purchase_namespaces.py` | Adiciona namespaces para valor mínimo de compra |
| `add_min_purchase_value_to_coupons.py` | Adiciona campo de valor mínimo de compra para cupons |
| `add_missing_coupon_namespaces.py` | Adiciona namespaces faltantes para cupons (tipo, valor, limite) |
| `add_user_contact_fields.py` | Adiciona campos de contato e redes sociais aos usuários |
| `add_user_global_namespaces.py` | Adiciona namespaces globais para informações do usuário |
| `apply_migration.py` | Aplica migrações pendentes do Alembic (flask db upgrade) |
| `check_templates.py` | Verifica e exibe templates no banco de dados |
| `create_admin.py` | Cria usuário administrador via linha de comando |
| `create_template_social_network_custom.py` | Cria tabela para templates customizados por rede social |
| `create_user.py` | Script interativo completo para gerenciamento de usuários |
| `debug_namespaces.py` | Debug detalhado de namespaces e enums |
| `exemplo_uso_mercadolivre.py` | Exemplo de uso dos scrapers do Mercado Livre |
| `fix_admin_user.py` | Verifica e corrige papéis de usuários administradores |
| `get_seller_from_product.py` | Extrai informações do vendedor a partir da URL do produto |
| `get_seller_id.py` | Obtém ID do vendedor no Mercado Livre |
| `init_default_settings.py` | Inicializa configurações padrão do aplicativo (moeda BRL) |
| `init_social_networks.py` | Inicializa configurações padrão de redes sociais |
| `make_admin.py` | Promove qualquer usuário existente para Admin |
| `mercadolivre_scraper.py` | Scraper básico para Mercado Livre (requests + BeautifulSoup) |
| `mercadolivre_scraper_selenium.py` | Scraper avançado com Selenium para Mercado Livre |
| `mercadolivre_selenium_scraper.py` | Variante do scraper com Selenium (configurações diferentes) |
| `reorganize_coupon_namespaces.py` | Reorganiza e adiciona namespaces mais claros para cupons |
| `seed_admin_data.py` | Popula o banco com dados administrativos iniciais (sellers, categories, manufacturers) |
| `seed_namespaces.py` | Popula namespaces padrão para templates (offer, global) |
| `setup_admin_module.py` | Configuração inicial completa do módulo admin (script mestre) |
| `test_api.py` | Testes básicos da API REST |
| `test_quick_create.py` | Testa funcionalidade de criação rápida |
| `test_quick_create_debug.py` | Testa criação rápida com logs detalhados |
| `test_template_social_network.py` | Testa criação de templates customizados por rede |
| `test_upload_security.py` | Testa segurança de upload de arquivos |
| `test_url_format.py` | Testa formatação e validação de URLs |
| `test_with_login.py` | Testes que requerem autenticação |

---

## 💾 Arquivos SQL (.sql)

| Arquivo | Descrição |
|---------|-----------|
| `add_color_to_sellers.sql` | Adiciona coluna de cor aos vendedores (SQL puro) |
| `add_coupon_namespaces.sql` | Adiciona namespaces de cupons via SQL |
| `add_description_namespaces.sql` | Adiciona namespaces de descrição de produtos via SQL |
| `add_installment_namespaces.sql` | Adiciona namespaces para parcelamento (count, value, interest_free, full) |
| `add_max_discount_value_to_coupons.sql` | Adiciona coluna de desconto máximo via SQL |
| `add_price_with_coupon_namespace.sql` | Adiciona namespace para preço com cupom aplicado |
| `add_template_social_networks.sql` | Cria tabela de associação template-rede social |
| `create_social_networks_table.sql` | Cria tabela de configurações de redes sociais |

---

## 🔧 Scripts Shell (.sh)

| Arquivo | Descrição |
|---------|-----------|
| `setup_upload_permissions.sh` | Configura permissões seguras da pasta de uploads (755/644) |

---

## 📁 Diretórios

| Diretório | Descrição |
|-----------|-----------|
| `__pycache__/` | Cache Python (gerado automaticamente) |
| `chrome_profile/` | Perfil do Chrome para scraping com Selenium (dados do navegador) |

---

## 📚 Documentação

| Arquivo | Descrição |
|---------|-----------|
| `README.md` | Documentação completa de todos os scripts (1200+ linhas) |
| `CHEATSHEET.md` | Referência rápida dos comandos mais usados |
| `INDEX.md` | Este arquivo - índice de todos os scripts |

---

## 🎯 Scripts por Categoria

### 🗄️ Migração de Banco de Dados (7)
- `add_color_to_sellers.py`
- `add_max_discount_value_to_coupons.py`
- `add_min_purchase_value_to_coupons.py`
- `add_user_contact_fields.py`
- `create_template_social_network_custom.py`
- `apply_migration.py`
- `setup_admin_module.py`

### 🌱 Inicialização e Seed (5)
- `seed_admin_data.py`
- `seed_namespaces.py`
- `init_default_settings.py`
- `init_social_networks.py`
- `setup_admin_module.py`

### 👤 Gerenciamento de Usuários (4)
- `create_admin.py`
- `create_user.py`
- `fix_admin_user.py`
- `make_admin.py`

### 🏷️ Namespaces (6)
- `add_coupon_namespaces.py`
- `add_description_namespaces.py`
- `add_missing_coupon_namespaces.py`
- `add_min_purchase_namespaces.py`
- `reorganize_coupon_namespaces.py`
- `add_user_global_namespaces.py`

### 🧪 Teste e Debug (8)
- `check_templates.py`
- `debug_namespaces.py`
- `test_template_social_network.py`
- `test_api.py`
- `test_quick_create.py`
- `test_quick_create_debug.py`
- `test_upload_security.py`
- `test_url_format.py`
- `test_with_login.py`

### 🔧 Configuração do Sistema (1)
- `setup_upload_permissions.sh`

### 🕷️ Web Scraping (5)
- `mercadolivre_scraper.py`
- `mercadolivre_scraper_selenium.py`
- `mercadolivre_selenium_scraper.py`
- `get_seller_from_product.py`
- `get_seller_id.py`
- `exemplo_uso_mercadolivre.py`

---

## 🔍 Busca Rápida

### Preciso criar um usuário admin
```bash
python scripts/create_admin.py --email admin@example.com
# ou
python scripts/make_admin.py usuario@email.com
```

### Preciso popular o banco de dados
```bash
python scripts/seed_admin_data.py
python scripts/seed_namespaces.py
```

### Preciso adicionar campos novos
```bash
python scripts/add_color_to_sellers.py
python scripts/add_user_contact_fields.py
python scripts/add_max_discount_value_to_coupons.py
```

### Preciso debugar algo
```bash
python scripts/check_templates.py
python scripts/debug_namespaces.py
```

### Preciso fazer scraping
```bash
python scripts/mercadolivre_scraper.py
python scripts/mercadolivre_scraper_selenium.py
```

### Preciso testar
```bash
python scripts/test_api.py
python scripts/test_upload_security.py
```

---

## 📊 Estatísticas

```
Total de Scripts Python:  36 arquivos
Total de Arquivos SQL:    8 arquivos
Total de Scripts Shell:   1 arquivo
Total de Documentação:    3 arquivos (README, CHEATSHEET, INDEX)
Total Geral:             48+ arquivos
```

---

## 🔗 Links Úteis

- **[README completo](README.md)** - Documentação detalhada de cada script
- **[Cheat Sheet](CHEATSHEET.md)** - Comandos mais usados
- **[Documentação Principal](../README.md)** - Documentação do projeto
- **[API Docs](../docs/api-docs.html)** - Documentação da API

---

**📅 Última atualização:** 04/12/2025  
**✅ Status:** Completo e atualizado

