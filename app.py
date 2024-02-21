from os import getenv
import flet as ft
import imagebase

# Get PORT value from environment
PORT = int(getenv("PORT", "8550"))

project = "imagebase-414802"
dataset = "imagebase"
label = "fantasy"

db_client = imagebase.db.DB(project=project, dataset=dataset, table=label)


def get_rows():
    # Get all images from the database
    rows = db_client.get_all()

    # Create a dictionary of images
    items = {}
    for row in rows:
        items[row["id"]] = dict(row)
    return items


# Main function
def main(page: ft.Page):
    # Create a dictionary of images
    items = get_rows()

    # Right-side content placeholder
    content_title = ft.Text(
        "Select an item from the list on the left",
        theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,
    )
    content_text = ft.Text()
    content_image = ft.Image(src="https://i.imgflip.com/6nlb4g.jpg")
    content_stack = [
        content_title,
        content_text,
        content_image,
    ]

    # Function to update right-side content
    def item_clicked(e):
        content_title.value = items[e.control.data]["title"]
        content_text.value = items[e.control.data]["prompt"]
        content_image.src = items[e.control.data]["url"]
        # items = get_rows()
        page.update()

    # Left-side list of items
    items_list = ft.ListView(
        [
            ft.ListTile(
                title=ft.Text(items[item]["title"]),
                data=item,
                on_click=item_clicked,
            )
            for item in items.keys()
        ],
        width=200,
    )

    # Right-side content display
    content_display = ft.Column(content_stack, expand=True, scroll=ft.ScrollMode.ALWAYS)

    # Main layout
    main_row = ft.Row([items_list, content_display], expand=True)
    page.add(main_row)


# Run the app
ft.app(target=main, port=PORT, view=ft.AppView.WEB_BROWSER)
