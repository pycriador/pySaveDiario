# 🔧 Solução de Problemas - Templates Personalizados

## ❌ Erro: 404 ao salvar template

### Causa
A rota `/template-social-network/save` não está registrada ou o servidor não está rodando.

### Solução
1. Reinicie o servidor Flask:
```bash
flask run
```

2. Verifique se a rota está registrada:
```bash
flask routes | grep template-social-network
```

3. Verifique o console do navegador para ver a URL exata sendo chamada

---

## ❌ Erro: 400 BAD REQUEST

### Causa
Dados enviados estão incompletos ou em formato incorreto.

### Solução
1. Abra o Console do navegador (F12)
2. Procure por: `💾 Salvando template:`
3. Verifique se tem `template_id`, `social_network` e `custom_body`

**Exemplo correto:**
```json
{
  "template_id": 4,
  "social_network": "whatsapp",
  "custom_body": "*Texto formatado*"
}
```

---

## ❌ Erro: SyntaxError: Unexpected token '<'

### Causa
Servidor retornou HTML ao invés de JSON (geralmente página de erro).

### Solução
1. Verifique se você está logado no sistema
2. Verifique se o modelo `TemplateSocialNetwork` existe:
```bash
python -c "from app.models import TemplateSocialNetwork; print('OK')"
```

3. Verifique se a tabela existe no banco:
```bash
sqlite3 instance/app.db "SELECT * FROM sqlite_master WHERE name='template_social_network_custom';"
```

---

## ❌ Emojis não inserem

### Causa
Event listeners não foram anexados aos botões.

### Solução
1. Abra o Console (F12)
2. Digite: `document.querySelectorAll('.emoji-btn').length`
3. Deve retornar número > 0

Se retornar 0:
- Recarregue a página (Ctrl+F5)
- Limpe o cache do navegador

---

## ❌ Formatação não aplica

### Causa
Nenhum texto foi selecionado ou rede não suporta.

### Solução
1. **Selecione o texto** antes de clicar no botão
2. Veja o aviso: "Selecione o texto que deseja formatar"
3. Para redes que não suportam (Instagram, etc.), você verá: "Riscado não suportado nesta rede"

---

## 🔍 Debug Mode

### Ativar Logs Detalhados

Abra o Console (F12) e procure por:

```javascript
// Ao gerar texto:
📝 Loaded custom template for WhatsApp  // Template customizado carregado
No custom template found, using default  // Usando padrão

// Ao salvar:
💾 Salvando template: {...}  // Dados enviados
Response status: 200  // Status HTTP
Response data: {...}  // Resposta do servidor
```

---

## ✅ Verificações Rápidas

### 1. Servidor Rodando?
```bash
curl http://localhost:5000/
```
Deve retornar HTML da home.

### 2. Autenticado?
```bash
# Verifique no navegador se está logado
# Ou teste a rota diretamente
curl http://localhost:5000/usuarios
```

### 3. Tabela Existe?
```bash
sqlite3 instance/app.db "PRAGMA table_info(template_social_network_custom);"
```

Deve listar: id, template_id, social_network, custom_body, created_at, updated_at

### 4. Modelo Carrega?
```bash
python -c "from app.models import TemplateSocialNetwork; print(TemplateSocialNetwork.__tablename__)"
```

Deve retornar: `template_social_network_custom`

---

## 🆘 Erros Comuns e Soluções

| Erro | Causa | Solução |
|------|-------|---------|
| 404 Not Found | Rota não existe | Reiniciar servidor |
| 400 Bad Request | Dados incompletos | Ver console (payload) |
| 401 Unauthorized | Não está logado | Fazer login |
| 500 Server Error | Erro no backend | Ver logs do Flask |
| Emoji não insere | Modal não abre | Recarregar página |
| Formatação não aplica | Texto não selecionado | Selecionar texto |

---

## 📝 Testando Manualmente

### Teste 1: Salvar Template

```bash
curl -X POST http://localhost:5000/template-social-network/save \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "template_id": 1,
    "social_network": "whatsapp",
    "custom_body": "*Teste* de template"
  }'
```

### Teste 2: Buscar Template

```bash
curl http://localhost:5000/template-social-network/1/whatsapp \
  -b cookies.txt
```

---

**Última Atualização:** 04/12/2025  
**Status:** ✅ Pronto para Troubleshooting

