from os import getenv
import flet as ft
from google.cloud import bigquery as bq


# Get PORT value from environment
PORT = int(getenv("PORT", "8550"))

project = "imagebase-414802"
dataset = "imagebase"
label = "fantasy"

db_client = bq.Client(project=project)
db_table = f"{project}.{dataset}.{label}"


def get_items():
    """Get image headers from the database"""
    h_query = "title, prompt, url"
    return db_client.query(f"SELECT {h_query} FROM {db_table}").result()


# Function to get item tiles
def get_item_tiles(click_function):
    tile_list = []
    for item in get_items():
        tile = ft.ListTile(
            title=ft.Text(item["title"]),
            leading=ft.Image(item["url"], fit="contain"),
            data=item,
            on_click=click_function,
        )
        tile_list.append(tile)
    return tile_list


# Main function
def main(page: ft.Page):

    # Right-side content placeholder
    content_title = ft.Text(
        "Select an item from the list on the left",
        theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,
    )
    content_text = ft.Text()
    content_image = ft.Image(src="", height=500, width=500)
    content_stack = [
        content_title,
        content_text,
        content_image,
    ]

    # Function to update content
    def item_clicked(e):
        content_title.value = e.control.data["title"]
        content_text.value = e.control.data["prompt"]
        content_image.src = e.control.data["url"]
        page.update()

    # Left-side list of items
    items_list = ft.ListView(
        controls=get_item_tiles(item_clicked),
        width=400,
    )

    # Right-side content display
    content_display = ft.Column(content_stack, expand=True, scroll=ft.ScrollMode.ALWAYS)

    # Main layout
    main_row = ft.Row([items_list, content_display], expand=True)
    page.add(main_row)


# Run the app
ft.app(target=main, port=PORT, view=ft.AppView.WEB_BROWSER)
