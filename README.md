# Welcome to project Agros

## TEAM: 
- Carl Krogmann     
    - 55361
    - 55361@novasbe.pt
    - carl.krogmann@hotmail.com
- Leon Kahrig
    - 55584
    - 55584@novasbe.pt
    - leonkahrig@web.de
- Meeka Lenisa
    - 56025
    - 56025@novasbe.pt
    - 118310340+meekalenisa@users.noreply.github.com
- Jannis Schmid
    - 54616
    - 54616@novasbe.pt
    - jannishsgph@gmail.com

---
## Scenario

We are participating in a two-day hackathon promoted to study the agricultural output of several countries. We expect to contribute to the green transition by having a more savvy taskforce. We decided to create a python class for the challenge.


## Structure of the repository
The structure of the repository is as follows. The main directory of the project contains the Showcase notebook, and the configuration files (.yml, .gitignore, .md and LICENSE). The python (.py) files with the methods and classes used in the Showcase notebook are kept in the Functions directory. The dataset used is stored in the Data directory. Other prototyping notebooks are kept in the testing directory. 


### Data

For this project, we used data from [Our World in Data](https://ourworldindata.org/). The dataset can be found [here](https://github.com/owid/owid-datasets/blob/master/datasets/Agricultural%20total%20factor%20productivity%20(USDA)/Agricultural%20total%20factor%20productivity%20(USDA).csv).

### Structure of the methods 
All of the following methods are contained in the class Group01, and the analyses are made in the Showcase notebook.

#### Downloading and Reading the Data

In the project, we create a method to download the data file from Our World in Data and store it in a downloads/ directory in the root directory of the project. If the data file already exists, the method does not download it again. We then develop another method to read the dataset into a pandas dataframe, which is an attribute of our class. These methods are implemented successfully and allow us to begin our analysis.

#### Available Countries in the Dataset

To identify the countries available in the dataset, we develop a method that outputs a list of the available countries. This method is useful in identifying the countries that we want to analyze.

####  Correlation between the "_quantity" Columns

We also develop a method that allows us to plot a way to correlate the "_quantity" columns. This is useful in identifying any correlations between the different variables and providing insights into how the different variables affect each other.

#### Area Chart of the Distinct "_output_" Columns

Another method that we develop allows us to plot an area chart of the distinct "output" columns. This method has two arguments, a country argument, and a normalize argument. The former, when receiving NONE or 'World', plots the sum for all distinct countries. The latter, if True, normalizes the output in relative terms: each year, output should always be 100%. The X-axis is the Year. The method returns a ValueError when the chosen country does not exist. This method is useful in identifying the trends in agricultural output for different countries.

#### Comparison of the Total Output for Chosen Countries

We also develop a method that can receive a string with a country or a list of country strings. This method compares the total of the "output" columns for each of the chosen countries and plots it, so a comparison can be made. The X-axis is the Year. This method is useful in comparing the agricultural output of different countries.

#### Gapminder Method

The next method that we develop is called gapminder. This method receives an argument year which has to be an int. If the received argument is not an int, the method raises a TypeError. This method plots a scatter plot where x is fertilizer_quantity, y is output_quantity, and the area of each dot is a third relevant variable we found with exploration of the data. This method is useful in identifying any relationships between different variables.

### Choropleth

We also develop a choropleth method which receives a year as input and plots the tfp variable on a world map using geopandas and a colorbar. We merge the agricultural data with the geodata on the countries and make a variable called merge_dict, which is a dictionary that renames 13 countries.

### Predictor 

Lastly, we develop a predictor method that receives up to three countries as input. If one or more countries on the list are not present in the Agricultural dataframe, they are ignored. If none are present, an error message is raised reminding the user what countries are available. It then plots the TFP and makes a prediction up to 2050.

#### Showcase Notebook

To showcase our analysis, we created a "showcase notebook" where we imported our Class and showcased all the methods we developed. In the showcase notebook, we told a story about our analysis and findings.

####  Analysis and Findings

Using the gapminder plot for the most recent year, we analyzed the world's agricultural production and found that it was increasing steadily. We then chose three countries, one from each continent, and used the fourth method to illustrate each country's agricultural output. We pointed out the main differences between the countries and found that each country had a unique pattern of agricultural output. Next, we used the fifth method to illustrate each country's output and identified the main differences between them. We found that each country had its strengths and weaknesses in terms of agricultural output. We then ran the third method to analyze the correlation between the different variables and found that there was a strong positive correlation between fertilizer quantity and output quantity. Finally, we analyzed the relationship between quantities and outputs and found that there was a positive relationship between the two. Overall, our analysis provided valuable insights into the agricultural sector, and our methods were successful in analyzing the data.


## Running the Virtual Environment
In order to run the virtual environment, it is suggested to load the virtual environment provided. Follow these steps to activate with conda:
1. Install conda and pip if you haven't already done so.
2. Navigate to the file source location.
3. Ensure you are currently in the base directory by running the command `conda deactivate`.
4. Create a virtual environment by running the command `conda env create -f group_01.yml`. 
5. Activate the virtual environment by running the command `conda activate group_01`.
6. Open in Jupyter lab by running the command `jupyterlab`.