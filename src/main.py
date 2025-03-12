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
        self.result_size = 70
        self.expression_size = self.result_size/2
        self.current_expression = ""
        self.display_expression = ""
        self.last_result = ""
        self.lastExpression = []

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
        
        self.get_text_size(self.page.height)

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

        self.close_button = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_color="red",
            on_click=self.toggle_history,
            width=self.letter_size,
            height=self.letter_size,
        )

        self.history_list = ft.Column(
            scroll=None,
            height=self.page.height * 0.55,
            alignment=ft.MainAxisAlignment.START,
            controls=[],
        )

        self.history_container = ft.Container(
            content=ft.Column(
                [
                    ft.ResponsiveRow([self.close_button], alignment="end"),
                    ft.ResponsiveRow([self.history_list]),
                ]
            ),
            bgcolor=ft.Colors.BLACK,
            border_radius=ft.border_radius.all(20),
            padding=ft.padding.all(20),
            visible=False,
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
                                                    on_click=self.toggle_history,
                                                    icon_size=self.letter_size * 1.5,
                                                    width=self.letter_size * 1.5,
                                                    height=self.letter_size * 1.5,
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
                self.history_container,
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
    
    def resizeTexts(self):
        ##self.result_size = self.result_size * 0.9
        ##self.expression_size = self.result_size / 2
        #print(type(self.result_size))
        #print(type(self.expression_size))
        self.page.update()

    def toggle_history(self, e):
        self.history_container.visible = not self.history_container.visible
        if self.history_container.visible:
            self.load_history()
        self.page.update()

    def load_history(self):
        self.history_list.controls.clear()
        for history_id in range(1, 11):
            if self.page.client_storage.contains_key(str(history_id)):
                expression, result_value = self.page.client_storage.get(str(history_id))
                self.history_list.controls.append(
                    ft.Column(
                        [
                            ft.ResponsiveRow(
                                [
                                    ft.Column(
                                        [
                                            ft.ResponsiveRow(
                                                [
                                                    ft.Text(
                                                        f"{expression}",
                                                        size=self.history_letter_size,
                                                        color=ft.Colors.GREY,
                                                    ),
                                                ]
                                            ),
                                            ft.ResponsiveRow(
                                                [
                                                    ft.Text(
                                                        f"{result_value}",
                                                        size=self.history_letter_size,
                                                        color=ft.Colors.WHITE,
                                                    ),
                                                ]
                                            ),
                                        ],
                                        col={
                                            "xs": 9,
                                            "sm": 9,
                                            "md": 9,
                                            "xl": 9,
                                        },
                                    ),
                                    ft.Column(
                                        [
                                            ft.ResponsiveRow(
                                                [
                                                    ft.Column(
                                                        [
                                                            ft.IconButton(
                                                                icon=ft.Icons.COPY,
                                                                icon_color="gray",
                                                                icon_size=self.history_letter_size,
                                                                on_click=self.copy_value(
                                                                    str(history_id)
                                                                ),
                                                                width=self.history_letter_size,
                                                                height=self.history_letter_size,
                                                                padding=ft.padding.all(
                                                                    0
                                                                ),
                                                            )
                                                        ],
                                                        col={
                                                            "xs": 6,
                                                            "sm": 6,
                                                            "md": 6,
                                                            "xl": 6,
                                                        },
                                                    ),
                                                    ft.Column(
                                                        [
                                                            ft.IconButton(
                                                                icon=ft.Icons.DELETE,
                                                                icon_color="red",
                                                                icon_size=self.history_letter_size,
                                                                on_click=self.delete_history(
                                                                    str(history_id)
                                                                ),
                                                                width=self.history_letter_size,
                                                                height=self.history_letter_size,
                                                                padding=ft.padding.all(
                                                                    0
                                                                ),
                                                            ),
                                                        ],
                                                        col={
                                                            "xs": 6,
                                                            "sm": 6,
                                                            "md": 6,
                                                            "xl": 6,
                                                        },
                                                    ),
                                                ]
                                            ),
                                        ],
                                        col={
                                            "xs": 3,
                                            "sm": 3,
                                            "md": 3,
                                            "xl": 3,
                                        },
                                    ),
                                ],
                            ),
                            ft.Divider(height=1),
                        ]
                    )
                )
        self.history_list.update()

    def delete_history(self, id):
        def delete(e):
            self.page.client_storage.remove(id)
            self.load_history()

        return delete

    def copy_value(self, id):
        def copy(e):
            _, result_value = self.page.client_storage.get(id)
            self.page.set_clipboard(result_value)

        return copy

    def button_click(self, e):
        self.resizeTexts()
        print(self.current_expression)

        if not self.current_expression and e.control.text in "=%DEL^*+-./":
            return
        elif e.control.text == "=":
            self.evaluate_expression()
        elif e.control.text == "AC":
            self.clear_expression()
        elif e.control.text == "DEL":
            self.delete_last_character(e)
        elif e.control.text == "^":
            self.add_to_expression("**", "^")
        elif e.control.text == "ANS":
            self.add_to_expression(self.last_result, "ANS")
        elif e.control.text == "√":
            self.add_to_expression("math.sqrt(", "√(")
        elif e.control.text == "∛":
            self.add_to_expression("math.cbrt(", "∛(")
        elif e.control.text == "π":
            self.add_to_expression(str(math.pi), "π")
        elif e.control.text == "+/-":
            self.toggle_sign()
        elif e.control.text == "%":
            self.add_to_expression("%", "%")
        elif e.control.text == "COS":
            self.add_to_expression("math.cos(math.radians(", "COS(")
        elif e.control.text == "SEN":
            self.add_to_expression("math.sin(math.radians(", "SEN(")
        elif e.control.text == "TAN":
            self.add_to_expression("math.tan(math.radians(", "TAN(")
        elif e.control.text in ("(", ")"):
            self.add_to_expression(
                e.control.text, e.control.text, check_parentheses=True
            )
        else:
            self.add_to_expression(e.control.text, e.control.text)

    def close_expression(self):
        count_parenthesis_current_expression = self.current_expression.count('(') - self.current_expression.count(')')
        self.current_expression += (" )" * count_parenthesis_current_expression)

        count_parenthesis_display_expression = self.display_expression.count('(') - self.display_expression.count(')')
        self.display_expression += (" )" * count_parenthesis_display_expression)

        self.expression.value = self.display_expression
        self.expression.update()


    def evaluate_expression(self):
        try:
            self.close_expression()

            result_value = eval(
                self.current_expression, {"__builtins__": None}, {"math": math}
            )

            if isinstance(result_value, float) and result_value.is_integer():
                result_value = int(result_value)
            else:
                result_value = str(round(result_value, 2))

            self.result.value = self.format_result(str(result_value))
            self.result.update()
            self.last_result = str(result_value)

            for history_id in reversed(range(1, 11)):
                if not self.page.client_storage.contains_key(str(history_id)):
                    self.page.client_storage.set(
                        str(history_id), (self.display_expression, result_value)
                    )
                    break
            else:
                for history_id in reversed(range(1, 11)):
                    if history_id < 10:
                        self.page.client_storage.set(
                            str(history_id + 1),
                            self.page.client_storage.get(str(history_id)),
                        )
                self.page.client_storage.set(
                    "1", (self.display_expression, result_value)
                )

            self.load_history()
            self.current_expression = ""
            self.display_expression = ""

        except Exception:
            self.result.value = "Error"

    def add_to_expression(self, value, display_value, check_parentheses=False):

        if len(self.display_expression) > 0 and (
                value not in "0123456789" or self.display_expression[-1] not in "0123456789"
            ):
            self.display_expression += " "

        if check_parentheses and value == ")":
            pattern = re.compile(r"math\.(cos|sin|tan)\(math\.radians\([^()]*$")
            if pattern.search(self.current_expression):
                self.current_expression += "))"
            else:
                if self.display_expression and (self.display_expression[-2] in "(" or self.display_expression[-1] in "("):
                    self.current_expression += '0' + value
                    self.display_expression += '0 '
                    self.lastExpression.append([len(str('0')), len(str('0'))])
                else:
                    self.current_expression += value
            self.display_expression += value
        else:
            if (value == "(" and self.display_expression and self.display_expression[-2] in "0123456789)") or (value in "0123456789"  and self.display_expression and self.display_expression[-2] == ")"):
                self.current_expression += '*'
                self.display_expression += '*' + " "
                self.lastExpression.append([len(str('*')), len(str('*'))])

            self.current_expression += value
            self.display_expression += display_value
        
        self.lastExpression.append([len(str(value)), len(str(display_value))])
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

    def delete_last_character(self, e):
        if len(self.lastExpression) > 0:
            self.current_expression = self.current_expression[:-self.lastExpression[-1][0]]
            self.display_expression = self.display_expression[:-self.lastExpression[-1][1]]
            self.lastExpression.pop()
            if self.display_expression.endswith(" "):
                self.display_expression = self.display_expression[: -1]
        
        self.expression.value = self.display_expression
        self.expression.update()

    def toggle_sign(self):
        if self.current_expression and self.current_expression[-1].isdigit():
            sign_index = len(self.current_expression) - 1
            while sign_index >= 0 and (
                self.current_expression[sign_index].isdigit()
                or self.current_expression[sign_index] == "."
            ):
                sign_index -= 1
            sign_index += 1

            is_negative = self.current_expression[sign_index - 1] == "-"
            has_operator_before = sign_index == 0 or any(
                op in self.current_expression[sign_index - 1] for op in "+-*/"
            )

            if is_negative:
                self.current_expression = (
                    self.current_expression[: sign_index - 1]
                    + self.current_expression[sign_index:]
                )
                self.display_expression = (
                    self.display_expression[: sign_index - 1]
                    + self.display_expression[sign_index:]
                )
            elif has_operator_before:
                self.current_expression = (
                    self.current_expression[:sign_index]
                    + "-"
                    + self.current_expression[sign_index:]
                )
                self.display_expression = (
                    self.display_expression[:sign_index]
                    + "-"
                    + self.display_expression[sign_index:]
                )
            self.expression.value = self.display_expression

            self.expression.update()

    def format_result(self, valueNumber):
        saveValue = valueNumber.split('.')
        oldValue = list(saveValue[0])
        newValue = []
        if len(valueNumber) > 3:
            counter = 0
            oldValue.reverse()
            for i in oldValue:
                if counter == 3:
                    newValue.append(' ')
                    counter = 0
                newValue.append(i)
                counter +=1
            newValue.reverse()

            valueNumber = str(''.join(newValue) + '.' + saveValue[1]) if (len(saveValue) > 1) else str(''.join(newValue))
        return valueNumber
    
def main(page: ft.Page):
    CalculatorApp(page)


app = ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)

# This makes the app work with Replit
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
