import re, subprocess, sys, json
from typing import Dict

DEFAULT_IMPORTS = """
import dotli
from dotli import Dotli
"""


def execute_code(code) -> str:
    run = subprocess.run([sys.executable, '-c', DEFAULT_IMPORTS + code], capture_output=True, cwd='./src', text=True)
    if run.returncode != 0:
        print(f'code:\n{code}')
        print(f'stdout: {run.stdout}')
        print(f'stderr: {run.stderr}')
        raise ValueError()

    return (run.stdout + run.stderr).strip()


trg = re.compile(
    r'```(?P<type>python|result)'           # python or result
    r'(?:(?<=result)(?P<rtype>:\w+))?'      # result type
    r'(?P<id>\([^)]+\))?'                   # optional ID
    r'(?P<rest>.*\n?)'                      # possible typos
    r'(?P<code>[^`]+)```', re.IGNORECASE
)


template = ''
readme = ''
with open('./readme.mdt', encoding='utf-8') as f:
    template = f.read()


snips: Dict[str, str] = {}
last_id = None
slice_pos = 0

for m in trg.finditer(template):
    _type, _restype, _id, _rest, _code = m.groups()   # type: str, str, str, str, str

    if _rest.strip():
        print(f'Warning: Invalid syntax for {m}! Unprocessed part: {_rest}')

    if _type.lower() == 'python':
        code = snips.get(_id, '') if _id is not None else ''
        if code:
            code += '\n'
        snips[_id] = code + _code
        last_id = _id

        readme += template[slice_pos:m.start()] + f'```python\n{_code.rstrip()}\n```'
        slice_pos = m.end()
        continue

    if _type.lower() == 'result':
        _to_run = snips[_id if _id is not None else last_id]
        __res = execute_code(_to_run)
        # if the output is json we try to reformat it so we have pretty data structures
        if _restype and _restype[1:].lower() == 'json':
            __res = json.dumps(json.loads(__res.replace("'", '"')), indent=2).replace('"', "'")
        readme += template[slice_pos:m.start()] + f'```{_restype[1:] if _restype else ""}\n{__res}\n```'
        slice_pos = m.end()
        continue

with open('./readme.md', encoding='utf-8', mode='w') as f:
    f.write(readme)
