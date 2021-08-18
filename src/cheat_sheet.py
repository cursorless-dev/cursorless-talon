from talon import Module, ui, registry, skia, actions, cron
from talon.canvas import Canvas
import re
import webbrowser
import math
from .actions.actions import ACTION_LIST_NAMES

mod = Module()
mod.mode("cursorless_cheat_sheet", "Mode for showing cursorless cheat sheet gui")
cheat_sheet = None

instructions_url = "https://github.com/pokey/cursorless-talon/tree/master/docs"
instructions_text = "Full docs"
line_height = 34
outer_padding = 27
text_size = 16
url_text_size = 30
close_size = 24
header_size = 22
padding = 4

command_font = "monospace"
text_font = ""

background_color = "fafafa"
border_color = "000000"
text_color = "444444"
header_color = "000000"
command_background_color = "e9e9e9"
command_text_color = "282828"
url_color = "0046c9"


class CheatSheet:
    def __init__(self):
        self.need_resize = True
        self.resize_job = None
        self.last_mouse_pos = None
        # Initializes at minimum size we can calculate and set correct size later
        self.canvas = Canvas(0, 0, 1, 1)
        self.canvas.blocks_mouse = True
        self.canvas.register("draw", self.draw)
        self.canvas.register("mouse", self.mouse)
        self.canvas.freeze()

    def close(self):
        self.canvas.unregister("draw", self.draw)
        self.canvas.unregister("mouse", self.mouse)
        self.canvas.close()

    def debounce_resize(self, width: int, height: int):
        cron.cancel(self.resize_job)
        self.resize_job = cron.after("50ms", lambda: self.resize(width, height))

    def resize(self, width: int, height: int):
        if not self.need_resize:
            return
        self.need_resize = False
        screen = ui.main_screen()
        rect = ui.Rect(
            screen.x + (screen.width - width) / 2,
            screen.y + (screen.height - height) / 2,
            width,
            height,
        )
        self.canvas.set_rect(rect)

    def mouse(self, e):
        if e.event == "mousedown" and e.button == 0:
            self.last_mouse_pos = e.gpos
        elif e.event == "mousemove" and self.last_mouse_pos:
            diff_x = e.gpos.x - self.last_mouse_pos.x
            diff_y = e.gpos.y - self.last_mouse_pos.y
            self.last_mouse_pos = e.gpos
            self.canvas.move(self.canvas.rect.x + diff_x, self.canvas.rect.y + diff_y)
        elif e.event == "mouseup" and e.button == 0:
            self.last_mouse_pos = None
            if is_in_rect(self.canvas, e.gpos, get_close_rect(self.canvas)):
                actions.user.cursorless_cheat_sheet_toggle()
            elif is_in_rect(self.canvas, e.gpos, self.url_rect):
                actions.user.cursorless_cheat_sheet_toggle()
                actions.user.cursorless_open_instructions()

    def draw(self, canvas):
        self.x = canvas.x + outer_padding
        self.w = 0
        self.max_y = 0

        self.draw_background(canvas)
        self.draw_legend(canvas)
        self.draw_close(canvas)
        self.draw_url(canvas)

        self.y = get_y(canvas)
        self.w = 0

        all_actions = {}
        for name in ACTION_LIST_NAMES:
            all_actions.update(get_raw_list(name))

        keys = dict_remove_values(all_actions, "bring", "move", "swap", "reformat")
        make_dict_readable(
            all_actions,
            {
                "call": "Call T on S",
                "wrap": '"round" wrap T',
            },
        )
        all_actions = {
            **all_actions,
            "{0} T1 to T2".format(keys["bring"]): "Replace T2 with T1",
            "{0} T".format(keys["bring"]): "Replace S with T",
            "{0} T1 to T2".format(keys["move"]): "Move T1 to T2",
            "{0} T".format(keys["move"]): "Move T to S",
            "{0} T1 to T2".format(keys["swap"]): "Swap T1 with T2",
            "{0} T".format(keys["swap"]): "Swap S with T",
            "{0} * at T".format(keys["reformat"]): "Reformat T as *",
        }

        actions_limit = round(len(all_actions) / 2)
        actions_1 = slice_dict(all_actions, 0, actions_limit)
        actions_2 = slice_dict(all_actions, actions_limit)

        self.draw_header(canvas, "Actions")
        self.draw_items(canvas, actions_1)
        self.next_column(canvas)

        self.draw_header(canvas, "More actions")
        self.draw_items(canvas, actions_2)
        self.next_column(canvas)

        all_scopes = get_list("scope_type")
        scopes_limit = round(len(all_scopes) - 3)
        scopes_1 = slice_dict(all_scopes, 0, scopes_limit)
        scopes_2 = slice_dict(all_scopes, scopes_limit)

        self.draw_header(canvas, "Scopes")
        self.draw_items(canvas, scopes_1)

        self.next_column(canvas)

        self.draw_header(canvas, "More scopes")
        self.draw_items(canvas, scopes_2)

        self.next_row()
        self.draw_header(canvas, "Selection types")
        self.draw_items(canvas, get_list("selection_type"))

        self.next_row()
        self.draw_header(canvas, "Subtokens")
        self.draw_items(canvas, get_list("subtoken"))

        self.next_row()
        self.draw_header(canvas, "Positions")
        self.draw_items(canvas, get_list("position"))

        self.next_row()
        self.draw_header(canvas, "Special marks")
        self.draw_items(
            canvas,
            get_list(
                "special_mark",
                {"this": "Selection", "that": "Last T", "source": "Source T"},
            ),
        )

        self.next_column(canvas)

        self.draw_header(canvas, "Compound targets")
        self.draw_items(
            canvas,
            {
                "T and T": "T1 and T2",
                "T past T": "T1 past T2",
                "past T": "S past T",
            },
        )

        self.next_row()
        self.draw_header(canvas, "Colors")
        self.draw_items(canvas, get_list("symbol_color"))

        self.next_row()
        self.draw_header(canvas, "Examples")
        self.draw_items(
            canvas,
            [
                "Post blue air",
                "Take funk green bat",
                "Chuck air past cap",
                "Clear first word drum",
                "Bring line each to fine",
                "Take gust and harp",
                "Copy that",
                "Center funk",
            ],
        )

        # Resize to fit content
        # NB: We debounce because for some reason draw gets called multiple
        # times in quick succession.
        self.debounce_resize(
            math.ceil(self.x - canvas.x + self.w + outer_padding),
            math.ceil(self.max_y - canvas.y + outer_padding),
        )

    def draw_background(self, canvas):
        radius = 10
        rrect = skia.RoundRect.from_rect(canvas.rect, x=radius, y=radius)
        canvas.paint.style = canvas.paint.Style.FILL
        canvas.paint.color = background_color
        canvas.draw_rrect(rrect)

        canvas.paint.style = canvas.paint.Style.STROKE
        canvas.paint.color = border_color
        canvas.draw_rrect(rrect)

    def draw_legend(self, canvas):
        canvas.paint.style = canvas.paint.Style.FILL
        canvas.paint.textsize = text_size
        canvas.paint.color = text_color
        self.y = canvas.y + canvas.height - line_height
        self.draw_value(canvas, "S = Current selection    T = Target")

    def draw_close(self, canvas):
        canvas.paint.textsize = close_size
        canvas.paint.style = canvas.paint.Style.FILL
        rect = get_close_rect(canvas)
        padding = close_size * 0.375
        canvas.draw_text("X", rect.x + padding, rect.y + rect.height - padding)

    def draw_url(self, canvas):
        canvas.paint.textsize = url_text_size
        canvas.paint.color = url_color
        canvas.paint.style = canvas.paint.Style.FILL
        rect = get_url_rect(canvas)
        self.url_rect = rect
        draw_text(
            canvas, instructions_text, rect.x + line_height, rect.y + 1.5 * padding
        )

    def next_column(self, canvas):
        self.max_y = max(self.max_y, self.y)
        self.x = self.x + self.w + 1.5 * line_height
        self.y = get_y(canvas)
        self.w = 0

    def next_row(self):
        self.y += line_height

    def draw_header(self, canvas, text):
        canvas.paint.typeface = text_font
        canvas.paint.color = header_color
        canvas.paint.textsize = header_size
        canvas.paint.style = canvas.paint.Style.FILL
        canvas.paint.font.embolden = True
        rect = canvas.paint.measure_text(text)[1]
        draw_text(canvas, text, self.x, self.y)
        self.y += line_height
        self.w = max(self.w, rect.width)

    def draw_items(self, canvas, items):
        canvas.paint.textsize = text_size
        canvas.paint.style = canvas.paint.Style.FILL
        canvas.paint.font.embolden = False
        if isinstance(items, dict):
            self.draw_dict(canvas, items)
        else:
            self.draw_list(canvas, items)

    def draw_dict(self, canvas, items):
        x_org = self.x
        y_org = self.y
        w_org = self.w

        self.w = 0
        for text in items.keys():
            self.draw_key(canvas, text)
        width_key = self.w

        self.x = x_org + width_key + line_height
        self.y = y_org
        self.w = 0
        for text in items.values():
            self.draw_value(canvas, text)
        width_value = self.w

        self.x = x_org
        self.w = max(w_org, width_key + line_height + width_value)

    def draw_list(self, canvas, items):
        for text in items:
            self.draw_key(canvas, text)

    def draw_key(self, canvas, text):
        canvas.paint.typeface = command_font
        rect = canvas.paint.measure_text(text)[1]

        canvas.paint.color = command_background_color
        radius = 4
        rrect = ui.Rect(
            self.x, self.y, rect.width + 2 * padding, text_size + 2 * padding
        )
        rrect = skia.RoundRect.from_rect(rrect, x=radius, y=radius)
        canvas.draw_rrect(rrect)

        canvas.paint.color = command_text_color
        draw_text(canvas, text, self.x + padding, self.y)

        self.y += line_height
        self.w = max(self.w, rect.width)

    def draw_value(self, canvas, text):
        canvas.paint.typeface = text_font
        canvas.paint.color = text_color
        rect = canvas.paint.measure_text(text)[1]
        draw_text(canvas, text, self.x, self.y)
        self.y += line_height
        self.w = max(self.w, rect.width)


@mod.action_class
class Actions:
    def cursorless_cheat_sheet_toggle():
        """Toggle cursorless cheat sheet"""
        global cheat_sheet
        if cheat_sheet:
            actions.mode.disable("user.cursorless_cheat_sheet")
            cheat_sheet.close()
            cheat_sheet = None
        else:
            cheat_sheet = CheatSheet()
            actions.mode.enable("user.cursorless_cheat_sheet")

    def cursorless_open_instructions():
        """Open web page with cursorless instructions"""
        webbrowser.open(instructions_url)


def get_list(name, descriptions={}):
    items = get_raw_list(f"user.cursorless_{name}")
    if isinstance(items, dict):
        make_dict_readable(items, descriptions)
    return items


def get_raw_list(name):
    return registry.lists[name][0].copy()


def get_y(canvas):
    return canvas.y + outer_padding


def draw_text(canvas, text, x, y):
    canvas.draw_text(text, x, y + text_size + padding / 2)


def make_dict_readable(dict, descriptions={}):
    for k in dict:
        desc = dict[k]
        if desc in descriptions:
            desc = descriptions[desc]
        else:
            desc = make_readable(desc)
        dict[k] = desc


def make_readable(text):
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text).lower().capitalize()


def get_close_rect(canvas):
    wh = 1.5 * close_size
    cr = canvas.rect
    return ui.Rect(cr.x + cr.width - wh, cr.y, wh, wh)


def get_url_rect(canvas):
    rect = canvas.paint.measure_text(instructions_text)[1]
    width = rect.width + 2 * line_height
    height = line_height + padding
    cr = canvas.rect
    return ui.Rect(cr.x + cr.width - width, cr.y + cr.height - height, width, height)


def in_range(value, min, max):
    return value >= min and value <= max


def is_in_rect(canvas, mouse_pos, rect):
    return in_range(mouse_pos.x, rect.x, rect.x + rect.width) and in_range(
        mouse_pos.y, rect.y, rect.y + rect.height
    )


def slice_dict(dict: dict, start: int, end: int = None):
    keys = sorted(dict)[start:end]
    return {key: dict[key] for key in keys}


def dict_remove_values(dict: dict, *values: list):
    keys = {}
    for key, value in dict.copy().items():
        if value in values:
            del dict[key]
            keys[value] = key
    assert len(values) == len(keys)
    return keys
