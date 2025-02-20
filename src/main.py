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


def main(page: ft.Page):
    CalculatorApp(page)


ft.app(target=main, assets_dir="assets")
