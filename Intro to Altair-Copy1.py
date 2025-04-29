#!/usr/bin/env python
# coding: utf-8

# <h1>An Introduction to Altair</h1>

# <i>Fundamentals of Visualization with Dr. Danielle Albers Szafir</i>
# 
# This is a notebook that is intended to introduce us to Altair, a version of Vega-Lite that we can build in Python using notebooks. Blue cells indicate markdown, where we can use HTML-like syntax to insert information as if the notebook is a normal webpage. 

# To insert Markdown, simply go to "Cell" and select "Cell Type" then "Markdown." The color of the cell border will turn blue. You can hit shift+enter to run the cell and double click the cell to edit.  

# The tutorial we'll go through for today is based on Marian Dork's InfoVis course from the University of Applied Sciences Potsdam: https://infovis.fh-potsdam.de/tutorials/

# <h2> Getting started with Altair

# For this activity, I assume you know some basic Python. If you don't, don't worry. You are welcome to do some tutorials, but most of the basic syntax that we'll need for Altair looks like the same syntax as Java or Javascript. We will explore Altair basics using the [2016 World Happiness Dataset](https://www.kaggle.com/unsdsn/world-happiness) from Kaggle. Make sure to download the dataset from Coursera before getting started.

# In[1]:


# Import our data processing library (note: you may have to install this!)
import pandas as pd

# Let's use this to upload a sample dataset and show the start of the dataset
# Note that you need to download the dataset and make sure it's in the same 
# directory as your notebook
data= pd.read_csv("World_Happiness_2016.csv")
data.head()


# In[2]:


# Now let's visualize the data
import altair as alt

alt.Chart(data).mark_bar().encode(x="Region", y="Happiness Score")


# Test Your Knowledge 1: Change the above bar chart into a horizontal bar chart. See the end of the notebook for the solution. 

# Now let's look at a bit different relationship in our data. Let's map see if happiness correlates with life expectancy. In other words, do we see evidence that happier people live longer?

# In[3]:


alt.Chart(data).mark_circle().encode(x="Health (Life Expectancy)", y="Happiness Score")


# Activity: Let's try to use the same variables above but to create a line graph

# In[4]:


alt.Chart(data).mark_line().encode(
    x='Happiness Rank',
    y='Health (Life Expectancy)'
)


# Going back to our scatterplot, we can also add in a little more information to this plot. Let's add in some color to differentiate different regions of the world. 

# In[5]:


alt.Chart(data).mark_circle().encode(
    x = "Health (Life Expectancy)",
    y = "Happiness Score",
    color="Region"
)


# We start to see some correlations in the regions. Let's choose a little bit different color scheme to make these regions pop a bit more. 

# In[6]:


alt.Chart(data).mark_circle().encode(
    x = "Health (Life Expectancy)",
    y = "Happiness Score",
    color=alt.Color('Region', scale=alt.Scale(scheme='spectral'))
)


# Now that we're happy with our color scheme (though feel free to [experiment with others!](https://altair-viz.github.io/user_guide/customization.html)). Let's start to integrate some additional information into the visualization, starting with a basic interaction: adding a tooltip.

# In[7]:


alt.Chart(data).mark_circle().encode(
    x = "Health (Life Expectancy)",
    y = "Happiness Score",
    color=alt.Color('Region', scale=alt.Scale(scheme='spectral')),
    tooltip=["Country", "Happiness Score"]
)


# Test Your Knowledge 2: Let's add a little more information to our chart. Since we're already using position to encode two dimensions of our dataset, we can use other channels to represent new data. Try mapping generosity to the size of marks in your scatterplot (hint: the <code>size</code> channel will be helpful here)

# How do we facet charts? Well we can use a few different approaches.

# In[8]:


c1 = alt.Chart(data).mark_circle().encode(
    x = "Health (Life Expectancy)",
    y = "Happiness Score",
)

c2 = alt.Chart(data).mark_circle().encode(
    x = "Generosity",
    y = "Happiness Score",
)

c1|c2


# In our last chart, we'll experiment with faceting our data to visualize different charts for different combinations of dimensions. To do this, we'll use the <code>repeat</code> function to look at happiness scores (mapped to color) across health, generosity, family and freedom. Which dimensions appear to correlate most to happiness?

# In[9]:


# Build a SPLOM
alt.Chart(data).mark_circle().encode(
    alt.X(alt.repeat("column"), type="quantitative"),
    alt.Y(alt.repeat("row"), type="quantitative"),
    color="Happiness Score",
    tooltip=["Country", "Happiness Score"]
).properties(
    width=125,
    height=125
).repeat(
    row=["Health (Life Expectancy)", "Generosity","Family", "Freedom"],
    column=["Health (Life Expectancy)", "Generosity", "Family", "Freedom"]
)


# Altair enables you to create a broad variety of traditional and non-traditional visualizations. For example, we can also create line graphs to look at data over time or across variables like rankings or parallel coordinate plots to explore a variety of dimensions. Here's a line graph that explores health trend as a function of happiness ranking. 

# We can explore multiple variables at once using a parallel coordinates plot. In a parallel coordinates plot, we have multiple axes (one for each dimension) that are arrayed horizontally. Each line represents one datapoint. The position of a line on each axis corresponds to its value at that axis. We can look at lines that move together to see correlations between different data values. 
# 
# <p>Implementing this graph is a bit more complicated than some of the others, but will hopefully give you a sense of the power of Altair as a platform. The plot below uses the <code>transform_window</code> and <code>transform_fold</code> operations to specify the axes (which we can use the <code>key</code> variable to reflect). The <code>value</code> variable will give us the value of the point for a given dimension and the <code>index</code> variable gives us our dimension. Finally, we'll reduce the opacity of all lines to 50% to see our data a bit better and use a multihue sequential colorscheme to make the differences a little easier to see.</p>

# In[10]:


# Build a parallel coordinates plot
alt.Chart(data).transform_window(
    index="count()"
).transform_fold(
    ["Health (Life Expectancy)", "Generosity","Family", "Freedom"]
).mark_line().encode(
    x="key:N",
    y="value:Q",
    detail="index:N",
    opacity=alt.value(0.5),
    color=alt.Color("Happiness Rank:Q", scale=alt.Scale(scheme="Magma")),
    tooltip=["Country"]
).properties(width=700).interactive()


# Activity: Generate a plot that addresses one specific question about the happiness data. 

# We can save any plot to export it as an image using the "..." icon in the upper right of the chart. Alternatively, you can programmatically save your visualizations as interactive Javascript charts embeddable in web pages. You simply need to assign your chart to a variable (<code>chart = alt.Chart(...)</code>) and use <code>chart.save()</code> as in the following example. Note that the chart will not render to the notebook if you assign it to a variable. Instead, the following code will automatically write out an HTML document containing an interactive SVG of the visualization. 

# In[11]:


# Store the SPLOM
chart = alt.Chart(data).mark_circle().encode(
    alt.X(alt.repeat("column"), type="quantitative"),
    alt.Y(alt.repeat("row"), type="quantitative"),
    color="Happiness Score",
    tooltip=["Country", "Happiness Score"]
).properties(
    width=125,
    height=125
).repeat(
    row=["Health (Life Expectancy)", "Generosity","Family", "Freedom"],
    column=["Health (Life Expectancy)", "Generosity", "Family", "Freedom"]
).interactive()

chart.save('webchart.html', embed_options={'renderer':'svg'})


# <b>Solutions</b>
# 
# Test Your Knowledge 1:

# In[12]:


alt.Chart(data).mark_bar().encode(x="Happiness Score", y="Region")


# Test Your Knowledge 2: 

# In[13]:


alt.Chart(data).mark_circle().encode(
    x = "Health (Life Expectancy)",
    y = "Happiness Score",
    color=alt.Color('Region', scale=alt.Scale(scheme='spectral')),
    size="Generosity",
    tooltip=["Country", "Happiness Score"]
)

