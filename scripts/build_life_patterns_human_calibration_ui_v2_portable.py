#!/usr/bin/env python3
"""Build the verified offline Life Patterns calibration UI with a SHA-256 fallback.

The underlying v2 UI builder remains authoritative for handoff verification and embedding. This
wrapper applies one narrowly bounded runtime-portability transformation: if WebCrypto is not
available in the local browser context, the UI can still verify the same SHA-256 content
addresses using a self-contained pure-JavaScript implementation. No measurement semantics,
private evidence, response contract, or network behavior changes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from build_life_patterns_human_calibration_ui_v2 import (
    build_standalone_human_calibration_ui_v2,
)

STRICT_SHA256_JS = (
    'async function sha256Hex(bytes){if(!crypto||!crypto.subtle)throw new Error('
    '"This browser does not provide the local cryptographic verifier required by this '
    'calibration UI.");const d=await crypto.subtle.digest("SHA-256",bytes);return '
    '[...new Uint8Array(d)].map(x=>x.toString(16).padStart(2,"0")).join("")}'
)

PORTABLE_SHA256_JS = '''function sha256Fallback(bytes){const K=new Uint32Array([1116352408,1899447441,3049323471,3921009573,961987163,1508970993,2453635748,2870763221,3624381080,310598401,607225278,1426881987,1925078388,2162078206,2614888103,3248222580,3835390401,4022224774,264347078,604807628,770255983,1249150122,1555081692,1996064986,2554220882,2821834349,2952996808,3210313671,3336571891,3584528711,113926993,338241895,666307205,773529912,1294757372,1396182291,1695183700,1986661051,2177026350,2456956037,2730485921,2820302411,3259730800,3345764771,3516065817,3600352804,4094571909,275423344,430227734,506948616,659060556,883997877,958139571,1322822218,1537002063,1747873779,1955562222,2024104815,2227730452,2361852424,2428436474,2756734187,3204031479,3329325298]);const H=new Uint32Array([1779033703,3144134277,1013904242,2773480762,1359893119,2600822924,528734635,1541459225]);const n=bytes.length,padded=((n+9+63)>>6)<<6,data=new Uint8Array(padded);data.set(bytes);data[n]=128;const dv=new DataView(data.buffer),bits=n*8;dv.setUint32(padded-8,Math.floor(bits/4294967296),false);dv.setUint32(padded-4,bits>>>0,false);const w=new Uint32Array(64),rotr=(x,n)=>(x>>>n)|(x<<(32-n));for(let off=0;off<padded;off+=64){for(let i=0;i<16;i++)w[i]=dv.getUint32(off+i*4,false);for(let i=16;i<64;i++){const a=w[i-15],b=w[i-2],s0=rotr(a,7)^rotr(a,18)^(a>>>3),s1=rotr(b,17)^rotr(b,19)^(b>>>10);w[i]=(w[i-16]+s0+w[i-7]+s1)>>>0}let[a,b,c,d,e,f,g,h]=H;for(let i=0;i<64;i++){const S1=rotr(e,6)^rotr(e,11)^rotr(e,25),ch=(e&f)^((~e)&g),t1=(h+S1+ch+K[i]+w[i])>>>0,S0=rotr(a,2)^rotr(a,13)^rotr(a,22),maj=(a&b)^(a&c)^(b&c),t2=(S0+maj)>>>0;h=g;g=f;f=e;e=(d+t1)>>>0;d=c;c=b;b=a;a=(t1+t2)>>>0}H[0]=(H[0]+a)>>>0;H[1]=(H[1]+b)>>>0;H[2]=(H[2]+c)>>>0;H[3]=(H[3]+d)>>>0;H[4]=(H[4]+e)>>>0;H[5]=(H[5]+f)>>>0;H[6]=(H[6]+g)>>>0;H[7]=(H[7]+h)>>>0}return[...H].map(x=>x.toString(16).padStart(8,"0")).join("")}
async function sha256Hex(bytes){if(globalThis.crypto&&crypto.subtle){const d=await crypto.subtle.digest("SHA-256",bytes);return[...new Uint8Array(d)].map(x=>x.toString(16).padStart(2,"0")).join("")}return sha256Fallback(bytes)}'''


def patch_html_for_portable_sha256(html: str) -> str:
    """Replace exactly one strict WebCrypto gate and fail closed on template drift."""

    occurrences = html.count(STRICT_SHA256_JS)
    if occurrences != 1:
        raise ValueError(
            "offline calibration UI SHA-256 portability patch expected exactly one strict gate; "
            f"found {occurrences}"
        )
    patched = html.replace(STRICT_SHA256_JS, PORTABLE_SHA256_JS, 1)
    if patched.count("function sha256Fallback") != 1:
        raise ValueError("offline calibration UI SHA-256 fallback injection failed")
    return patched


def build_portable_standalone_human_calibration_ui_v2(
    handoff_zip: str | Path,
    output_html: str | Path,
    *,
    overwrite: bool = False,
) -> dict[str, Any]:
    """Build the exact verified UI, then apply only the bounded SHA-256 fallback patch."""

    output = Path(output_html)
    if output.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output}")

    with tempfile.TemporaryDirectory(prefix="life-patterns-ui-v2-") as temporary:
        intermediate = Path(temporary) / "verified-ui.html"
        base_receipt = build_standalone_human_calibration_ui_v2(
            handoff_zip,
            intermediate,
        )
        html = intermediate.read_text(encoding="utf-8")

    patched = patch_html_for_portable_sha256(html)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(patched, encoding="utf-8", newline="\n")
    raw_output = output.read_bytes()

    receipt = dict(base_receipt)
    receipt.update(
        schema_version="life-patterns-human-calibration-ui-portable-build-receipt-v2",
        output_html_sha256=hashlib.sha256(raw_output).hexdigest(),
        output_html_bytes=len(raw_output),
        native_webcrypto_preferred=True,
        pure_javascript_sha256_fallback_available=True,
        measurement_semantics_changed=False,
        response_contract_changed=False,
        network_requests_required=False,
        automated_judgment_used=False,
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff-zip", type=Path, required=True)
    parser.add_argument("--output-html", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    receipt = build_portable_standalone_human_calibration_ui_v2(
        args.handoff_zip,
        args.output_html,
        overwrite=args.overwrite,
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
