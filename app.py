import dash
from layout.layout import create_layout, callback_dropdown_estados
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = create_layout()

callback_dropdown_estados(app)

if __name__ == "__main__":
    app.run_server(debug=True)
