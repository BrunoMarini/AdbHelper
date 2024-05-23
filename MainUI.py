from nicegui import ui
from CmdHelper import AdbCommandHelper
from DbHelper import DbHelper

selectedDevice = ""
adb = AdbCommandHelper()
dbHelper = DbHelper()


def _build_android_database_tab():
    with ui.grid(rows=2, columns='1fr 1fr 1fr 1fr').classes('w-full'):
        ui.label('Select Database').style('display: flex;justify-content: center;align-items: center;')
        ui.select(options=adb.list_available_db(), with_input=True,
                  on_change=lambda e: table.set_options(dbHelper.load_db(adb.pull_db(e.value)), value=1))
        ui.label('Select Table').style('display: flex;justify-content: center;align-items: center;')
        table = ui.select([], with_input=True, on_change=lambda e: _build_table_ui(e.value))


def _build_table_ui(table):
    table = dbHelper.query_table(table)
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

    table = ui.table(columns=db_columns, rows=db_rows).classes('col-span-full')
    with table.add_slot('top-right'):
        def toggle() -> None:
            table.toggle_fullscreen()
            button.props('icon=fullscreen_exit' if table.is_fullscreen else 'icon=fullscreen')

        button = ui.button('Toggle fullscreen', icon='fullscreen', on_click=toggle).props('flat')


# Header
with ui.header().style('background-color: #481E14').classes(replace='row items-center') as header:
    with ui.button(icon='menu').props('flat color=white'):
        with ui.menu() as menu:
            ui.menu_item('Settings')

# Left Drawer
with ui.left_drawer().style('background-color: #9B3922;').classes('text_center; items-center justify-between'):
    ui.label('Device List').style('color: #FFFFFF; font-size: 200%; font-weight: 400')

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
        ui.label('Second tab')

ui.run(dark=True)
