#!/usr/bin/env python3

import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports():
    import mistletoe
    from mistletoe import Document, HTMLRenderer
    from mistletoe.latex_renderer import LaTeXRenderer

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    with fdp.ConsumeTemporaryFile('.md', all_data=False, as_bytes=False) as fin:
        mistletoe.markdown(fin, LaTeXRenderer)
    with fdp.ConsumeTemporaryFile('.md', all_data=False, as_bytes=False) as Hfin:
        with HTMLRenderer() as renderer:
            doc = Document(Hfin)
            renderer.render((doc))

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
