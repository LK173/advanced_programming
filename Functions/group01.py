"""
This module contains a `Group01` class, which represents agricultural output of several countries.

The `Group01` class has the following methods:

Methods:
-------
__init__(name):
    Initializes the object with the given name.

get_data():
    Downloads a CSV file containing agricultural total factor productivity data from
    this Github repository (https://github.com/owid/owid-datasets/tree/master/datasets),
    saves it into a downloads/ directory and reads the dataset into a pandas DataFrame.

get_countries():
    Returns a list of available countries in the dataset.

plot_quantity():
    Plots a heatmap of the correlation between all the columns in the Pandas
    DataFrame that end with the string '_quantity'.

plot_area_chart(country: str, normalize: bool):
    Plots an area chart of the distinct "_output_" columns
    for the given country or all countries if `country` is set to "World" or None.
    The columns are normalized by the total output if the `normalize` parameter
    is set to True.

plot_country_chart(args: Union[list[str], str]):
    Plots the total of the _output_ values of each
    selected country given by `country`, on the same chart with the
    X-axis being the Year.

gapminder_plot(year: int):
    Visualize Gapminder data for a specific year.

choropleth(self, year: int) -> None:
    Plots a choropleth map of the total factor productivity (tfp) for the given year

predictor(self, countries: list) -> None:
    Predicts the total factor productivity (tfp) by year for the given countries
    up to three until the year 2050.


Example usage:
--------------
    my_object = Group01("my_object")
    my_object.get_data()
    my_object.get_countries() # Output: ['Afghanistan', 'Albania', 'Algeria', ... 'Zimbabwe']
    my_object.plot_quantity()
    my_object.plot_area_chart("World", True)
    my_object.plot_country_chart("World", True)
    my_object.gapminder_plot("World", True)
    my_object.choropleth(1990)
    my_object.predictor(['Germany','France','Iraq'])
"""

import os
import warnings
from typing import Optional, Union
import pandas as pd
import requests
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import geopandas as gpd
from statsmodels.tsa.arima.model import ARIMA


class Group01:
    """
    A class to represent agricultural output of several countries.

    Attributes:
    ----------
    name : str
        name of the object

    df : pandas.DataFrame
        a pandas DataFrame containing the data

    Methods:
    -------
    get_data():
        Downloads a CSV file containing agricultural total factor productivity data from this Github
        repository (https://github.com/owid/owid-datasets/tree/master/datasets)

    get_countries():
        Returns a list of available countries in the dataset.

    plot_quantity():
        Plots a heatmap of the correlation between all the columns in the Pandas DataFrame that end
        with the string '_quantity'.

    plot_area_chart(country, normalize):
        Plots an area chart of the distinct "_output_" columns for the given country or all
        countries if `country` is set to "World" or None. The columns are normalized by the
        total output if the `normalize` parameter is set to True.

    plot_country_chart(args: Union[list[str], str]):
        Plots the total of the _output_ values of each selected country given by `country`, on the
        same chart with the X-axis being the Year.

    gapminder_plot(year: int):
        Visualize Gapminder data for a specific year.

    choropleth(self, year: int) -> None:
        Plots a choropleth map of the total factor productivity (tfp) for the given year

    predictor(self, countries: list) -> None:
        Predicts the total factor productivity (tfp) by year for the given
        countries up to three until the year 2050.
    """

    merge_dict = {
        "Bosnia and Herzegovina": "Bosnia and Herz.",
        "Burma": "Myanmar",
        "Eswatini": "eSwatini",
        "United States": "United States of America",
        "North Macedonia": "Macedonia",
        "Dominican Republic": "Dominican Rep.",
        "Equatorial Guinea": "Eq. Guinea",
        "South Sudan": "S. Sudan",
        "Democratic Republic of Congo": "Dem. Rep. Congo",
        "Solomon Islands": "Solomon Is.",
        "Timor": "Timor-Leste",
        "Central African Republic": "Central African Rep.",
        "Macedonia": "North Macedonia",
    }

    def __init__(self, name: str):
        """
        Initializes an instance of the Group01 class.

        Parameters:
            name: str, name of the object.
        """
        self.name = name
        self.df = None
        self.df_geographical = None

    def get_data(self) -> None:
        """
        This method downloads a CSV file containing agricultural total factor productivity data from
        this Github repository (https://github.com/owid/owid-datasets/tree/master/datasets) and
        saves it into a downloads/ directory in the root directory of the project (main project
        directory). If the data file already exists, the method does not download it again. The
        method also reads the dataset into a pandas DataFrame, which is stored as an attribute of
        the class. If the DataFrame already exists (i.e., has already been loaded), the method does
        not reload it.

        Parameters:
            None

        Raises:
            Exception: If there is an error while downloading the data file

        Returns:
            None

        Example usage:
            my_object = Group01("my_object")
            my_object.get_data()
        """

        url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Agricultural%20total%20factor%20productivity%20(USDA)/Agricultural%20total%20factor%20productivity%20(USDA).csv"

        if os.path.exists("downloads"):  # check if the downloads directory exists
            print("downloads directory already exists")
        else:
            print("creating downloads directory...")
            os.mkdir("downloads")  # create a downloads directory

        if os.path.exists("downloads/data.csv"):  # check if the data file exists
            print("data file already exists")
        else:
            print("downloading data file...")
            try:
                # get the data from url
                response = requests.get(url, timeout=60)
            except requests.exceptions.RequestException as e:
                print("Error: unable to download data file")
                print(e)
                return
                # exit the method

            print("saving data into file ... downloads/data.cs")
            with open("downloads/data.csv", "w", encoding="utf-8") as f:
                f.write(response.text)  # write the data to a csv file

        if self.df is None:
            print("reading data file into pandas dataframe...")
            self.df = pd.read_csv(
                "downloads/data.csv"
            )  # read the data into a pandas dataframe
            aggregated_columns = (
                "Caribbean",
                "Central Africa",
                "Central African Republic",
                "Central America",
                "Central Asia",
                "Central Europe",
                "Czechoslovakia",
                "Developed Asia",
                "Developed countries",
                "Former Soviet Union",
                "High income",
                "Horn of Africa",
                "Latin America and the Caribbean",
                "Least developed countries",
                "Low income",
                "Lower-middle income",
                "North Africa",
                "Northeast Asia",
                "Northern Europe",
                "South Asia",
                "Southeast Asia",
                "Southern Africa",
                "Southern Europe",
                "Sub-Saharan Africa",
                "Upper-middle income",
                "West Africa",
                "West Asia",
                "Western Europe",
                "World",
                "Yugoslavia",
            )
            self.df = self.df[~self.df["Entity"].isin(aggregated_columns)]

        if os.path.exists(
            "downloads/data_geographical.csv"
        ):  # check if the data file exists
            print("data_geographical file already exists")
        else:
            print("downloading data_geographical file...")
            df_geographical = gpd.read_file(
                gpd.datasets.get_path("naturalearth_lowres")
            )
            df_geographical.to_csv("downloads/data_geographical.csv")

        if self.df_geographical is None:
            print("reading data_geographical file into pandas geo dataframe...")
            self.df_geographical = gpd.read_file(
                gpd.datasets.get_path("naturalearth_lowres")
            )

    def get_countries(self) -> list:
        """
        Returns a list of available countries in the dataset.

        If the dataframe is not available, the method will first call the `get_data` method to
        download and read the dataset into the `df` attribute. Then it returns a list of unique
        countries in the 'Entity' column.

        Parameters:
            None

        Raises:
            None

        Returns:
            list: A list of unique countries in the dataset.

        Example usage:
            my_object = Group01("my_object")
            my_object.get_countries() # Output: ['Afghanistan', 'Albania', 'Algeria'...]

        """
        if self.df is None:
            self.get_data()  # check if df is available
        # return all countries in a list
        return self.df["Entity"].unique().tolist()

    def plot_quantity(self) -> None:
        """
        Plots a heatmap of the correlation between all the columns in the Pandas DataFrame that end
        with the string '_quantity'.

        If the DataFrame does not exist as an attribute of the class instance, the method calls the
        'get_data()' method to obtain the data.

        The method creates an empty list called 'plotted_columns', and loops through each column in
        the DataFrame, checking if the column name ends with the string '_quantity'. If a column
        name ends with '_quantity', the name is appended to the 'plotted_columns' list.

        Finally, the method calls the 'heatmap()' function from the seaborn library on the
        'plotted_columns' data in the DataFrame, and displays the lower triangle
        heatmap plot using 'plt.show()'.

        Parameters:
            None

        Raises:
            None

        Returns:
            None

        Example usage:
            my_object = Group01("my_object")
            my_object.plot_quantity()
        """
        # Check if self.df exists
        if self.df is None:
            self.get_data()

        plotted_columns = []

        # Loop through each column in the DataFrame
        for column in self.df.columns:
            # Check if the column name ends with '_quantity'
            if column.endswith("_quantity"):
                # Append the column name to the plotted_columns list
                plotted_columns.append(column)

        # Set the plot size and font scale
        plt.figure(figsize=(10, 8))
        sns.set(font_scale=1.2)

        # Getting the lower Triangle of the correlation matrix
        matrix = np.triu(self.df[plotted_columns].corr())

        # Create a correlation heatmap with all columns from the plotted_columns list
        sns.heatmap(
            self.df[plotted_columns].corr(),
            annot=True,
            cmap="crest",
            cbar_kws={"label": "Correlation Coefficient"},
            mask=matrix,
        )

        # Set the plot title and show the plot
        plt.title("Correlation between Quantity Columns")
        # Add the source of the data as a subtitle
        fig = plt.gcf()
        fig.suptitle(
            "Source: Agricultural total factor productivity (USDA), OWID",
            fontsize=10,
            y=-0.2,
        )
        # Show the plot
        plt.show()

    def plot_area_chart(
        self,
        country: Optional[str] = None,
        normalize: bool = False,
        optional: Optional[str] = None,
    ) -> None:
        """
        Plots an area chart of the distinct "_output_" columns for the given country or all
        countries if `country` is set to "World" or None. The columns are normalized by the total
        output if the `normalize` parameter is set to True.

        If the dataframe is not available, the method will first call the `get_data` method to
        download and read the dataset into the `df` attribute.

        Parameters:
        country (str, optional):
            The country to plot the data for. If set to "World" or None,
            the data for all countries will be plotted.

        normalize : bool
            If set to True, the data will be normalized by the total output.

        Raises:
            TypeError: If the `country` parameter is not a string or the `normalize`
            parameter is not a bool

            Exception: If one or less columns with the "_output_" suffix are available or if the
            given country does not exist

        Returns:
            None

        Example usage:
            my_object = Group01("my_object")
            my_object.plot_area_chart("World", True)
        """

        if country is not None and not isinstance(country, str):
            raise TypeError("country is not a string, Please pass a string")

        if not isinstance(normalize, bool):
            raise TypeError("normalize is not a bool, Please pass a bool")

        if self.df is None:
            self.get_data()

        # Get all columns with "_quantity" suffix and check if there are enough columns
        column_names = self.df.columns.tolist()
        df_subset = [c for c in column_names if "_output_" in c]
        df_subset.append("Year")
        if len(df_subset) < 2:
            raise Exception("Not enough columns with '_output' suffix")

        # Plotting function
        def country_plot(df_temp):
            norm = ""
            if normalize:
                df_temp["Total"] = (df_temp.iloc[:, :-1]).sum(axis=1)
                df_temp.iloc[:, :-2] = (
                    df_temp.iloc[:, :-2].div(df_temp.Total, axis=0) * 100
                )
                norm = "% (Normalized)"
            list_outputs = []
            list_labels = []
            for each in df_subset[:-1]:
                list_outputs.append(df_temp[each])
                list_labels.append(each)
            plt.stackplot(df_temp.Year, list_outputs, labels=list_labels)
            plt.set_cmap("Pastel1")
            plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
            plt.tick_params(labelsize=12)
            plt.title("Consumption of agricultural products by country over time, O")
            # Add the source of the data as a subtitle
            fig = plt.gcf()
            fig.suptitle(
                "Source: Agricultural total factor productivity (USDA), OWID",
                fontsize=10,
                y=-0.05,
            )
            plt.xlabel("Year", size=12)
            plt.ylabel(("Counsumption" + norm), size=12)
            plt.ylim(bottom=0)
            # Show the plot
            plt.show()

        # Plotting for all countries or a specific country
        if country in (None, "World"):
            df_temp = self.df[df_subset].groupby("Year").sum().reset_index()
            df_temp = df_temp.reindex(
                columns=list(df_temp.columns[1:]) + [df_temp.columns[0]]
            )
            country_plot(df_temp)
        elif country in self.get_countries():
            df_temp = self.df[self.df["Entity"] == country]
            df_temp = df_temp[df_subset]
            country_plot(df_temp)
        else:
            raise TypeError("Country does not exist")

    def plot_country_chart(self, args: Union[list[str], str]) -> None:
        """
        Plots the total of the _output_ values of each selected country given by `country`,
        on the same chart with the X-axis being the Year.

        Parameters:
        args : list
            A list of countries to plot

        Raises:
            TypeError: If the input is not a string or a list of strings

        Returns:
            None

        Example usage:
            my_object = Group01("my_object")
            my_object.plot_country_chart("World", True)
        """
        title = "Plot of total _output_ values of "

        if (not isinstance(args, list)) and (not isinstance(args, str)):
            raise TypeError(
                "args is not a list or a string. Please pass a list or a string."
            )

        if self.df is None:
            self.get_data()  # check if df is available
        # Get all columns with "_output"
        column_names = self.df.columns.tolist()
        df_subset = [c for c in column_names if "_output_" in c]
        df_subset.append("Year")

        def country_plot(country):
            df_temp = self.df[self.df["Entity"] == country]
            df_temp = df_temp[df_subset]
            df_temp["Total"] = (df_temp[:-1]).sum(axis=1)
            plt.plot(df_temp["Year"], df_temp["Total"], label=country)
            plt.legend()

        if isinstance(args, str):  # pass a string
            if args in self.get_countries():
                country_plot(args)
                title += args
            else:
                raise ValueError("Country does not exist")
        elif all(isinstance(each, str) for each in args):  # list
            for each in args:
                if each in self.get_countries():
                    country_plot(each)
                    title += each + ", "
                else:
                    raise TypeError("Country does not exist")
        else:
            raise TypeError("Please pass a country string or countries list")

        plt.title(title)
        # Add the source of the data as a subtitle
        fig = plt.gcf()
        fig.suptitle(
            "Source: Agricultural total factor productivity (USDA), OWID",
            fontsize=10,
            y=-0.05,
        )
        plt.xlabel("Year")
        plt.ylabel("Total _output")
        # Show the plot
        plt.show()

    def gapminder(self, year: int, log_scale: bool = False) -> None:
        """
        Visualize Gapminder data for a specific year.

        This function generates a scatter plot that shows the relationship between fertilizer
        quantity and output quantity for agriculture in a specific year. The size of each point
        represents the animal output quantity, which is assumed to be an indicator of the size of
        the agricultural operation.

        Parameters:
        year : int
            The year for which to visualize the data.
        log_scale : bool, optional (default=False)
            If True, the x and y axis will be displayed in logarithmic scale.
        Raises:
        TypeError
            If the received argument is not an int or if it's negative.
        ValueError
            If the year is not present in the dataset.

        Returns:
            None

        Example usage:
            my_object = Group01("my_object")
            my_object.gapminder_plot(2000, True)
        """
        if not isinstance(year, int) or year < 0:
            raise TypeError("Please pass a positive integer for year")

        if self.df is None:
            self.get_data()  # check if df is available

        if year not in self.df["Year"].unique():
            raise ValueError(f"{year} is not present in the dataset")

        # Increase the graph size
        plt.figure(dpi=150)

        # Filter data by year
        year_data = self.df[self.df["Year"] == year]

        # Store animal_output_quantity as a numpy array: np_pop
        # Exploratory analysis showed that animal_output_quantity is the most relevant variable
        # regarding their correlation with fertilizer_quantity and output_quantity
        np_pop = np.array(year_data["animal_output_quantity"])
        np_pop2 = np_pop * 2

        # Create a scatter plot
        sns.scatterplot(
            x="fertilizer_quantity",
            y="output_quantity",
            data=year_data,
            legend=True,
            size=np_pop2,
            sizes=(20, 400),
            alpha=0.5,
        )

        # Use seaborn scatterplot for better customization
        plt.grid(True)
        plt.xlabel("fertilizer_quantity", fontsize=14)
        plt.ylabel("output_quantity", fontsize=14)
        plt.title(f"Gapminder agriculture - Year {year}", fontsize=20)
        # Add the source of the data as a subtitle
        fig = plt.gcf()
        fig.suptitle(
            "Source: Agricultural total factor productivity (USDA), OWID",
            fontsize=10,
            y=-0.05,
        )

        if log_scale:
            plt.xscale("log")
            plt.yscale("log")
            plt.xlabel("fertilizer_quantity_log", fontsize=14)
            plt.ylabel("output_quantity_log", fontsize=14)

        plt.show()

    def choropleth(self, year: int) -> None:
        """
        Plots a choropleth map of the total factor productivity (tfp) for the given year

        Parameters:
        year : int
            The year for which to plot the tfp

        Raises:
            TypeError: If the input year is not an integer
            ValueError: If the self.df or self.df_geographical attributes are None
            ValueError: If year is not in the dataset

        Returns:
            None

        Example usage:
            my_object.choropleth(2000)
        """
        # Check that year is an integer
        if not isinstance(year, int):
            raise TypeError("Year must be an integer")

        # Check if self.df or self.df_geographical attributes are None and call
        # self.get_data() if necessary
        if (self.df is None) or (self.df_geographical is None):
            self.get_data()

        # Check if year is in the dataset
        if year not in self.df["Year"].values:
            raise ValueError("Year is not in the dataset")

        # Rename country in self.df according to merge_dict
        self.df = self.df.replace({"Entity": Group01.merge_dict})

        # Merge geographical and agricultural dataframe and filter by selected year
        merged_df = self.df_geographical.merge(
            self.df, left_on="name", right_on="Entity", how="left"
        )
        merged_df = merged_df[merged_df["Year"] == year]

        # Plot choropleth map of tfp
        ax = merged_df.plot(
            column="tfp",
            legend=True,
            figsize=[20, 10],
            legend_kwds={"label": "total factor productivity"},
        )
        ax.set_title(f"Total factor productivity in {year}")
        plt.xlabel("Longitude", fontsize=14)
        plt.ylabel("Latitude", fontsize=14)
        # Add the source of the data as a subtitle
        fig = plt.gcf()
        fig.suptitle(
            "Sources: Natural Earth powered by WordPress and Agricultural total factor productivity (USDA), OWID",
            fontsize=10,
            y=-0.05,
        )
        # Show the plot
        plt.show()

    def predictor(self, countries: list) -> None:
        """
        Plots the Total Factor Productivity (TFP) of the given countries
        and predicts TFP up to 2050 using ARIMA. Arima is used instead of
        SARIMAX because it was no seasonality in the data. It was checked by
        plotting ACF and PACF plots and by checking the seasonal decomposition
        plot. It is oserved by the autocorrelation that the time series of the
        data does show a long-term trend or systematic patterns that could affect
        its statistical properties. Thats why we have to use the differencing
        parameter 'd' to remove the trend and make the data stationary and smooth
        the variance and mean. It is important becasue an accurate prediction can
        only be made for stationary series, since the data are otherwise randomly
        distributed and randomness cannot be forecasted.

        The order of the autoregressive (AR) component parameter 'p' is set to 20.
        The degree of differencing (I) parameter 'd' is set to 2.
        The order of the moving average (MA) component parameter 'q' is set to 2.

        Parameters:
            countries (list): A list of up to three country names to plot.

        Raises:
            TypeError: If the received argument is not a list.
            ValueError: If the agricultural data has not been loaded yet.
            ValueError: If no valid countries are provided.
            ValueError: If more than three countries are provided.

        Returns:
            None

        Example usage:
            my_object = Group01("my_object")
            my_object.predictor(['United States', 'China', 'India'])

        """
        warnings.filterwarnings("ignore")

        if not isinstance(countries, list):
            raise TypeError(
                "No valid type as an argument. Please insert the names of countries as a list into the method."
            )

        if self.df is None:
            self.get_data()  # check if df is available

        available_countries = set(self.df["Entity"].unique())

        # Select the countries that are in the available countries
        countries_to_use = [
            country for country in countries if country in available_countries
        ]
        if not countries_to_use:
            # Raise an error if no valid countries are provided
            raise ValueError(
                f"No valid countries provided. Available countries are: {', '.join(available_countries)}"
            )

        if len(countries) > 3:
            # Raise an error if more than three countries are provided
            raise ValueError("Maximum of three countries can be provided.")

        fig, ax = plt.subplots(figsize=(12, 8))

        for country in countries_to_use:
            # Select the data for the current country
            data = self.df[self.df["Entity"] == country]
            # Extract the TFP and years values
            tfp = data["tfp"].values
            years = data["Year"].values
            # Plot the TFP for the current country
            ax.plot(years, tfp, label=country)
            # Fit an ARIMA model to the TFP data for the current country
            model = ARIMA(tfp, order=(20, 2, 2))
            model_fit = model.fit()
            # Generate predictions for TFP up to 2050
            predictions = model_fit.forecast(steps=31)
            # Plot the predicted TFP using a different line style
            ax.plot(
                np.arange(years[-1], years[-1] + 31),
                predictions,
                linestyle="--",
                color=ax.get_lines()[-1].get_color(),
                label=f"{country} (forecast)",
            )

        # Set the title and legend for the plot
        ax.set_title("Total Factor Productivity (TFP) by Year")
        plt.xlabel("Year", fontsize=14)
        plt.ylabel("Total Factor Productivity", fontsize=14)
        ax.legend()
        # Add the source of the data as a subtitle
        fig = plt.gcf()
        fig.suptitle(
            "Source: Agricultural total factor productivity (USDA), OWID",
            fontsize=10,
            y=-0.05,
        )
        # Show the plot
        plt.show()
