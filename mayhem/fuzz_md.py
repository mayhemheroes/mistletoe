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
    choice = fdp.ConsumeIntInRange(0, 2)
    if choice == 0:
        with fdp.ConsumeMemoryFile(all_data=True, as_bytes=False) as fin:
            mistletoe.markdown(fin)
    if choice == 1:
        with fdp.ConsumeMemoryFile(all_data=True, as_bytes=False) as fin:
            mistletoe.markdown(fin, LaTeXRenderer)
    if choice == 2:
        with fdp.ConsumeMemoryFile(all_data=True, as_bytes=False) as fin:
            with HTMLRenderer() as renderer:
                doc = Document(fin)
                renderer.render(doc)
def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
