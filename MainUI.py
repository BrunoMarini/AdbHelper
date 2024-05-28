from nicegui import ui
from pathlib import Path
from CmdHelper import AdbCommandHelper
from DbHelper import DbHelper

selectedDevice = ""
adb = AdbCommandHelper()
dbHelper = DbHelper()
table_instance = None

ui.add_head_html(
    "<style>" +
    open(Path(__file__).parent / "css" / "styles.css").read() +
    "</style>")


def _build_android_database_tab():
    with ui.grid(rows='1fr 5fr', columns='1fr 1fr 1fr 1fr').classes('w-full'):
        ui.label('Select Database').classes('text_alignment_center')
        ui.select(options=adb.list_available_db(), with_input=True,
                  on_change=lambda e: table.set_options(dbHelper.load_db(adb.pull_db(e.value)), value=1))
        ui.label('Select Table').classes('text_alignment_center')
        table = ui.select([], with_input=True, on_change=lambda e: _build_table_ui(e.value))


def _build_table_ui(sql_table):
    global table_instance

    table = dbHelper.query_table(sql_table)
    columns = table[0]
    db_columns = []
    for column in columns:
        db_columns.append({'name': column, 'label': column, 'field': column, 'align': 'center'})

    db_rows = []
    for row in table[1:]:
        table_dic = {}
        for i, col in enumerate(columns):
            table_dic[col] = row[i]
        db_rows.append(table_dic)

    if table_instance is not None:
        table_instance.delete()

    table_instance = ui.table(columns=db_columns, rows=db_rows).classes('col-span-full')
    with table_instance.add_slot('top-right'):
        def toggle() -> None:
            table_instance.toggle_fullscreen()
            button.props('icon=fullscreen_exit' if table_instance.is_fullscreen else 'icon=fullscreen')

        button = ui.button('Toggle fullscreen', icon='fullscreen', on_click=toggle).props('flat')


def _build_push_pull_tab():
    with (ui.card().classes('w-full'), ui.row()):
        with ui.column().classes('text_alignment_center'):
            ui.label('Push file to device')
            ui.image('images/ic_push.png').classes('w-32')
        ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')

        dest_path = ui.input(label='Destination Path', placeholder='Type destination path',
                             on_change=lambda e: dest_path.set_autocomplete(adb.list_related_paths(e.value))
                             ).props('clearable')
    with ui.card().classes('col-span-full'), ui.row():
        ui.image('images/ic_pull.png').classes('w-32')
        ui.label('Pull file from device')


# Header
with ui.header().classes('header') as header:
    with ui.button(icon='menu').props('flat color=white'):
        with ui.menu() as menu:
            ui.menu_item('Settings')

# Left Drawer
with ui.left_drawer().classes('left-drawer'):
    ui.label('Device List').classes('header_text')

    with ui.expansion('Select your Device', icon='work').classes('w-full'):
        devices = adb.list_devices()
        if not devices:
            ui.label('No device attached')
        else:
            for device in devices:
                with ui.row().classes('w-full border'):
                    ui.label(device[0])
                    ui.space()
                    ui.label(device[1])

    ui.space()
    ui.button('Mirror Screen').classes('w-full')

# Footer
with ui.footer(value=False) as footer:
    ui.label('For support or new feature suggestions contact: Bruno Guilherme S. Marini (b.marini)')

# Question
with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

# ADB Interation TABs
with ui.tabs().classes('w-full') as tabs:
    one = ui.tab('Android Database')
    two = ui.tab('Push / Pull')
with ui.tab_panels(tabs, value=one).classes('w-full'):
    with ui.tab_panel(one):
        _build_android_database_tab()
    with ui.tab_panel(two):
        _build_push_pull_tab()

ui.run(title='Adb Helper', dark=True)
