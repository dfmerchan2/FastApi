from pathlib import Path

from reactpy import component, html


stylesheet_css = Path("config/templates/button_styles.css").read_text()


@component
def welcome_message(title):
    return html.div(
        html.h3(title)
    )


@component
def menu_bar():
    return html.ul(
        html.li(
            html.a(""),
            "BookShop"
        )
    )

@component
def button_login():
    return html.button(
        {"on_click": lambda event: html.title("Hola"),
         "id": "btn_login"},
        "Login"
    )

@component
def button_sign_in():
    return html.button(
        {"on_click": lambda event: html.title("Hola"),
         "id": "btn_sign_in"},
        "Sign in"
    )


@component
def choose():
    return html.div(
        html.p("What do you want to do today"),
        button_login(),
        button_sign_in()
    )


@component
def button_create_user_admin():
    return html.button(
        {"on_click": lambda event: html.title("Hola"),
         "id": "btn_create_user_admin"},
        "Create Admin"
    )


@component
def button_create_user_customer():
    return html.button({"on_click":lambda event: "Hola"}, "Create Customer")


@component
def button_create_user_manager():
    return html.button({"on_click":lambda event: "Hola"}, "Create Manager")


@component
def HomePage():
    return html.div(
        html.style(stylesheet_css),
        html.nav(menu_bar()),
        html.br(),
        welcome_message("Welcome to book store"),
        html.div(
            choose(),
            html.br(),
            html.br(),
        )
    )