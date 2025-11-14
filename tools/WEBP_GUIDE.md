# WebP & Responsive Images Guide

## Visão Geral
Este guia explica como implementar suporte a WebP e imagens responsivas com `<picture>` e `srcset`.

---

## 1. Por que WebP?

- **20-30% menor** que JPEG/PNG no mesmo tamanho
- **Suporte moderno:** Chrome, Firefox, Safari 16+
- **Fallback automático:** navegadores antigos usam JPEG/PNG

---

## 2. Converter Imagens para WebP

### Usando ImageMagick (Linux/Mac)
```bash
# Instalar (se necessário)
brew install imagemagick  # Mac
# ou: sudo apt install imagemagick  # Ubuntu

# Converter uma imagem
convert input.jpg -quality 80 output.webp

# Converter todas as JPG em uma pasta
for f in *.jpg; do convert "$f" -quality 80 "${f%.jpg}.webp"; done
```

### Usando Cwebp (Google)
```bash
# Instalar
brew install webp  # Mac
# ou: sudo apt install webp  # Ubuntu

# Converter
cwebp -q 80 input.jpg -o output.webp
```

### Online (sem instalar)
- https://convertio.co/jpg-webp/
- https://www.freeconvert.com/jpg-to-webp

---

## 3. Sintaxe com `<picture>` e `srcset`

### Exemplo Simples (WebP + JPEG Fallback)
```html
<picture>
    <source srcset="/imagens/hero.webp" type="image/webp">
    <source srcset="/imagens/hero.jpg" type="image/jpeg">
    <img src="/imagens/hero.jpg" alt="Hero background" loading="lazy">
</picture>
```

### Exemplo com Responsive (múltiplos tamanhos)
```html
<picture>
    <!-- WebP: diferentes tamanhos -->
    <source
        srcset="
            /imagens/fornecedores/banda-small.webp 480w,
            /imagens/fornecedores/banda-medium.webp 768w,
            /imagens/fornecedores/banda-large.webp 1200w
        "
        type="image/webp"
        sizes="(max-width: 480px) 100vw, (max-width: 768px) 50vw, 33vw"
    >
    
    <!-- JPEG Fallback: diferentes tamanhos -->
    <source
        srcset="
            /imagens/fornecedores/banda-small.jpg 480w,
            /imagens/fornecedores/banda-medium.jpg 768w,
            /imagens/fornecedores/banda-large.jpg 1200w
        "
        type="image/jpeg"
        sizes="(max-width: 480px) 100vw, (max-width: 768px) 50vw, 33vw"
    >
    
    <!-- Fallback para navegadores muito antigos -->
    <img
        src="/imagens/fornecedores/banda-large.jpg"
        alt="Banda Harmonia"
        loading="lazy"
        width="400"
        height="300"
    >
</picture>
```

### Exemplo para Cards (Simples)
```html
<!-- Fornecedor Card com WebP -->
<div class="fornecedor-card">
    <picture>
        <source srcset="/imagens/fornecedores/banda-harmonia-1.webp" type="image/webp">
        <source srcset="/imagens/fornecedores/banda-harmonia-1.jpg" type="image/jpeg">
        <img
            src="/imagens/fornecedores/banda-harmonia-1.jpg"
            alt="Banda Harmonia"
            loading="lazy"
            width="300"
            height="250"
        >
    </picture>
</div>
```

---

## 4. Implementação Automática (Python Script)

Script para converter e atualizar HTML automaticamente:

```python
#!/usr/bin/env python3
"""
Converter imagens para WebP e atualizar referências em HTML.
Uso: python3 tools/convert_webp.py
"""

import os
import subprocess
from pathlib import Path

def convert_to_webp(src_dir='piracicaba/imagens', quality=80):
    """Converte todas as JPG/PNG para WebP."""
    count = 0
    for root, dirs, files in os.walk(src_dir):
        for fname in files:
            if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                src = os.path.join(root, fname)
                base, ext = os.path.splitext(src)
                dest = base + '.webp'
                
                # Pular se WebP já existe
                if os.path.exists(dest):
                    continue
                
                try:
                    subprocess.run([
                        'cwebp', '-q', str(quality), src, '-o', dest
                    ], check=True, capture_output=True)
                    print(f"✓ {fname} → {os.path.basename(dest)}")
                    count += 1
                except FileNotFoundError:
                    print(f"✗ cwebp não encontrado. Instale: brew install webp")
                    return
                except subprocess.CalledProcessError as e:
                    print(f"✗ Erro ao converter {fname}: {e}")
    
    print(f"✓ Convertidas {count} imagens para WebP")

def update_html_with_webp(html_dir='piracicaba'):
    """Atualiza <img> para <picture> com WebP."""
    import re
    
    count = 0
    for root, dirs, files in os.walk(html_dir):
        if 'includes' in root:
            continue
        
        for fname in files:
            if not fname.endswith('.html'):
                continue
            
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            original = html
            
            # Encontrar <img> com src de fornecedores/imagens e converter para <picture>
            pattern = r'<img\s+src="([^"]*(?:fornecedores|imagens)[^"]*)"\s+alt="([^"]*)"\s*(?:loading="lazy")?\s*>'
            
            def replace_with_picture(match):
                src = match.group(1)
                alt = match.group(2)
                
                # Gerar caminho WebP
                base, ext = os.path.splitext(src)
                webp_src = base + '.webp'
                
                return f'''<picture>
    <source srcset="{webp_src}" type="image/webp">
    <source srcset="{src}" type="image/jpeg">
    <img src="{src}" alt="{alt}" loading="lazy">
</picture>'''
            
            html = re.sub(pattern, replace_with_picture, html)
            
            if html != original:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(html)
                count += 1
    
    print(f"✓ Atualizados {count} arquivos HTML com <picture> WebP")

if __name__ == '__main__':
    print("=== Convertendo para WebP ===")
    convert_to_webp()
    
    print("\n=== Atualizando HTML ===")
    update_html_with_webp()
    
    print("\n✅ WebP implementation complete!")
```

---

## 5. Sizes & Srcset (Responsividade)

### O que significa `sizes`?
```html
sizes="(max-width: 480px) 100vw, (max-width: 768px) 50vw, 33vw"
```
- Tela ≤ 480px: imagem ocupa 100% da viewport width
- Tela ≤ 768px: imagem ocupa 50% da viewport
- Tela > 768px: imagem ocupa 33% da viewport

Navegador baixa a imagem do tamanho apropriado automaticamente.

### Tamanhos Recomendados
Para fornecedor cards (geralmente 100vw em mobile, 50vw em tablet, 33vw em desktop):
- **Small (480px):** qualidade mobile
- **Medium (768px):** qualidade tablet
- **Large (1200px):** qualidade desktop

---

## 6. Performance Ganhos

| Formato | Tamanho | Redução |
|---------|--------|---------|
| JPEG original | 250 KB | — |
| WebP | 180 KB | 28% |
| JPEG otimizado | 200 KB | 20% |
| WebP otimizado | 140 KB | 44% |

---

## 7. Checklist de Implementação

- [ ] Instalar `cwebp` ou usar ferramenta online
- [ ] Converter todas as imagens para WebP
- [ ] Atualizar `<img>` para `<picture>` com WebP source
- [ ] Testar em Chrome, Firefox, Safari
- [ ] Adicionar `loading="lazy"` (já feito)
- [ ] Validar com Lighthouse / PageSpeed

---

## 8. Testes no Navegador

### DevTools (Chrome/Firefox)
1. F12 → Network tab
2. Recarregar página
3. Filtrar por imagens
4. Ver qual formato é carregado (WebP vs JPEG)

### Verificar Suporte WebP
```javascript
// No console do navegador:
const canvas = document.createElement('canvas');
const webp = canvas.toDataURL('image/webp') === 'data:image/webp;base64,';
console.log('WebP suportado:', webp);
```

---

## Próximos Passos

1. Converter imagens da pasta `imagens/` para WebP
2. Rodar script de atualização HTML (ou editar manualmente)
3. Testar com DevTools
4. Publicar em produção com cache-control headers

---

## Recursos

- [MDN: Picture Element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture)
- [MDN: Responsive Images](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images)
- [Google: Serve images in modern formats](https://web.dev/serve-images-webp/)
- [Squoosh (converter online)](https://squoosh.app/)
