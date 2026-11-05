"""
Translate the text files made by Extraction.py (option 1) with DeepL.

Only text lines are sent; the "###" marker lines that gsspt needs to rebuild
the .spt file are copied unchanged. The previous lines are sent as DeepL
`context`, which improves pronouns and tone.

Usage:
    export DEEPL_API_KEY=xxxxxxxx:fx
    python translate_files_deepl.py scripts_repaired/ scripts_translated/ [--lang EN-US]

Note: for new projects, VNTools (https://github.com/abunomaru/VNTools) reads
.spt files directly, translates with speaker-aware context (Claude, OpenAI,
local models or DeepL) and re-inserts text of any length.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

BATCH = 50


def deepl_translate(texts, api_key, target_lang, context=''):
    host = 'api-free.deepl.com' if api_key.endswith(':fx') else 'api.deepl.com'
    body = {'text': texts, 'source_lang': 'JA', 'target_lang': target_lang,
            'preserve_formatting': True}
    if context:
        body['context'] = context
    req = urllib.request.Request(
        f'https://{host}/v2/translate', data=json.dumps(body).encode('utf-8'),
        headers={'Authorization': f'DeepL-Auth-Key {api_key}',
                 'Content-Type': 'application/json'},
        method='POST')
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return [t['text'] for t in json.loads(resp.read())['translations']]
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 5:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f'DeepL error {e.code}: {e.read().decode("utf-8", "replace")}')


def translate_file(input_file, output_file, api_key, target_lang):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    todo = [i for i, line in enumerate(lines) if line.strip() and not line.startswith('###')]
    out = list(lines)
    for start in range(0, len(todo), BATCH):
        idx = todo[start:start + BATCH]
        context = '\n'.join(lines[i] for i in todo[max(0, start - 5):start])
        for i, text in zip(idx, deepl_translate([lines[i] for i in idx], api_key, target_lang, context)):
            out[i] = text

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print(f'{os.path.basename(input_file)}: {len(todo)} lines')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('input_dir')
    ap.add_argument('output_dir')
    ap.add_argument('--lang', default='EN-US', help='DeepL target language code (default EN-US)')
    ap.add_argument('--api-key', default=os.environ.get('DEEPL_API_KEY', ''))
    args = ap.parse_args()
    if not args.api_key:
        sys.exit('Set DEEPL_API_KEY or pass --api-key')

    os.makedirs(args.output_dir, exist_ok=True)
    for name in sorted(os.listdir(args.input_dir)):
        if name.endswith('.txt'):
            translate_file(os.path.join(args.input_dir, name), os.path.join(args.output_dir, name),
                           args.api_key, args.lang)


if __name__ == '__main__':
    main()
