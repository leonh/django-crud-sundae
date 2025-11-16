#!/usr/bin/env python
"""
Script to take updated screenshots after design improvements
"""
import os
import django
from playwright.sync_api import sync_playwright

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')
django.setup()

from articles.models import Article

def take_screenshots():
    # Get the first article for detail/update/delete views
    first_article = Article.objects.first()

    if not first_article:
        print("No articles found! Please run create_sample_data.py first")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--single-process'
        ])
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        screenshots_dir = 'screenshots_after'
        os.makedirs(screenshots_dir, exist_ok=True)

        base_url = 'http://127.0.0.1:8000'

        # 1. List View (Home)
        print("Capturing: List View (After)")
        try:
            page.goto(f'{base_url}/articles/article/', wait_until='domcontentloaded', timeout=10000)
            page.wait_for_timeout(2000)
            page.screenshot(path=f'{screenshots_dir}/01_list_view_after.png', full_page=True)
            print("  ✓ Saved 01_list_view_after.png")
        except Exception as e:
            print(f"  ✗ Error: {e}")

        # 2. List View with Search
        print("Capturing: List View with Search (After)")
        try:
            page.goto(f'{base_url}/articles/article/', wait_until='domcontentloaded', timeout=10000)
            page.wait_for_timeout(1000)
            search_input = page.query_selector('input[name="q"]')
            if search_input:
                search_input.fill('Django')
                search_input.press('Enter')
                page.wait_for_timeout(2000)
                page.screenshot(path=f'{screenshots_dir}/02_list_view_search_after.png', full_page=True)
                print("  ✓ Saved 02_list_view_search_after.png")
            else:
                print("  ✗ Search input not found")
        except Exception as e:
            print(f"  ✗ Error: {e}")

        # 3. List View with Filter
        print("Capturing: List View with Filter (After)")
        try:
            page.goto(f'{base_url}/articles/article/?status=published', wait_until='domcontentloaded', timeout=10000)
            page.wait_for_timeout(2000)
            page.screenshot(path=f'{screenshots_dir}/03_list_view_filtered_after.png', full_page=True)
            print("  ✓ Saved 03_list_view_filtered_after.png")
        except Exception as e:
            print(f"  ✗ Error: {e}")

        # 4. Create View
        print("Capturing: Create View (After)")
        try:
            page.goto(f'{base_url}/articles/article/create/', wait_until='domcontentloaded', timeout=10000)
            page.wait_for_timeout(2000)
            page.screenshot(path=f'{screenshots_dir}/04_create_view_after.png', full_page=True)
            print("  ✓ Saved 04_create_view_after.png")
        except Exception as e:
            print(f"  ✗ Error: {e}")

        # 5. Detail View
        print("Capturing: Detail View (After)")
        try:
            page.goto(f'{base_url}/articles/article/{first_article.pk}/', wait_until='domcontentloaded', timeout=10000)
            page.wait_for_timeout(2000)
            page.screenshot(path=f'{screenshots_dir}/05_detail_view_after.png', full_page=True)
            print("  ✓ Saved 05_detail_view_after.png")
        except Exception as e:
            print(f"  ✗ Error: {e}")

        # 6. Update View
        print("Capturing: Update View (After)")
        try:
            page.goto(f'{base_url}/articles/article/{first_article.pk}/update/', wait_until='domcontentloaded', timeout=10000)
            page.wait_for_timeout(2000)
            page.screenshot(path=f'{screenshots_dir}/06_update_view_after.png', full_page=True)
            print("  ✓ Saved 06_update_view_after.png")
        except Exception as e:
            print(f"  ✗ Error: {e}")

        # 7. Delete View
        print("Capturing: Delete View (After)")
        try:
            page.goto(f'{base_url}/articles/article/{first_article.pk}/delete/', wait_until='domcontentloaded', timeout=10000)
            page.wait_for_timeout(2000)
            page.screenshot(path=f'{screenshots_dir}/07_delete_view_after.png', full_page=True)
            print("  ✓ Saved 07_delete_view_after.png")
        except Exception as e:
            print(f"  ✗ Error: {e}")

        browser.close()

        print(f"\n✅ Updated screenshots saved to '{screenshots_dir}/' directory")

if __name__ == '__main__':
    take_screenshots()
