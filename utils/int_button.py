import flet as ft 


def incr_btn(e, text):
    text.value = str(round(float(text.value) + 0.1, 2))
    e.page.update()

def decr_btn(e, text):
    text.value = str(round(float(text.value) - 0.1, 2))
    e.page.update()

def Stepper():
    text =  ft.TextField(
        text_align="center",
        value="0",
        keyboard_type=ft.KeyboardType.NUMBER,
        label="inch",
        width=150,
        height=60,
        prefix=ft.IconButton(ft.icons.ARROW_UPWARD, icon_color=ft.colors.BLACK, on_click=lambda e: incr_btn(e, text)),
        suffix=ft.IconButton(ft.icons.ARROW_DOWNWARD, icon_color=ft.colors.BLACK, on_click=lambda e: decr_btn(e, text)),
        border_radius=10,
        show_cursor=False,
        color="black",
        input_filter=ft.NumbersOnlyInputFilter()
    )
    return text

