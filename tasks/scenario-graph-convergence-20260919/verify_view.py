"""Check the offline graph document in an available local Chromium browser."""
from pathlib import Path
import json,time,shutil,os
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
start=time.perf_counter();errors=[];requests=[]
chrome=os.environ.get('CHROME_BIN') or shutil.which('chromium') or shutil.which('google-chrome')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,**({'executable_path':chrome} if chrome else {}))
 page=b.new_page(viewport={'width':1300,'height':1100})
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('request',lambda r:requests.append(r.url))
 page.set_content((root/'GRAPH-EXPLORER.html').read_text(), wait_until='load')
 svg=page.locator('svg').count();questions=page.locator('.question').count();families=page.locator('.family').count()
 page.screenshot(path=str(root/'graph-desktop.png'),full_page=False)
 page.locator('#search').fill('M02');found=page.locator('#q-M02').is_visible()
 page.locator('#clear').click();page.evaluate("location.hash='q-M02'");page.wait_for_function("document.getElementById('q-M02').open")
 expanded=page.locator('#q-M02').get_attribute('open') is not None
 page.set_viewport_size({'width':390,'height':844});page.evaluate("location.hash='';window.scrollTo(0,0)")
 overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth')
 page.screenshot(path=str(root/'graph-mobile.png'),full_page=False)
 duplicate=page.evaluate('(()=>{const a=[...document.querySelectorAll("[id]")].map(e=>e.id);return a.length-new Set(a).size})()')
 b.close()
checks={'svg_graphs':svg==30,'question_entries':questions==79,'families':families==28,'search_found_M02':found,'hash_navigation_expanded_question':expanded,'no_mobile_page_overflow':not overflow,'unique_dom_ids':duplicate==0,'no_page_errors':not errors,'no_network_requests':not any(x.startswith(('http:','https:')) for x in requests)}
result={'kind':'offline graph presentation, not survey runtime','load_method':'exact artifact HTML via set_content; browser file-URL navigation is administrator-blocked' ,'checks':checks,'passed':sum(checks.values()),'failed':len(checks)-sum(checks.values()),'page_errors':errors,'elapsed_seconds':round(time.perf_counter()-start,3),'browser':chrome or 'playwright-default','model_calls':0}
(root/'VIEW-CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
