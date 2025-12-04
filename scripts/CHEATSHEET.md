# 🚀 Scripts Cheat Sheet - pySaveDiario

> **Referência rápida dos comandos mais usados**

---

## 📦 Setup Inicial

```bash
# Banco de dados
flask db upgrade

# Dados iniciais
python scripts/seed_namespaces.py
python scripts/seed_admin_data.py
python scripts/init_social_networks.py

# Criar admin
python scripts/create_admin.py --email admin@example.com
```

---

## 👤 Usuários

```bash
# Criar admin
python scripts/create_admin.py --email usuario@email.com

# Promover para admin
python scripts/make_admin.py usuario@email.com

# Corrigir papéis
python scripts/fix_admin_user.py

# Menu interativo
python scripts/create_user.py
```

---

## 🗄️ Migrações

```bash
# Aplicar migrações
python scripts/apply_migration.py

# Adicionar cor aos vendedores
python scripts/add_color_to_sellers.py

# Adicionar campos de cupom
python scripts/add_max_discount_value_to_coupons.py
python scripts/add_min_purchase_value_to_coupons.py

# Adicionar campos de usuário
python scripts/add_user_contact_fields.py

# Criar tabela de templates customizados
python scripts/create_template_social_network_custom.py
```

---

## 🏷️ Namespaces

```bash
# Namespaces básicos
python scripts/seed_namespaces.py

# Namespaces de cupons
python scripts/add_coupon_namespaces.py
python scripts/add_missing_coupon_namespaces.py
python scripts/add_min_purchase_namespaces.py
python scripts/reorganize_coupon_namespaces.py

# Namespaces de descrição
python scripts/add_description_namespaces.py

# Namespaces de usuário
python scripts/add_user_global_namespaces.py
```

---

## 🧪 Debug & Testes

```bash
# Verificar templates
python scripts/check_templates.py

# Criar template de teste
python scripts/check_templates.py --create-test

# Debug de namespaces
python scripts/debug_namespaces.py

# Testar API
python scripts/test_api.py

# Testar uploads
python scripts/test_upload_security.py
```

---

## 🔧 Configuração

```bash
# Permissões de upload (produção)
chmod +x scripts/setup_upload_permissions.sh
sudo ./scripts/setup_upload_permissions.sh
```

---

## 🕷️ Web Scraping

```bash
# Scraper básico
python scripts/mercadolivre_scraper.py

# Scraper com Selenium
python scripts/mercadolivre_scraper_selenium.py

# Obter vendedor
python scripts/get_seller_from_product.py "URL"
python scripts/get_seller_id.py "URL"

# Exemplo
python scripts/exemplo_uso_mercadolivre.py
```

---

## 💾 SQL Direto

```bash
# Executar arquivo SQL
sqlite3 instance/database.db < scripts/arquivo.sql

# Modo interativo
sqlite3 instance/database.db
.read scripts/arquivo.sql
.exit
```

---

## 🆘 Troubleshooting

```bash
# Backup do banco
cp instance/database.db instance/database.db.backup

# Restaurar backup
cp instance/database.db.backup instance/database.db

# Limpar cache Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Recriar banco do zero
rm instance/database.db
flask db upgrade
# Execute os scripts de seed novamente
```

---

## 📋 Ordem de Execução (Setup Completo)

```bash
# 1. Banco e tabelas
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 2. Dados básicos
python scripts/seed_namespaces.py
python scripts/seed_admin_data.py
python scripts/init_social_networks.py
python scripts/init_default_settings.py

# 3. Admin
python scripts/create_admin.py --email admin@email.com

# 4. Migrações extras (se necessário)
python scripts/add_color_to_sellers.py
python scripts/add_max_discount_value_to_coupons.py
python scripts/add_min_purchase_value_to_coupons.py
python scripts/add_user_contact_fields.py
python scripts/create_template_social_network_custom.py

# 5. Namespaces extras
python scripts/add_coupon_namespaces.py
python scripts/add_description_namespaces.py
python scripts/add_missing_coupon_namespaces.py
python scripts/add_min_purchase_namespaces.py
python scripts/add_user_global_namespaces.py
python scripts/reorganize_coupon_namespaces.py

# 6. Verificar
python scripts/check_templates.py
python scripts/debug_namespaces.py
```

---

## 🔑 Argumentos Comuns

### create_admin.py
```bash
--email EMAIL          # Email do admin (obrigatório)
--display-name NAME    # Nome de exibição (opcional)
--password SENHA       # Senha (opcional, solicita se omitido)
--role PAPEL           # admin ou editor (padrão: admin)
```

### create_user.py
```bash
--list                 # Listar usuários
--quick EMAIL NOME SENHA PAPEL  # Criação rápida
```

### check_templates.py
```bash
--create-test          # Criar template de teste
```

---

## 📊 Verificações Rápidas

```bash
# Contar usuários
sqlite3 instance/database.db "SELECT COUNT(*) FROM users;"

# Listar admins
sqlite3 instance/database.db "SELECT email, role FROM users WHERE role = 'admin';"

# Contar namespaces
sqlite3 instance/database.db "SELECT COUNT(*) FROM namespaces;"

# Listar templates
sqlite3 instance/database.db "SELECT id, name, slug FROM templates;"

# Verificar tabelas
sqlite3 instance/database.db ".tables"

# Schema de tabela
sqlite3 instance/database.db ".schema users"
```

---

**📚 Documentação completa:** `scripts/README.md`  
**⚡ Última atualização:** 04/12/2025

