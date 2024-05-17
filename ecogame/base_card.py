import textwrap

import drawsvg as svg

from .utils import mm_to_px


class BaseCard:
    FONT_HEIGHT_TITLE = 24
    FONT_HEIGHT_VALUE = 34
    FONT_HEIGHT_TEXT = 20
    FONT_HEIGHT_KEYWORDS = 12
    FONT_HEIGHT_FLAVOUR = 12
    FONT_HEIGHT_COST = 18
    FONT_HEIGHT_COUNT = 12

    BACKGROUND_COLOR = (255, 255, 255, 255)
    INK_COLOR = (0, 0, 0, 255)

    UNIT_SIZE = FONT_HEIGHT_VALUE, FONT_HEIGHT_VALUE
    TEXT_ICON_SPACING = 2

    WIDTH, HEIGHT = None, None
    COLS, ROWS = None, None

    BLEED_MARGIN = mm_to_px(1.5)
    BLEED_WIDTH = BLEED_HEIGHT = None
    MARGIN_LEFT = MARGIN_RIGHT = MARGIN_TOP = MARGIN_BOTTOM = None
    INNER_WIDTH = INNER_HEIGHT = None
    BACK_LABEL = "Improvement"

    ROTATE = False

    BACK_BORDER_COLOR = "#555555"
    BACK_BACKGROUND_COLOR = "white"
    BACK_BORDER_WIDTH = mm_to_px(10)
    BACK_FONT_HEIGHT_TITLE = 32
    BACK_FONT_HEIGHT_TYPE = 20

    def __init__(self, **config: hash):
        self._count = config.pop("count", 1)
        self._config = config
        self._is_blank = self._config.pop("is_blank", False)

    def _value(self, value: str, size: int, x: int, y: int, right_justify: bool = False):
        if value.endswith("P"):
            icon = "pollution"
            value = value[:-1]
        elif value.endswith("$"):
            icon = "prosperity"
            value = value[:-1]
        else:
            icon = None

        if right_justify:
            text_anchor = "end"
            icon_x = x - size
            text_x = icon_x - self.TEXT_ICON_SPACING
        else:
            text_anchor = "start"
            text_x = x
            icon_x = x + len(value) * size * 0.7 + self.TEXT_ICON_SPACING

        yield svg.Text(value, size, text_x, y + size, text_anchor=text_anchor, font_weight="bold")

        if icon:
            yield self._image(icon_x, y + size * 0.2, size * 0.8, icon)

    def _wrap(self, text: str, size: int, x: int, y: int, width: int, valign: str = "top") -> svg.Text:
        if width == 0:
            lines = text.split("\n")
        else:
            lines = textwrap.wrap(text, width)

        height = (size + 2) * (len(lines) - 1)

        if valign == "top":
            offset = 0
        elif valign == "middle":
            offset = -height // 2
        elif valign == "bottom":
            offset = -height
        else:
            raise

        return svg.Text("\n".join(lines), size, x, y + offset)

    @staticmethod
    def _image(x: float, y: float, size: float, name: str) -> svg.Image:
        return svg.Image(x, y, size, size, path=f"./images/{name}.png", embed=True)

    @property
    def count(self) -> int:
        return self._count

    def render_front(self):
        if self._is_blank:
            return

        yield from self._render_front(**self._config)

    def render_back(self):
        if self._is_blank:
            return

        yield from self._render_back(**self._config)

    def _render_front(self, **config):
        raise NotImplementedError

    def _render_back(self, **config):
        yield svg.Rectangle(-self.BLEED_MARGIN, -self.BLEED_MARGIN, self.BLEED_WIDTH, self.BLEED_HEIGHT,
                            fill=self.BACK_BORDER_COLOR, stroke="none")

        yield svg.Rectangle(self.MARGIN_LEFT, self.MARGIN_TOP, self.INNER_WIDTH, self.INNER_HEIGHT,
                            stroke="none", fill=self.BACK_BACKGROUND_COLOR)

        yield svg.Text("ECOGAME", self.BACK_FONT_HEIGHT_TITLE, self.WIDTH / 2, self.HEIGHT / 2,
                       center=True)

        yield svg.Text(self.BACK_LABEL, self.BACK_FONT_HEIGHT_TYPE, self.WIDTH / 2, self.HEIGHT / 2 + 40,
                       center=True)

    @property
    def width(self) -> float:
        return self.WIDTH

    @property
    def height(self) -> float:
        return self.HEIGHT


class PortraitCard(BaseCard):
    WIDTH, HEIGHT = mm_to_px(63.5), mm_to_px(88.9)
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(5), mm_to_px(5)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(5), mm_to_px(5)
    INNER_WIDTH = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    INNER_HEIGHT = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    BLEED_WIDTH = WIDTH + BaseCard.BLEED_MARGIN * 2
    BLEED_HEIGHT = HEIGHT + BaseCard.BLEED_MARGIN * 2
    ROTATE = True
    COLS, ROWS = 2, 4


class LandscapeCard(BaseCard):
    WIDTH, HEIGHT = mm_to_px(88.9), mm_to_px(63.5)
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(5), mm_to_px(5)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(5), mm_to_px(5)
    INNER_WIDTH = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    INNER_HEIGHT = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    BLEED_WIDTH = WIDTH + BaseCard.BLEED_MARGIN * 2
    BLEED_HEIGHT = HEIGHT + BaseCard.BLEED_MARGIN * 2
    COLS, ROWS = 2, 4