# menuTitle: extract xProject API Docs

from importlib import reload
import xTools4.modules.xproject
reload(xTools4.modules.xproject)

import os, ast, textwrap, inspect, types
from itertools import pairwise
from inspect import isfunction
from xTools4.modules.xproject import xProject

folder = os.path.dirname(os.getcwd())
outputPath = os.path.join(folder, '_reference', 'xproject.md')
print(outputPath)

# copied from http://davidism.com/attribute-docstrings/
def get_attr_docs(cls):
    """Get any docstrings placed after attribute assignments in a class body."""
    cls_node = ast.parse(textwrap.dedent(inspect.getsource(cls))).body[0]

    if not isinstance(cls_node, ast.ClassDef):
        raise TypeError("Given object was not a class.")

    out = {}

    # Consider each pair of nodes.
    for a, b in pairwise(cls_node.body):
        # Must be an assignment then a constant string.
        if (
            not isinstance(a, ast.Assign | ast.AnnAssign)
            or not isinstance(b, ast.Expr)
            or not isinstance(b.value, ast.Constant)
            or not isinstance(b.value.value, str)
        ):
            continue

        doc = inspect.cleandoc(b.value.value)

        if isinstance(a, ast.Assign):
            # An assignment can have multiple targets (a = b = v).
            targets = a.targets
        else:
            # An annotated assignment only has one target.
            targets = [a.target]

        for target in targets:
            # Must be assigning to a plain name.
            if not isinstance(target, ast.Name):
                continue

            out[target.id] = doc

    return out

ignoreNames = []

attrDocs = get_attr_docs(xProject)

txt = '''\
---
title     : xProject
layout    : default
permalink : /reference/xproject/
---

A Pythonic API for scripting font source data for parametric variable fonts.
{: .lead}

<span class='badge bg-warning rounded-0'>draft</span> 

<table class="table table-hover">
'''

for key, value in xProject.__dict__.items():
    if key.startswith('_'):
        continue
    txt +=  '<tr>\n'
    txt += f'<td><code>xProject.{key}</code></td>\n'

    if attrDocs.get(key):
        txt += f'<td>{attrDocs[key]}</td>\n'
    else:
        txt += f'<td>{value.__doc__}</td>\n'
    txt +=  '</tr>\n'

txt += '''\
</table>
'''

with open(outputPath, mode='w') as f:
    f.write(txt)
