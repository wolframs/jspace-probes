"""Headless UI check with explicitly synthetic, temporary participant data."""
import functools
import hashlib
import http.server
import json
import shutil
import tempfile
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

from folk01 import ROOT, write
from folk01_ratings import validate


def check():
    with tempfile.TemporaryDirectory(prefix='folk01-ui-') as td:
        folder=Path(td);shutil.copyfile(ROOT/'probes/folk01_rating.html',folder/'rate.html')
        packets=[];key={}
        for code,definitions,exposure in [('TESTFULL','unaided','full'),('TESTSHRT','supplied','first')]:
            turns=[dict(turn=i,user='Synthetic user: <script>window.injected=true</script>',response='Synthetic assistant response. *smiles*',capped=i==3) for i in range(1,9 if exposure=='full' else 2)]
            packet=dict(code=code,definitions=definitions,exposure=exposure,pairs=[dict(pair_id=f'{code}-{i+1}',A=turns,B=turns) for i in range(2)])
            packet['packet_id']=hashlib.sha256(json.dumps(packet,sort_keys=True).encode()).hexdigest()
            write(folder/'assignments'/f'{code}.json',packet);packets.append(packet)
            key[code]=dict(**packet)
        handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(folder))
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        screenshots=ROOT/'out/folk01-ui';screenshots.mkdir(parents=True,exist_ok=True)
        try:
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path='/home/wolfram/.cache/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-linux64/chrome-headless-shell',headless=True,args=['--disable-gpu'])
                page=browser.new_page(viewport=dict(width=1280,height=900));errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                url=f'http://127.0.0.1:{server.server_port}/rate.html'
                for packet in packets:
                    page.goto(url);page.locator('#code').fill(packet['code']);page.locator('#load').click()
                    page.locator('#intro').wait_for(state='visible')
                    if packet['definitions']=='unaided':
                        page.locator('#meaning_flattened').fill('Synthetic unchanged responses')
                        page.locator('#meaning_introverted').fill('Synthetic quiet but responsive')
                    else:assert page.locator('#own').is_hidden()
                    page.locator('#introform button').click();page.locator('#comparison').wait_for(state='visible')
                    assert page.locator('.turn').count()==(16 if packet['exposure']=='full' else 2)
                    assert page.evaluate('typeof window.injected')=='undefined'
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                    page.screenshot(path=str(screenshots/f'{packet["code"]}-desktop.png'))
                    for index in range(2):
                        page.locator('#next').click();assert page.locator('#comparison').is_visible()
                        for field in ['flat_pair','intro_pair']:page.locator('#'+field).select_option('unknown')
                        for field in ['A_flat','A_intro','B_flat','B_intro']:page.locator('#'+field).select_option('unknown')
                        for field in ['flat_evidence','intro_evidence']:page.locator('#'+field).fill('Synthetic QA evidence only; never human data.')
                        page.locator('#next').click()
                        if index==0:
                            page.reload();page.locator('#code').fill(packet['code']);page.locator('#load').click()
                            page.locator('#comparison').wait_for(state='visible');assert page.locator('#progress').inner_text()=='Pair 2 of 2'
                    page.locator('#finish').wait_for(state='visible')
                    with page.expect_download() as download_info:page.locator('#download').click()
                    data=json.loads(Path(download_info.value.path()).read_text());validate(data,key)
                    page.locator('#clear').click();assert page.evaluate(f'localStorage.getItem("folk01:{packet["code"]}")') is None
                page.set_viewport_size(dict(width=390,height=844));page.goto(url)
                page.locator('#code').fill('TESTFULL');page.locator('#load').click();page.locator('#intro').wait_for(state='visible')
                page.locator('#meaning_flattened').fill('Synthetic unchanged responses');page.locator('#meaning_introverted').fill('Synthetic quiet but responsive')
                page.locator('#introform button').click();page.locator('#comparison').wait_for(state='visible')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                page.screenshot(path=str(screenshots/'mobile.png'))
                assert not errors,errors
                browser.close()
        finally:server.shutdown();server.server_close()
    print('PASS: exposure rendering, two-pair completion, required fields, reload recovery, JSON validation, storage removal, HTML escaping, desktop/mobile overflow. Synthetic only.')


if __name__=='__main__':check()
