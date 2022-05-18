"""Copyright (c) 2022 VIKTOR B.V.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

VIKTOR B.V. PROVIDES THIS SOFTWARE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import io
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from viktor import UserException
from viktor.core import ViktorController
from viktor.result import DownloadResult
from viktor.views import DataGroup
from viktor.views import DataItem
from viktor.views import PNGResult
from viktor.views import PNGView
from viktor.views import PlotlyAndDataResult
from viktor.views import PlotlyAndDataView
from viktor.views import PlotlyResult
from viktor.views import PlotlyView

from .parametrization import ProjectParametrization


class ProjectController(ViktorController):
    """Controller class which acts as interface for this entity type."""
    label = "Data"
    parametrization = ProjectParametrization
    viktor_convert_entity_field = True

    @PNGView("Results", duration_guess=3)
    def csv_visualization(self, params, **kwargs):
        """Reads csv file and plots its data."""
        if not params.csv_page.file_link:
            raise UserException('Upload a CSV file and define its axis\'')

        try:
            buffer = params.csv_page.file_link.file.open_binary()
            df = pd.read_csv(buffer)
            df.plot(kind='scatter', x=params.csv_page.options_x, y=params.csv_page.options_y)
        except ValueError as err:
            raise UserException(err)

        buffer.close()

        png_buffer = io.BytesIO()
        plt.savefig(png_buffer, format="png")
        return PNGResult(png_buffer)

    @PlotlyView("Results", duration_guess=3)
    def plotly_visualization(self, params, **kwargs):
        """Use the build-in gapminder dataset from plotly to create a plot."""
        df = px.data.gapminder()
        fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
                         size="pop", color="continent", hover_name="country", facet_col="continent",
                         log_x=True, size_max=45, range_x=[100, 100000], range_y=[25, 90])
        return PlotlyResult(fig.to_json())

    @PlotlyAndDataView("Results", duration_guess=3)
    def numpy_interpolate(self, params, **kwargs):
        """Picks samples from a sin function and plots an interpolation with a given polynomial"""
        x = np.linspace(0, 2 * np.pi, params.numpy_interp.linspace)
        pol_x = np.linspace(0, 2 * np.pi, 100)

        # Interpolate over sinus curve
        polyfit = np.polyfit(x, np.sin(x), params.numpy_interp.polynomial)
        polyfit_function = np.poly1d(polyfit)
        y_interpolated = polyfit_function(params.numpy_interp.x)

        # Create plotly figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=np.sin(x), name='Sin curve samples', mode='lines+markers'))
        fig.add_scatter(x=[params.numpy_interp.x], y=[y_interpolated], name='Intersection', line_color='black')
        fig.add_vline(params.numpy_interp.x, line_color='cyan')
        if params.numpy_interp.show_graph:
            fig.add_trace(go.Scatter(x=pol_x, y=polyfit_function(pol_x), name='Interpolation', mode='lines',
                                     marker_color='red'))

        # Create data group
        data_group = DataGroup(
            DataItem(label='Y-interpolated', value=y_interpolated, number_of_decimals=4),
            DataItem(label='Y-calculated', value=math.sin(params.numpy_interp.x), number_of_decimals=4),
            DataItem(label='Error', value=np.abs(y_interpolated - math.sin(params.numpy_interp.x)),
                     number_of_decimals=4)
        )
        return PlotlyAndDataResult(fig.to_json(), data_group)

    @PNGView("Results", duration_guess=4)
    def pokemon_type_heat_map(self, params, **kwargs):
        """ Using the Pokemon database to create a correlation matrix en plots a heatmap"""
        possible_types = params.pokemon_pandas.types
        n_types = len(possible_types)

        if n_types < 2:
            raise UserException("Please select more then 1 pokemon type as input. Click on Select all to see the"
                                "full figure.")

        df = pd.read_csv(Path(__file__).parent / 'datasets' / 'pokemon.csv').dropna()

        # Create correlation matrix
        matrix = [[0 for _ in range(n_types)] for _ in range(n_types)]
        for i in range(n_types):
            for j in range(n_types):
                if i != j:
                    connection_between_types = (
                            df[(df['Type.1'] == possible_types[i]) & (df['Type.2'] == possible_types[j])].count()[0] +
                            df[(df['Type.1'] == possible_types[j]) & (df['Type.2'] == possible_types[i])].count()[0]
                    )
                    matrix[i][j] = np.round(connection_between_types / df.shape[0] * 100, 2)

        # Plot figure
        plt.figure(figsize=(12, 10), dpi=80)
        sns.heatmap(matrix, xticklabels=possible_types, yticklabels=possible_types,
                    cmap=sns.cubehelix_palette(as_cmap=True), annot=True)
        plt.title('% of pokemon having both types', fontsize=22)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        f = io.BytesIO()
        plt.savefig(f, format="png")
        return PNGResult(f)

    def download_pokemon_csv(self):
        """ Download the Pokemon CSV dataset"""
        pokemon_file_path = Path(__file__).parent / 'datasets' / 'pokemon.csv'
        pokemon_file_buffer = io.BytesIO()
        with open(pokemon_file_path, "rb") as pokemon_file:
            pokemon_file_buffer.write(pokemon_file.read())
        return DownloadResult(pokemon_file_buffer, 'pokemon.csv')
