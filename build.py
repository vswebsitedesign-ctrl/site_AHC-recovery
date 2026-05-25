#!/usr/bin/env python3
import json, os, shutil, sys
from datetime import datetime

def build():
    pages_path = 'data/pages.json'
    if not os.path.exists(pages_path):
        print("ERROR: pages.json not found")
        sys.exit(1)
    with open(pages_path, 'r') as f:
        pages = json.load(f)
    with open('theme/base.html', 'r') as f:
        template = f.read()
    if os.path.exists('build'):
        shutil.rmtree('build')
    os.makedirs('build')

    sitemap_urls = []
    domain = 'https://cornwallauctionhouseclearance.co.uk'

    for page in pages:
        slug = page['slug']
        content = page.get('body_content', '')
        html = template.replace('{{ content }}', content)

        # 404.html must be a file not a directory
        if slug == '404.html':
            with open('build/404.html', 'w') as f:
                f.write(html)
            continue

        out_dir = os.path.join('build', slug) if slug else 'build'
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w') as f:
            f.write(html)

        # Add to sitemap — skip utility slugs
        if slug not in ['footer', 'header', 'call-button', 'cookie-consent']:
            url = f"{domain}/{slug}/" if slug else domain
            sitemap_urls.append(url)

    # Write sitemap.xml
    today = datetime.utcnow().strftime('%Y-%m-%d')
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sitemap_urls:
        sitemap += f'  <url><loc>{url}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
    sitemap += '</urlset>'
    with open('build/sitemap.xml', 'w') as f:
        f.write(sitemap)

    # Copy index fix
    index_dir = 'build/index/index.html'
    if os.path.exists(index_dir):
        shutil.copy(index_dir, 'build/index.html')

    # Copy assets
    if os.path.exists('assets'):
        shutil.copytree('assets', 'build/assets', dirs_exist_ok=True)

    print(f"Built {len(pages)} pages")
    print(f"Sitemap: {len(sitemap_urls)} URLs")

if __name__ == '__main__':
    build()
