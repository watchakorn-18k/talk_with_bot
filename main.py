import threading
import flet as ft
import datetime
import requests
from dotenv import load_dotenv

load_dotenv()
import os

api = os.environ.get("API_URL")


def create_state(name, value=None):
    globals()[name] = value


def send_api(text="hello"):
    response = requests.post(api + "generate", json={"text": text})


def get_api():
    return requests.get(api + "generate-text").json()["data"]


def get_api_date():
    return requests.get(api + "generate-text").json()["date"]


class InputField(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.text_field = ft.TextField(
            height=50,
            width=300,
            border_color=ft.colors.PRIMARY,
            on_change=self.on_change_text,
        )
        self.page = page
        self.button_send = ft.IconButton(
            icon=ft.icons.SEND,
            disabled=True,
        )

    def update(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            super().update()
            self.page.update()

    def on_change_text(self, e):
        self.button_send.disabled = False if e.control.value else True
        super().update()
        self.page.update()

    def build(self):
        return ft.Container(
            content=ft.Row(
                [
                    self.text_field,
                    ft.Container(
                        self.button_send,
                        bgcolor=ft.colors.PRIMARY_CONTAINER,
                        border_radius=10,
                        height=50,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )


class MainPage(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.list_view = ft.ListView(height=500, padding=20)
        self.text_show_from_input = "สวัสดีจ้า"
        self.text_bot = ""
        self.date_text = ""

    def build(self):
        data_example = [
            {
                "id": "ตัวอย่าง",
                "content": [
                    "ไอเดียสร้างสรรค์สำหรับวันเกิดอายุ 10 ขวบไหม?",
                    "ฉันจะส่งคำขอ HTTP ใน Javascript ได้อย่างไร",
                    "อธิบายการคำนวณควอนตัมด้วยคำศัพท์ง่ายๆ",
                ],
            },
            {
                "id": "ความสามารถ",
                "content": [
                    "สามารถถามได้ทุกอย่าง หากตอบไม่ได้จะทำการปฏิเสธ",
                    "ได้รับการฝึกฝนให้ปฏิเสธคำขอที่ไม่เหมาะสม",
                    "ใช้งานได้ฟรี ไม่จำเป็นต้องใช้ token ในการใช้งานก่อน",
                ],
            },
            {
                "id": "ข้อจำกัด",
                "content": [
                    "บางครั้งอาจสร้างคำแนะนำที่เป็นอันตรายหรือเนื้อหาที่มีอคติ",
                    "ความรู้จำกัดของโลกและเหตุการณ์หลังปี 2021",
                    "บางครั้งอาจสร้างข้อมูลที่ไม่ถูกต้อง",
                ],
            },
        ]
        header_example = ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND)
        exaple_list = ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND)

        for i in data_example:
            header_example.controls.append(
                ft.Row(
                    [
                        ft.Text(i["id"]),
                    ],
                )
            )
            exaple_list.controls.append(
                ft.Column(
                    [
                        ft.Card(
                            content=ft.Container(
                                ft.Text(
                                    i["content"][0],
                                    text_align=ft.TextAlign.CENTER,
                                    size=10,
                                ),
                                width=87,
                                padding=ft.padding.all(10),
                            ),
                            height=85,
                        ),
                        ft.Card(
                            content=ft.Container(
                                ft.Text(
                                    i["content"][1],
                                    text_align=ft.TextAlign.CENTER,
                                    size=10,
                                ),
                                width=87,
                                padding=ft.padding.all(10),
                            ),
                            height=85,
                        ),
                        ft.Card(
                            content=ft.Container(
                                ft.Text(
                                    i["content"][2],
                                    text_align=ft.TextAlign.CENTER,
                                    size=10,
                                ),
                                width=87,
                                padding=ft.padding.all(10),
                            ),
                            height=85,
                        ),
                    ],
                )
            )

        controls = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("พูดคุยกับ AI", size=30, color=ft.colors.PRIMARY),
                        ft.Text("วัชกร บุตร์ดีวงษ์"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(padding=5),
                ft.Row(
                    [
                        ft.Icon(name="person", size=30, color=ft.colors.PRIMARY),
                        ft.Icon(name="bolt", size=30, color=ft.colors.PRIMARY),
                        ft.Icon(name="smart_toy", size=30, color=ft.colors.PRIMARY),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                ft.Container(padding=5),
                ft.Column(
                    [header_example, exaple_list],
                ),
                ft.Container(height=80),
            ]
        )

        return controls

    def chat_page(self):
        self.client_card = ft.Row(
            [
                ft.Icon(name="person", color=ft.colors.PRIMARY, size=30),
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    f"{datetime.datetime.now().strftime('%d/%m/%Y')},{datetime.datetime.now().strftime('%H:%M:%S')}",
                                    size=10,
                                ),
                            ]
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(self.text_show_from_input),
                                    ]
                                ),
                                width=300,
                                padding=20,
                            )
                        ),
                    ]
                ),
            ]
        )
        self.bot_card = ft.Row(
            [
                ft.Icon(name="smart_toy", color=ft.colors.SECONDARY, size=30),
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    self.date_text,
                                    size=10,
                                ),
                            ]
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        self.text_bot,
                                    ]
                                ),
                                width=300,
                                padding=20,
                            )
                        ),
                    ]
                ),
            ]
        )

        self.list_view.controls = [self.client_card, self.bot_card]

        return ft.Column(
            [
                self.list_view,
                ft.Container(height=30),
            ]
        )


class AppTalkBot(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.app_bar()
        self.input_text = InputField(self.page)
        self.main_page = MainPage()
        self.text_field = self.input_text.text_field
        self.btn_send = self.input_text.button_send
        self.btn_send.on_click = self.after_click

    # create decoration
    def update(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            super().update()
            self.page.update()

        return wrapper

    @update
    def switch_theme(self, e):
        self.page.theme_mode = (
            ft.ThemeMode.LIGHT
            if self.page.theme_mode == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        super().update()

    @update
    def app_bar(self):
        button_switch = ft.IconButton(
            icon=ft.icons.DARK_MODE, on_click=self.switch_theme
        )
        self.page.appbar = ft.AppBar(
            leading_width=40,
            title=ft.Text("คุยกับ AI"),
            center_title=False,
            bgcolor=ft.colors.PRIMARY_CONTAINER,
            actions=[button_switch],
        )

    @update
    def after_click(self, e):
        def widget_static():
            self.main_page.update()
            self.main_page.text_show_from_input = self.text_field.value
            self.main_page.controls.pop()
            self.main_page.controls.append(self.main_page.chat_page())
            self.main_page.update()

        def task():
            while True:
                if get_api():
                    self.main_page.text_bot = ft.Text(get_api())
                    self.main_page.date_text = get_api_date()
                    widget_static()
                    break

        if self.text_field.value != "":
            threading.Thread(target=send_api, args=(self.text_field.value,)).start()
            threading.Thread(target=task).start()
            self.main_page.text_bot = ft.Row(
                [
                    ft.ProgressRing(width=16, height=16, stroke_width=2),
                    ft.Text("กำลังประมวลข้อความอยู่รอสักครู่..."),
                ]
            )
            widget_static()

    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    self.main_page,
                    self.input_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=30,
        )


def main(page: ft.Page):
    page.title = "คุยกับ AI"
    page.theme = ft.Theme(color_scheme_seed=ft.colors.INDIGO)
    app = AppTalkBot(page)
    page.window_height = 1039
    page.window_width = 575
    page.add(app)


ft.app(main, view=ft.WEB_BROWSER, port=8080)
