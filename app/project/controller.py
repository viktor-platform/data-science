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

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
from viktor import UserException
from viktor.core import ViktorController
from viktor.views import PNGResult
from viktor.views import PNGView
from viktor.views import PlotlyResult
from viktor.views import PlotlyView

from .parametrization import ProjectParametrization


class ProjectController(ViktorController):
    """Controller class which acts as interface for the Sample entity type."""
    label = "Sample"
    parametrization = ProjectParametrization
    viktor_convert_entity_field = True

    @PlotlyView("Results", duration_guess=3)
    def csv_visualization(self, params, **kwargs):
        if not params.csv_file:
            raise UserException('Upload a CSV file and define its axis\'')
        buffer = params.csv_file.file.open_binary()
        df = pd.read_csv(buffer)
        try:
            fig = px.line(df, x=params.xaxis, y=params.yaxis)
        except ValueError as err:
            raise UserException(err)

        buffer.close()
        return PlotlyResult(fig.to_json())

    @PlotlyView("Results", duration_guess=3)
    def plotly_gapminder_visualization(self, params, **kwargs):
        df = px.data.gapminder()
        fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
                         size="pop", color="continent", hover_name="country", facet_col="continent",
                         log_x=True, size_max=45, range_x=[100, 100000], range_y=[25, 90])
        return PlotlyResult(fig.to_json())

    @PlotlyView("Results", duration_guess=3)
    def plotly_sunburst_visualization(self, params, **kwargs):
        df = px.data.gapminder().query(f'year == {params.plotly_express_sunburst.year}')
        fig = px.sunburst(df, path=['continent', 'country'], values='pop',
                          color='lifeExp', hover_data=['iso_alpha'])
        return PlotlyResult(fig.to_json())

    @PlotlyView("Results", duration_guess=3)
    def plotly_sunburst_visualization(self, params, **kwargs):
        df = px.data.gapminder().query(f'year == {params.plotly_express_sunburst.year}')
        fig = px.sunburst(df, path=['continent', 'country'], values='pop',
                          color='lifeExp', hover_data=['iso_alpha'])
        return PlotlyResult(fig.to_json())

    @PlotlyView("Results", duration_guess=3)
    def iris_visualization(self, params, **kwargs):
        df = px.data.iris()  # replace with your own data source
        fig = px.scatter_matrix(
            df, color="species")
        return PlotlyResult(fig.to_json())

    @PNGView("Results", duration_guess=3)
    def boxplot_visualization(self, params, **kwargs):
        df = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/mpg_ggplot2.csv")
        # Create Fig and gridspec
        fig = plt.figure(figsize=(16, 10), dpi=80)
        grid = plt.GridSpec(4, 4, hspace=0.5, wspace=0.2)

        # Define the axes
        ax_main = fig.add_subplot(grid[:-1, :-1])
        ax_right = fig.add_subplot(grid[:-1, -1], xticklabels=[], yticklabels=[])
        ax_bottom = fig.add_subplot(grid[-1, 0:-1], xticklabels=[], yticklabels=[])

        # Scatterplot on main ax
        ax_main.scatter('displ', 'hwy', s=df.cty * 5, c=df.manufacturer.astype('category').cat.codes, alpha=.9, data=df,
                        cmap="Set1", edgecolors='black', linewidths=.5)

        # Add a graph in each part
        sns.boxplot(df.hwy, ax=ax_right, orient="v")
        sns.boxplot(df.displ, ax=ax_bottom, orient="h")

        # Decorations ------------------
        # Remove x axis name for the boxplot
        ax_bottom.set(xlabel='')
        ax_right.set(ylabel='')

        # Main Title, Xlabel and YLabel
        ax_main.set(title='Scatterplot with Histograms \n displ vs hwy', xlabel='displ', ylabel='hwy')

        # Set font size of different components
        ax_main.title.set_fontsize(20)
        for item in (
                [ax_main.xaxis.label, ax_main.yaxis.label] + ax_main.get_xticklabels() + ax_main.get_yticklabels()):
            item.set_fontsize(14)
        f = io.BytesIO()
        plt.savefig(f, format="png")
        return PNGResult(f)

    @PNGView("Results", duration_guess=3)
    def correllogram_visualization(self, params, **kwargs):
        df = pd.read_csv("https://github.com/selva86/datasets/raw/master/mtcars.csv")

        # Plot
        plt.figure(figsize=(12, 10), dpi=80)
        sns.heatmap(df.corr(), xticklabels=df.corr().columns, yticklabels=df.corr().columns, cmap='RdYlGn', center=0,
                    annot=True)

        # Decorations
        plt.title('Correlogram of mtcars', fontsize=22)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        f = io.BytesIO()
        plt.savefig(f, format="png")
        return PNGResult(f)

    @PNGView("Results", duration_guess=3)
    def car_mileage_visualization(self, params, **kwargs):
        df = pd.read_csv("https://github.com/selva86/datasets/raw/master/mtcars.csv")
        x = df.loc[:, ['mpg']]
        df['mpg_z'] = (x - x.mean()) / x.std()
        df['colors'] = ['red' if x < 0 else 'green' for x in df['mpg_z']]
        df.sort_values('mpg_z', inplace=True)
        df.reset_index(inplace=True)

        # Draw plot
        plt.figure(figsize=(14, 10), dpi=80)
        plt.hlines(y=df.index, xmin=0, xmax=df.mpg_z, color=df.colors, alpha=0.4, linewidth=5)

        # Decorations
        plt.gca().set(ylabel='$Model$', xlabel='$Mileage$')
        plt.yticks(df.index, df.cars, fontsize=12)
        plt.title('Diverging Bars of Car Mileage', fontdict={'size': 20})
        plt.grid(linestyle='--', alpha=0.5)
        f = io.BytesIO()
        plt.savefig(f, format="png")
        return PNGResult(f)
