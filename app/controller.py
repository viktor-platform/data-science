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
from pathlib import Path

import math
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
from viktor import UserError
from viktor.core import ViktorController, File
from viktor.result import DownloadResult
from viktor.views import DataGroup
from viktor.views import DataItem
from viktor.views import ImageAndDataResult 
from viktor.views import ImageAndDataView 
from viktor.views import ImageResult
from viktor.views import ImageView
from viktor.views import PlotlyResult
from viktor.views import PlotlyView

from .parametrization import Parametrization


class Controller(ViktorController):
    label = "Data"
    parametrization = Parametrization

    @ImageView("Results", duration_guess=4)
    def csv_visualization(self, params, **kwargs):
        """Reads csv file and plots its data."""
        if not params.csv_page.file_link:
            raise UserError('Upload a CSV file and define its axis\'')

        try:
            buffer = params.csv_page.file_link.file.open_binary()
            dataframe = pd.read_csv(buffer)
            fig, ax = plt.subplots()
            dataframe.plot(kind='scatter', x=params.csv_page.options_x, y=params.csv_page.options_y, ax=ax)

            for k, row in dataframe.iterrows():
                txt_first_column = row.iloc[0]  # the text is equal to the first column
                ax.text(x=row[params.csv_page.options_x], y= row[params.csv_page.options_y], s= txt_first_column)

        except ValueError as err:
            raise UserError(err)

        buffer.close()

        png_buffer = BytesIO()
        plt.savefig(png_buffer, format="png")
        return ImageResult(png_buffer)

    @PlotlyView("Results", duration_guess=3)
    def plotly_visualization(self, params, **kwargs):
        """Use the build-in gapminder dataset from plotly to create a plot."""
        dataframe = px.data.gapminder()
        fig = px.scatter(dataframe, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
                         size="pop", color="continent", hover_name="country", facet_col="continent",
                         log_x=True, size_max=45, range_x=[100, 100000], range_y=[25, 90])
        return PlotlyResult(fig.to_json())

    @ImageAndDataView ("Results", duration_guess=3)
    def numpy_interpolate(self, params, **kwargs):
        """This is an example of how numpy and matplotlib can be used with viktor
          In this example numpy is used to pick samples from a sin function and plot an interpolation with a
          given order polynomial."""
        x_value = np.linspace(0, 2 * np.pi, params.numpy_interp.linspace)
        pol_x = np.linspace(0, 2 * np.pi, 100)

        # Interpolate over sinus curve
        polyfit = np.polyfit(x_value, np.sin(x_value), params.numpy_interp.polynomial)
        polyfit_function = np.poly1d(polyfit)
        y_interpolated = polyfit_function(params.numpy_interp.x)

        # Plot figure using matplotlib
        plt.figure()
        plt.plot(x_value, np.sin(x_value))
        plt.scatter([params.numpy_interp.x], [y_interpolated])
        plt.axvline(params.numpy_interp.x, linestyle='--', color='red')
        if params.numpy_interp.show_graph:
            plt.plot(pol_x, polyfit_function(pol_x))

        figure_buffer = BytesIO()
        plt.savefig(figure_buffer, format="png")

        # Create data group
        data_group = DataGroup(
            DataItem(label='Y-interpolated', value=y_interpolated, number_of_decimals=4),
            DataItem(label='Y-calculated', value=math.sin(params.numpy_interp.x), number_of_decimals=4),
            DataItem(label='Error', value=np.abs(y_interpolated - math.sin(params.numpy_interp.x)), number_of_decimals=4)
        )
        return ImageAndDataResult(figure_buffer, data_group)

    @ImageView("Results", duration_guess=1)
    def correlation_map(self, params, **kwargs):
        """ In this example, we show how to use pandas and matplotlib with VIKTOR.
        Here, pandas is used to parse a database of props_material types, that is then used to create a correlation
        matrix that is visualized with matplotlib."""
        # Set a random seed for reproducibility
        columns = params.correlation_matrix.types
        
        # Generate a random pandas DataFrame
        data = pd.DataFrame(np.random.rand(10, len(columns)), columns=columns)

        # Calculate the correlation matrix
        corr_matrix = data.corr()

        # Plotting the correlation matrix
        plt.figure(figsize=(8, 6))
        plt.imshow(corr_matrix, cmap='coolwarm', interpolation='nearest')
        plt.colorbar()
        plt.xticks(range(len(corr_matrix)), corr_matrix.columns, rotation='vertical')
        plt.yticks(range(len(corr_matrix)), corr_matrix.columns)
        plt.title('Correlation Matrix')
        figure_buffer = BytesIO()
        plt.savefig(figure_buffer, format="png")
        return ImageResult(figure_buffer)

    def download_props_material_csv(self):
        """ Download the props_material CSV dataset"""
        file_path = Path(__file__).parent / 'datasets' / 'props_material.csv'
        file = File.from_path(file_path)
        return DownloadResult(file, 'props_material.csv')
