# Cache Strategy & Deployment Guide

## Visão Geral
Este documento descreve a estratégia de cache para o site **Guia Noivas Piracicaba** ao publicar em produção.

---

## 1. Cache-Control Headers (Servidor Web)

Configure os seguintes headers no seu servidor (Apache `.htaccess`, Nginx, ou similar):

### HTML (Não-cacheável / Revalidação)
```
Cache-Control: public, max-age=0, must-revalidate
```
- **Razão:** Novo conteúdo pode ser publicado frequentemente; sempre validar com servidor.

### CSS & JavaScript (Cache Longo + Fingerprinting)
```
Cache-Control: public, max-age=31536000, immutable
```
- **Razão:** Assets estáticos com fingerprint (hash) mudam raramente.
- **Exemplo:** `estilo.abc123def.css` → usuário usa versão cacheada, novo build gera novo hash.

### Imagens (Cache Longo)
```
Cache-Control: public, max-age=2592000
```
- **Razão:** Imagens mudam pouco; cache por 30 dias é seguro.

### Fonts (Cache Muito Longo)
```
Cache-Control: public, max-age=31536000, immutable
```
- **Razão:** Fontes raramente mudam.

---

## 2. Implementação por Servidor

### Apache (`.htaccess`)
```apache
# HTML - sempre revalidar
<FilesMatch "\.html$">
    Header set Cache-Control "public, max-age=0, must-revalidate"
</FilesMatch>

# CSS, JS, WOFF - cache longo
<FilesMatch "\.(css|js|woff|woff2|ttf|eot)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
</FilesMatch>

# Imagens - cache 30 dias
<FilesMatch "\.(jpg|jpeg|png|gif|webp|svg|ico)$">
    Header set Cache-Control "public, max-age=2592000"
</FilesMatch>
```

### Nginx
```nginx
# HTML - sempre revalidar
location ~* \.html$ {
    add_header Cache-Control "public, max-age=0, must-revalidate";
}

# CSS, JS, WOFF - cache longo
location ~* \.(css|js|woff|woff2|ttf|eot)$ {
    add_header Cache-Control "public, max-age=31536000, immutable";
}

# Imagens - cache 30 dias
location ~* \.(jpg|jpeg|png|gif|webp|svg|ico)$ {
    add_header Cache-Control "public, max-age=2592000";
}
```

---

## 3. Fingerprinting (Quebra de Cache Automática)

Adicione hashes dos assets ao filename para invalidar cache automaticamente:

### Exemplo de Build Script (Python simples)
```python
import hashlib
import os
import shutil

def fingerprint_assets(src_dir, dest_dir):
    """Copia assets e adiciona hash ao filename."""
    for fname in os.listdir(src_dir):
        if fname.endswith(('.css', '.js')):
            src = os.path.join(src_dir, fname)
            with open(src, 'rb') as f:
                hash_digest = hashlib.md5(f.read()).hexdigest()[:8]
            
            # Exemplo: estilo.css -> estilo.abc123def.css
            name, ext = os.path.splitext(fname)
            new_fname = f"{name}.{hash_digest}{ext}"
            dest = os.path.join(dest_dir, new_fname)
            
            shutil.copy2(src, dest)
            print(f"Fingerprinted: {fname} -> {new_fname}")

fingerprint_assets('css', 'dist/css')
fingerprint_assets('js', 'dist/js')
```

### Atualizar referências em HTML
Depois de fazer fingerprinting, atualizar os `<link>` e `<script>` para apontar aos novos filenames.

---

## 4. Versioning com Git

Recomendação: colocar artifacts (CSS/JS fingerprinted) no `.gitignore` e apenas fazer build na CI/CD.

```gitignore
# Fingerprinted assets (rebuild na CI/CD)
dist/
*.min.css
*.min.js
```

---

## 5. Checklist de Publicação

- [ ] Adicionar headers de cache-control no servidor
- [ ] (Opcional) Implementar fingerprinting se usar build automation
- [ ] Testar cache com DevTools: abrir página → F12 → Network → verificar `Cache-Control` header
- [ ] Verificar que HTML sempre traz conteúdo fresco (`max-age=0`)
- [ ] Confirmar que CSS/JS/imagens têm cache longo
- [ ] Configurar HTTPS + `Strict-Transport-Security` (bonus)

---

## 6. Teste Local (Simulação)

Use o Python HTTP server com headers customizados (apenas para simulação):

```python
from http.server import SimpleHTTPRequestHandler, HTTPServer

class CacheControlHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        if self.path.endswith('.html'):
            self.send_header('Cache-Control', 'public, max-age=0, must-revalidate')
        elif self.path.endswith(('.css', '.js', '.woff', '.woff2')):
            self.send_header('Cache-Control', 'public, max-age=31536000, immutable')
        elif self.path.endswith(('.jpg', '.png', '.gif', '.webp')):
            self.send_header('Cache-Control', 'public, max-age=2592000')
        super().end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), CacheControlHandler)
    print("Serving with cache-control headers on http://localhost:8000")
    server.serve_forever()
```

Salvar como `tools/test_server_with_cache.py` e rodar:
```bash
cd /workspaces/guianoivas/piracicaba
python3 ../tools/test_server_with_cache.py
```

---

## 7. Recursos Úteis

- [MDN: Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)
- [Web Vitals: LCP (Largest Contentful Paint)](https://web.dev/lcp/)
- [Google PageSpeed Insights](https://pagespeed.web.dev/)

---

## Próximos Passos

1. **Implementar no servidor:** adicionar headers `Cache-Control` (ver seção 2).
2. **(Opcional) Fingerprinting:** usar script Python ou ferramenta como `esbuild` / `parcel`.
3. **Testar:** verificar headers com `curl -i https://seu-dominio.com/index.html | grep Cache-Control`.
4. **Monitorar:** usar Google Lighthouse ou WebPageTest para validar performance.
