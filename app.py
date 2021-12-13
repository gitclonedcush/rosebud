from dash import html, dcc

from config import app
from page_header import page_header
from page_body import page_body

ROSEBUD_LOGO = "popcorn.svg"

server = app.server

app.layout = html.Div(children=[
	page_header(app.get_asset_url(ROSEBUD_LOGO)),
	page_body(),
	dcc.Store(id='genre-store'),
	dcc.Store(id='ratings-store'),
	dcc.Store(id='selected-genre')
])


if __name__ == '__main__':
    app.run_server(debug=True)
