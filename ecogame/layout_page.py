import drawsvg as svg

from .utils import A4_WIDTH, A4_HEIGHT, mm_to_px

MARGIN = mm_to_px(10)
SPACING = mm_to_px(5)
REG_MARGIN = mm_to_px(5)
REG_LEFT, REG_TOP = REG_MARGIN, REG_MARGIN
REG_LEN, REG_WIDTH = mm_to_px(5), 4
REG_RIGHT = A4_WIDTH - REG_MARGIN

COLOR_BORDER = "grey"
COLOR_REG = "red"
COLOR_MARGIN = "lightgrey"


def layout_page(cards: list, show_border: bool, show_margin: bool, render_backs: bool):
    draw = svg.Drawing(A4_WIDTH, A4_HEIGHT, origin="top-left")

    cols, rows = cards[0].COLS, cards[0].ROWS

    if cards[0].ROTATE:
        width, height = cards[0].height, cards[0].width
        rotation = f", translate(0, {height}) rotate({-90})"
    else:
        width, height = cards[0].width, cards[0].height
        rotation = ""

    # Ensure we center any cards.
    render_width = cols * width + (cols - 1) * SPACING
    render_offset_y = (A4_WIDTH - render_width) / 2

    page = svg.Group()

    render_area = svg.Group(transform=f"translate({render_offset_y}, {MARGIN})")
    reg_bottom = render_cards(cards=cards, cols=cols, draw=render_area, height=height, rotation=rotation, rows=rows,
                              show_border=show_border, show_margin=show_margin, width=width, render_backs=render_backs)
    page.append(render_area)

    reg_bottom += MARGIN * 2 - REG_MARGIN

    page.extend(reg_mark(REG_LEFT, REG_TOP, left=True, top=True))
    page.extend(reg_mark(REG_RIGHT, REG_TOP, left=False, top=True))
    page.extend(reg_mark(REG_LEFT, reg_bottom, left=True, top=False))
    page.extend(reg_mark(REG_RIGHT, reg_bottom, left=False, top=False))

    draw.append(page)

    return draw


def render_cards(cards: list, cols: int, draw, height: int, rotation: str, rows: int, show_border: bool,
                 show_margin: bool, width: int, render_backs: bool):
    top = None

    for row in range(rows):
        for col in range(cols):
            index = row * cols + col

            # Flip backs the other way around so they line up with the fronts when printed double-sided.
            if render_backs:
                left = (cols - 1 - col) * (width + SPACING)
            else:
                left = col * (width + SPACING)

            top = row * (height + SPACING)

            try:
                card = cards[index]
            except IndexError:
                return top - SPACING

            group = svg.Group(transform=f"translate({left}, {top}) {rotation}")

            group.extend(card.render_back() if render_backs else card.render_front())

            if show_border:
                group.append(svg.Rectangle(0, 0, card.width, card.height, stroke=COLOR_BORDER, fill="none"))

            if show_margin:
                group.append(svg.Rectangle(card.MARGIN_LEFT, card.MARGIN_TOP, card.INNER_WIDTH, card.INNER_HEIGHT,
                                           stroke=COLOR_MARGIN, fill="none"))

            draw.append(group)

    return top + height


def reg_mark(x: float, y: float, left: bool, top: bool):
    yield svg.Line(x, y, x + REG_LEN * (1 if left else -1), y, stroke=COLOR_REG)
    yield svg.Line(x, y, x, y + REG_LEN * (1 if top else -1), stroke=COLOR_REG)
