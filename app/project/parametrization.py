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
import math

import pandas as pd
from viktor.parametrization import BooleanField
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
    numpy_interp = Page('Numpy interpolation', views='numpy_interpolate')
    numpy_interp.x = NumberField('x', min=0, max=6.2, step=0.1, default=0, variant='slider')
    numpy_interp.polynomial = NumberField('polynomial for interpolation', min=0, max=30, step=1, default=8,
                                          variant='slider')
    numpy_interp.linspace = NumberField('number of samples', min=4, max=15, step=1, default=6, variant='slider')
    numpy_interp.show_graph = BooleanField('show interpolation', default=True)
    pokemon_pandas = Page('Pokemon with pandas', views='pokemon_type_chord_diagram')
