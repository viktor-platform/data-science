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
import pandas as pd
from viktor.parametrization import FileField
from viktor.parametrization import NumberField
from viktor.parametrization import OptionField
from viktor.parametrization import Page
from viktor.parametrization import Parametrization


def get_possible_columns(params, **kwargs):
    if params.csv_file:
        buffer = params.csv_file.file.open_binary()
        df = pd.read_csv(buffer)
        buffer.close()
        return df.columns.values.tolist()
    return ['First upload a CSV file']


class ProjectParametrization(Parametrization):

    """Defines the input fields in left-side of the web UI in the Sample entity (Editor)."""
    csv_page = Page('CSV visualization', views='csv_visualization')
    csv_page.file_link = FileField('CSV file', name='csv_file', file_types=['.csv'])
    csv_page.options_x = OptionField('x axis', name='xaxis', options=get_possible_columns)
    csv_page.options_y = OptionField('y axis', name='yaxis', options=get_possible_columns)
    plotly_express_page = Page('Plotly', views='plotly_gapminder_visualization')
    plotly_express_sunburst = Page('Plotly 2', views='plotly_sunburst_visualization')
    plotly_express_sunburst.year = NumberField('year', min=1952, max=2007, step=5, default=2007, variant='slider')
    numpy_interp = Page('Numpy interpolation', views='numpy_interpolate')
    numpy_interp.
    iris_page = Page('Iris visualization', views='iris_visualization')
    boxplot_page = Page('Boxplot visualization', views='boxplot_visualization')
    correllogram_page = Page('Correllogram visualization', views='correllogram_visualization')
    car_mileage_page = Page('Car Mileage visualization', views='car_mileage_visualization')
