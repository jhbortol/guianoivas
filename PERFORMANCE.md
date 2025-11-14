# Performance Build & Optimization Guide

## Resumo das Implementações

✅ **1. Critical CSS Inline**
- Arquivo crítico criado: `css/critical.css`
- Contém menu, hero e responsividade acima da dobra
- Será injetado inline em `<head>` durante build

✅ **2. Minificação de CSS/JS**
- Script: `tools/build.py`
- Redução: 32.9% em CSS, 26.8% em JS
- Saída: `dist/css/*.min.css` e `dist/js/*.min.js`

✅ **3. WebP & Responsive Images**
- Guia completo: `tools/WEBP_GUIDE.md`
- Inclui scripts Python para conversão automática
- Suporte a `<picture>` com fallback JPEG

---

## Como Usar

### 1. Minificar CSS/JS

```bash
cd /workspaces/guianoivas
python3 tools/build.py --minify
```

**Resultado:**
- CSS minificado: `dist/css/estilo.min.css`, `dist/css/critical.min.css`
- JS minificado: `dist/js/include-header.min.js`
- ~30% de redução em tamanho

### 2. Injetar Critical CSS (Futuro)

```bash
python3 tools/build.py --critical
```

Isso irá:
- Adicionar `<style>critical.css inline</style>` em `<head>`
- Carregar `estilo.css` com `media="print"` para evitar bloqueio
- Melhorar Largest Contentful Paint (LCP)

### 3. Converter Imagens para WebP

```bash
# 1. Instalar cwebp (se não tiver)
brew install webp  # Mac
# ou
sudo apt install webp  # Ubuntu

# 2. Converter manualmente
cd piracicaba/imagens
cwebp -q 80 *.jpg -o output.webp

# Ou usar o script do guia (tools/WEBP_GUIDE.md)
```

### 4. Executar Tudo de Uma Vez

```bash
python3 tools/build.py --all
```

---

## Estrutura de Arquivos Criados

```
tools/
├── build.py                 # Script minificação + critical CSS
├── CACHE_STRATEGY.md        # Guia de cache-control para produção
├── WEBP_GUIDE.md            # Guia completo WebP + responsive images
└── test_server_with_cache.py # Servidor local com headers de cache

piracicaba/
├── css/
│   ├── estilo.css          # CSS completo
│   └── critical.css        # CSS crítico (novo)
└── js/
    └── include-header.js   # Header loader

dist/ (gerado após build --minify)
├── css/
│   ├── estilo.min.css
│   └── critical.min.css
└── js/
    └── include-header.min.js
```

---

## Próximos Passos (Recomendados)

### Curto Prazo (Esta semana)
1. ✅ Adicionar `defer` aos scripts → **FEITO**
2. ✅ Adicionar `loading="lazy"` às imagens → **FEITO**
3. ⏭️ Converter imagens para WebP (siga `WEBP_GUIDE.md`)
4. ⏭️ Minificar e publicar com `build.py --minify`

### Médio Prazo (Próximas semanas)
5. Configurar cache-control headers no servidor (veja `CACHE_STRATEGY.md`)
6. Testar com Lighthouse / PageSpeed Insights
7. Injetar Critical CSS inline (usar `build.py --critical`)
8. Adicionar fingerprinting aos assets

### Longo Prazo (Automação CI/CD)
9. Integrar `tools/build.py` em GitHub Actions
10. Validar com htmlhint, stylelint na CI
11. Deploy automático para produção

---

## Performance Ganhos Esperados

| Otimização | Impacto |
|-----------|--------|
| `defer` scripts | -50ms First Contentful Paint |
| `loading="lazy"` | -200ms inicial, melhor performance mobile |
| CSS minificado | -6.3 KB por request |
| JS minificado | -303 bytes por request |
| WebP images | -30% tamanho imagens |
| Critical CSS inline | -1 request HTTP, melhora LCP |
| Cache headers | -300ms em recargas (cache local) |

**Total esperado:** ~0.5-1s de redução em carregamento.

---

## Validação

### Testar Localmente
```bash
# Servidor com cache headers simulado
python3 tools/test_server_with_cache.py

# Abrir http://localhost:8000 e verificar Network tab (DevTools)
```

### Lighthouse (Chrome DevTools)
1. F12 → Lighthouse
2. Gerar relatório
3. Verificar "Performance" score

### Critérios de Sucesso
- ✅ Defer: scripts não bloqueiam render
- ✅ Lazy-load: imagens abaixo da dobra com `loading="lazy"`
- ✅ Minificação: CSS/JS reduzidos 25-30%
- ✅ WebP: imagens servidas em formato moderno
- ✅ Critical CSS: `<style>` inline em `<head>` (futuro)

---

## Troubleshooting

### "cwebp: command not found"
```bash
# Instalar:
brew install webp
# ou
sudo apt install webp
```

### Build script não encontra pasta dist/
```bash
# Criar manualmente:
mkdir -p dist/css dist/js
```

### Imagens não carregam após mudar src
```bash
# Limpar cache do navegador:
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)
```

---

## Recursos

- [MDN: Performance](https://developer.mozilla.org/en-US/docs/Glossary/Performance)
- [Web.dev: Performance](https://web.dev/performance/)
- [Google Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [Squoosh: Image Optimizer](https://squoosh.app/)
- [WebP Format](https://developers.google.com/speed/webp)

---

**Próximo:** Escolha uma das otimizações acima e implemente! 🚀
