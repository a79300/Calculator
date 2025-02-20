import flet as ft
import math
import re


class CalculatorApp:
    def __init__(self, page: ft.Page):
        self.buttons = [
            ["COS", "SEN", "TAN", "DEL"],
            ["√", "(", ")", "AC"],
            ["*", "/", "^", "+/-"],
            ["7", "8", "9", "%"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "ANS", "="],
        ]
        self.page = page
        self.columns = []

        self.get_text_size(self.page.height)

        self.expression = ft.TextField(
            hint_text="...",
            color="black",
            text_align=ft.TextAlign.RIGHT,
            read_only=True,
            expand=True,
            border_width=0,
            text_size=self.expression_size,
        )

        self.result = ft.TextField(
            hint_text="0",
            color="black",
            text_align=ft.TextAlign.RIGHT,
            read_only=True,
            expand=True,
            border_width=0,
            text_size=self.result_size,
        )
        self.result_size = None
        self.expression_size = None
        self.current_expression = ""
        self.display_expression = ""
        self.last_result = ""

        for row_idx, row in enumerate(self.buttons):
            for col_idx, button_text in enumerate(row):
                self.columns.append(
                    ft.Container(
                        ft.Button(
                            button_text,
                            bgcolor=ft.Colors.BLACK,
                            color=ft.Colors.WHITE,
                            on_click=self.button_click,
                        ),
                        col={
                            "xs": 3,
                            "sm": 3,
                            "md": 3,
                            "xl": 3,
                        },
                    )
                )

        self.main_container = ft.Column(
            [
                ft.ResponsiveRow(
                    [
                        ft.Column(
                            [
                                ft.ResponsiveRow(
                                    [
                                        ft.Column(
                                            [
                                                ft.IconButton(
                                                    icon=ft.Icons.MENU,
                                                    icon_color="black",
                                                )
                                            ],
                                            col={
                                                "xs": 3,
                                                "sm": 3,
                                                "md": 3,
                                                "xl": 3,
                                            },
                                        ),
                                        ft.Column(
                                            [self.expression],
                                            col={
                                                "xs": 9,
                                                "sm": 9,
                                                "md": 9,
                                                "xl": 9,
                                            },
                                        ),
                                    ]
                                ),
                                ft.ResponsiveRow([self.result]),
                            ]
                        )
                    ]
                ),
                ft.ResponsiveRow(self.columns),
            ]
        )

        self.stack = ft.Stack(
            controls=[
                self.main_container,
            ],
            expand=True,
        )

        self.page.add(self.stack)

    def get_text_size(self, screen_height):
        if screen_height <= 650:
            self.result_size = 70
        else:
            self.result_size = 70 + round(((screen_height - 650) // 50), 0) * 20
        self.expression_size = self.result_size / 2
        self.letter_size = self.result_size // 3
        self.history_letter_size = self.result_size // 8.5
        self.page.update()

    def button_click(self, e):
        if e.control.text == "=":
            pass
        elif e.control.text == "AC":
            self.clear_expression()
        elif e.control.text == "DEL":
            self.delete_last_character()
        elif e.control.text == "^":
            self.add_to_expression("**", "^")
        elif e.control.text in ("(", ")"):
            self.add_to_expression(
                e.control.text, e.control.text, check_parentheses=True
            )
        elif e.control.text == "ANS":
            self.add_to_expression(self.last_result, "ANS")
        elif e.control.text == "√":
            self.add_to_expression("math.sqrt(", "√(")
        elif e.control.text == "∛":
            self.add_to_expression("math.cbrt(", "∛(")
        elif e.control.text == "π":
            self.add_to_expression(str(math.pi), "π")
        elif e.control.text == "+/-":
            pass
        elif e.control.text == "%":
            self.add_to_expression("%", "%")
        elif e.control.text == "COS":
            self.add_to_expression("math.cos(math.radians(", "COS(")
        elif e.control.text == "SEN":
            self.add_to_expression("math.sin(math.radians(", "SEN(")
        elif e.control.text == "TAN":
            self.add_to_expression("math.tan(math.radians(", "TAN(")
        else:
            self.add_to_expression(e.control.text, e.control.text)

    def add_to_expression(self, value, display_value, check_parentheses=False):
        if check_parentheses and value == ")":
            pattern = re.compile(r"math\.(cos|sin|tan)\(math\.radians\([^()]*$")
            if pattern.search(self.current_expression):
                self.current_expression += "))"
            else:
                self.current_expression += value
            self.display_expression += value
        else:
            self.current_expression += value
            self.display_expression += display_value

        self.expression.value = self.display_expression
        self.expression.update()

    def clear_expression(self):
        self.result.value = ""
        self.expression.value = ""
        self.current_expression = ""
        self.display_expression = ""
        self.result.update()
        self.expression.update()
        self.page.update()

    def delete_last_character(self):
        self.current_expression = self.current_expression[:-1]
        self.display_expression = self.display_expression[:-1]
        self.expression.value = self.display_expression
        self.expression.update()


def main(page: ft.Page):
    CalculatorApp(page)


ft.app(target=main, assets_dir="assets")
