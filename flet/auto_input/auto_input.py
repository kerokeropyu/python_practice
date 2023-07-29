import flet as ft
import configparser
import datetime
from flet import (
    Page,
    colors
)

# 変数
dt = datetime.datetime.today()
today = str(dt.date())
url = 'test.com'
start_time ='0900'
end_time = '1800'
except_holidays = True
id = '12345'
password = 'password'

# global dt
# global today
# global url
# global start_time
# global end_time
# global except_holidays
# global id
# global password

# 設定読み込み
def load_settings():
    config = configparser.ConfigParser()
    config.read('../settings.ini')
    settings = config['DEFAULT']
    url = settings.get('url')
    start_time = settings.get('start_time')
    end_time = settings.get('end_time')
    except_holidays = settings.getboolean('exclude_holidays', False)
    id = settings.get('id')
    password = settings.get('password')
    # dt = datetime.datetime.today()
    # today = str(dt.date())
    # print(url, start_time, end_time, except_holidays, id, password)
def get_init_value():
    return 1

def test():
    print(1)

def main(page: ft.Page):
    load_settings()
    page.title = "Auto Input King-Of-Time"
    page.bgcolor = colors.SECONDARY
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.AUTO_MODE_OUTLINED),
        leading_width=40,
        title=ft.Text("king of time 自動入力"),
        center_title=False,
        # bgcolor=ft.colors.SURFACE_VARIANT,
        bgcolor=ft.colors.DEEP_PURPLE,
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="終了", on_click=test),
                ]
            ),
        ],
    )
    page.add(
        ft.Container(
            content=ft.Text("今日の日付:"+today),
            alignment=ft.alignment.top_right,
            border_radius=10,
        ),
        ft.TextField(label="URL", value=url),
        ft.ResponsiveRow(
            [
                ft.TextField(label="出勤時間", keyboard_type="NUMBER", max_length=4, hint_text="0900", value=start_time, col={"md": 6}),
                ft.TextField(label="退勤時間", keyboard_type="NUMBER", max_length=4, hint_text="1800", value=end_time, col={"md": 6}),
            ],
            run_spacing={"xs": 10},
        ),

        ft.TextField(label="ID", keyboard_type="TEXT", value=id),
        ft.TextField(label="パスワード", keyboard_type="VISIBLE_PASSWORD", password=True, can_reveal_password=True, value=password),
        
        ft.Container(
            content=ft.Checkbox(value=True, label="土日を除く"),
            alignment=ft.alignment.top_right,
            border_radius=10,
        ),
        # ft.label(),
        ft.Container(
            ft.ElevatedButton(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(value="実行", size=20),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=3,
                    ),
                    padding=ft.padding.all(5),
                ),
                bgcolor=ft.colors.DEEP_PURPLE,
            ),
            alignment=ft.alignment.top_right,
            border_radius=10,
        ),
        ft.ElevatedButton(
            "実行",
            style=ft.ButtonStyle(
                color={
                    ft.MaterialState.HOVERED: ft.colors.WHITE,
                    ft.MaterialState.FOCUSED: ft.colors.BLUE,
                    ft.MaterialState.DEFAULT: ft.colors.GREY_300,
                },
                shape=ft.StadiumBorder(),
            ),
            on_click=test
        ),
    )


ft.app(target=main)