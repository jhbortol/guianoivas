#!/usr/bin/env python3
"""
Build script para Guia Noivas Piracicaba.
Minifica CSS/JS e injeta Critical CSS inline.

Uso:
  python3 tools/build.py --minify     # Minificar CSS/JS
  python3 tools/build.py --critical   # Injetar CSS crítico
  python3 tools/build.py --all        # Ambas acima
"""

import os
import re
import sys
import argparse
from pathlib import Path

# Minificação básica de CSS
def minify_css(css_content):
    """Remove comentários, espaços e quebras de linha desnecessárias."""
    # Remove comentários
    css = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    # Remove espaços em excesso
    css = re.sub(r'\s+', ' ', css)
    # Remove espaços antes de { } : ;
    css = re.sub(r'\s*([{}:;,])\s*', r'\1', css)
    return css.strip()

# Minificação básica de JS
def minify_js(js_content):
    """Remove comentários e espaços desnecessários em JS."""
    # Remove comentários de linha
    js = re.sub(r'//.*?$', '', js_content, flags=re.MULTILINE)
    # Remove comentários de bloco
    js = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
    # Remove espaços em excesso (mas preserva strings)
    js = re.sub(r'\s+', ' ', js)
    # Remove espaços antes de { } ( ) ;
    js = re.sub(r'\s*([{}();,=\[\]])\s*', r'\1', js)
    return js.strip()

def minify_files(src_dir='piracicaba', dest_dir='dist'):
    """Minifica CSS e JS para diretório dist."""
    os.makedirs(dest_dir, exist_ok=True)
    
    css_dir = os.path.join(src_dir, 'css')
    js_dir = os.path.join(src_dir, 'js')
    
    os.makedirs(os.path.join(dest_dir, 'css'), exist_ok=True)
    os.makedirs(os.path.join(dest_dir, 'js'), exist_ok=True)
    
    # Minificar CSS
    for fname in os.listdir(css_dir):
        if fname.endswith('.css'):
            src = os.path.join(css_dir, fname)
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()
            
            minified = minify_css(content)
            
            # Salvar versão minificada com .min.css
            name, ext = os.path.splitext(fname)
            dest = os.path.join(dest_dir, 'css', f'{name}.min.css')
            with open(dest, 'w', encoding='utf-8') as f:
                f.write(minified)
            
            original_size = len(content)
            minified_size = len(minified)
            savings = ((original_size - minified_size) / original_size) * 100
            print(f"✓ {fname}: {original_size} → {minified_size} bytes ({savings:.1f}% reduction)")
    
    # Minificar JS
    for fname in os.listdir(js_dir):
        if fname.endswith('.js'):
            src = os.path.join(js_dir, fname)
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()
            
            minified = minify_js(content)
            
            # Salvar versão minificada com .min.js
            name, ext = os.path.splitext(fname)
            dest = os.path.join(dest_dir, 'js', f'{name}.min.js')
            with open(dest, 'w', encoding='utf-8') as f:
                f.write(minified)
            
            original_size = len(content)
            minified_size = len(minified)
            savings = ((original_size - minified_size) / original_size) * 100
            print(f"✓ {fname}: {original_size} → {minified_size} bytes ({savings:.1f}% reduction)")

def inject_critical_css(src_dir='piracicaba'):
    """Injeta Critical CSS inline em todas as páginas HTML."""
    # Ler Critical CSS
    critical_path = os.path.join(src_dir, 'css', 'critical.css')
    with open(critical_path, 'r', encoding='utf-8') as f:
        critical_css = f.read()
    
    # Minificar Critical CSS
    critical_css_minified = minify_css(critical_css)
    
    # Template para inline <style>
    inline_style = f'<style>{critical_css_minified}</style>'
    
    count = 0
    for root, dirs, files in os.walk(src_dir):
        # Skip includes e dist
        if 'includes' in root or 'dist' in root:
            continue
        
        for fname in files:
            if not fname.endswith('.html'):
                continue
            
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            # Procurar por </head> e injetar antes dele
            if '</head>' in html and '<style>' not in html:
                # Injetar antes do </head> e adicionar rel="preload" para estilo.css
                html = html.replace(
                    '</head>',
                    f'{inline_style}\n<link rel="stylesheet" href="../css/estilo.css" media="print" onload="this.media=\'all\'">\n</head>'
                )
                
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(html)
                
                count += 1
    
    print(f"✓ Injected critical CSS into {count} HTML files")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build script para Guia Noivas Piracicaba')
    parser.add_argument('--minify', action='store_true', help='Minificar CSS/JS')
    parser.add_argument('--critical', action='store_true', help='Injetar CSS crítico inline')
    parser.add_argument('--all', action='store_true', help='Executar ambas operações')
    
    args = parser.parse_args()
    
    if args.all:
        args.minify = True
        args.critical = True
    
    if args.minify:
        print("=== Minificando CSS/JS ===")
        minify_files()
    
    if args.critical:
        print("\n=== Injetando Critical CSS ===")
        inject_critical_css()
    
    if not (args.minify or args.critical or args.all):
        print("Nenhuma operação selecionada. Use --help para ver opções.")
        sys.exit(1)
    
    print("\n✅ Build concluído!")
