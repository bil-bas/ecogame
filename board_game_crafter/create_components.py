import os
from itertools import batched
import glob

from PyPDF2 import PdfMerger
import cairosvg

from .layout_page import layout_page
from .base_component import Face
from .utils import output_path


def create_components(component_types: list, name, show_border: bool = False, show_margin: bool = False,
                      keep_as_svg: bool = False, face: str = Face.FRONT, extra_config: dict = None) -> None:
    num_components_on_page = component_types[0].cols * component_types[0].rows

    components = []
    for component_type in component_types:
        components.extend(component_type.create_components(extra_config))

    if face == Face.TEMPLATE:
        components = components[:num_components_on_page]

    for i, components_on_page in enumerate(batched(components, num_components_on_page), 1):
        doc = layout_page(components_on_page, show_border=show_border, show_margin=show_margin, face=face)
        if keep_as_svg:
            output_file = output_path(f"{name}.svg")
            doc.save_svg(output_file)
            print(f"Written {len(components)} components to {output_file}")
        else:
            cairosvg.svg2pdf(doc.as_svg(), write_to=output_path(f"{name}_{i:02}.pdf"))

    if not keep_as_svg:
        merge_pdfs(len(components), name)

        for filename in glob.glob(output_path(f"{name}_*.pdf")):
            os.remove(filename)


def merge_pdfs(num_components, name):
    output_file = output_path(f"{name}.pdf")

    with PdfMerger() as merger:
        for pdf in sorted(glob.glob(output_path(f"{name}_*.pdf"))):
            merger.append(pdf)

        merger.write(output_file)

    print(f"Written {num_components} components to {output_file}")