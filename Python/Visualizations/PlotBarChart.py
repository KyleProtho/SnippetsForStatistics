# Load packages
import pandas as pd
import os
from math import ceil
from matplotlib import pyplot as plt
import seaborn as sns
import textwrap
sns.set(style="white",
        font="Arial",
        context="paper")

# Declare function
def PlotBarChart(dataframe,
                 categorical_variable, 
                 value_variable,
                 # Plot formatting arguments
                 color_palette="Set1",
                 fill_color=None,
                 top_n_to_highlight=None,
                 highlight_color="#b0170c",
                 fill_transparency=0.8,
                 figure_size=(8, 6),
                 # Text formatting arguments
                 title_for_plot=None,
                 subtitle_for_plot=None,
                 caption_for_plot=None,
                 data_source_for_plot=None,
                 title_y_indent=1.15,
                 subtitle_y_indent=1.1,
                 caption_y_indent=-0.15,
                 decimal_places_for_data_label=2):
    """
    This function generates a bar chart using the seaborn library. 
    The function takes in a pandas dataframe, a categorical variable, and a value variable. 
    The function also takes in optional arguments for plot formatting, text formatting, and data labels.

    Parameters:
    dataframe (pandas dataframe): The dataframe containing the data to be plotted.
    categorical_variable (str): The name of the column in the dataframe containing the categorical variable.
    value_variable (str): The name of the column in the dataframe containing the value variable.
    color_palette (str or list, optional): The seaborn color palette to use for the plot. Defaults to "Set1".
    fill_color (str, optional): The color to use for the bars in the plot. If None, the color palette will be used. Defaults to None.
    top_n_to_highlight (int, optional): The number of top categories to highlight in the plot. Defaults to None.
    highlight_color (str, optional): The color to use for the highlighted categories. Defaults to "#b0170c".
    fill_transparency (float, optional): The transparency of the bars in the plot. Defaults to 0.8.
    figure_size (tuple, optional): The size of the plot figure. Defaults to (8, 6).
    title_for_plot (str, optional): The title of the plot. Defaults to None.
    subtitle_for_plot (str, optional): The subtitle of the plot. Defaults to None.
    caption_for_plot (str, optional): The caption of the plot. Defaults to None.
    data_source_for_plot (str, optional): The data source of the plot. Defaults to None.
    title_y_indent (float, optional): The y-axis indent for the plot title. Defaults to 1.15.
    subtitle_y_indent (float, optional): The y-axis indent for the plot subtitle. Defaults to 1.1.
    caption_y_indent (float, optional): The y-axis indent for the plot caption. Defaults to -0.15.
    decimal_places_for_data_label (int, optional): The number of decimal places to round the data labels to. Defaults to 2.

    Returns:
    None
    """
    
    # Check that the column exists in the dataframe.
    if categorical_variable not in dataframe.columns:
        raise ValueError("Column {} does not exist in dataframe.".format(categorical_variable))
    
    # Ensure that rare category threshold is between 0 and 1
    if rare_category_threshold < 0 or rare_category_threshold > 1:
        raise ValueError("Rare category threshold must be between 0 and 1.")
    
    # Make sure that the top_n_to_highlight is a positive integer, and less than the number of categories
    if top_n_to_highlight != None:
        if top_n_to_highlight < 0 or top_n_to_highlight > len(dataframe[categorical_variable].value_counts()):
            raise ValueError("top_n_to_highlight must be a positive integer, and less than the number of categories.")
    
    # Create figure and axes
    fig, ax = plt.subplots(figsize=figure_size)

    # Generate bar chart
    if top_n_to_highlight != None:
        ax = sns.barplot(
            data=dataframe,
            y=categorical_variable,
            x=value_variable,
            palette=[highlight_color if x in dataframe.sort_values(value_variable, ascending=False)[value_variable].nlargest(top_n_to_highlight).index else "#b8b8b8" for x in dataframe.sort_values(value_variable, ascending=False).index],
            order=dataframe.sort_values(value_variable, ascending=False)[categorical_variable],
            alpha=fill_transparency
        )
    elif fill_color == None:
        ax = sns.barplot(
            data=dataframe,
            y=categorical_variable,
            x=value_variable,
            palette=color_palette,
            order=dataframe.sort_values(value_variable, ascending=False)[categorical_variable],
            alpha=fill_transparency
        )
    else:
        ax = sns.barplot(
            data=dataframe,
            y=categorical_variable,
            x=value_variable,
            color=fill_color,
            order=dataframe.sort_values(value_variable, ascending=False)[categorical_variable],
            alpha=fill_transparency
        )
    
    # Add space between the title and the plot
    plt.subplots_adjust(top=0.85)
    
    # Wrap y axis label using textwrap
    wrapped_variable_name = "\n".join(textwrap.wrap(categorical_variable, 30))  # String wrap the variable name
    ax.set_ylabel(wrapped_variable_name)
    
    # Format and wrap y axis tick labels using textwrap
    y_tick_labels = ax.get_yticklabels()
    wrapped_y_tick_labels = ['\n'.join(textwrap.wrap(label.get_text(), 30)) for label in y_tick_labels]
    ax.set_yticklabels(wrapped_y_tick_labels, fontsize=10, fontname="Arial", color="#262626")
    
    # Move x-axis to the top
    ax.xaxis.tick_top()
    
    # Change x-axis colors to "#666666"
    ax.tick_params(axis='x', colors="#666666")
    ax.spines['top'].set_color("#666666")
    
    # Remove bottom, left, and right spines
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Add data labels
    abs_values = dataframe.sort_values(value_variable, ascending=True)[value_variable].round(decimal_places_for_data_label).astype(str)
    lbls = [f'{p[0]}' for p in zip(abs_values)]
    lbls = lbls[::-1]
    ax.bar_label(container=ax.containers[0],
                 labels=lbls,
                 padding=5)
        
    # Set the x indent of the plot titles and captions
    # Get longest y tick label
    longest_y_tick_label = max(wrapped_y_tick_labels, key=len)
    if len(longest_y_tick_label) >= 30:
        x_indent = -0.3
    else:
        x_indent = -0.005 - (len(longest_y_tick_label) * 0.011)
        
    # Set the title with Arial font, size 14, and color #262626 at the top of the plot
    ax.text(
        x=x_indent,
        y=title_y_indent,
        s=title_for_plot,
        fontname="Arial",
        fontsize=14,
        color="#262626",
        transform=ax.transAxes
    )
    
    # Set the subtitle with Arial font, size 11, and color #666666
    ax.text(
        x=x_indent,
        y=subtitle_y_indent,
        s=subtitle_for_plot,
        fontname="Arial",
        fontsize=11,
        color="#666666",
        transform=ax.transAxes
    )
    
        
    # Add a word-wrapped caption if one is provided
    if caption_for_plot != None or data_source_for_plot != None:
        # Create starting point for caption
        wrapped_caption = ""
        
        # Add the caption to the plot, if one is provided
        if caption_for_plot != None:
            # Word wrap the caption without splitting words
            wrapped_caption = textwrap.fill(caption_for_plot, 110, break_long_words=False)
            
        # Add the data source to the caption, if one is provided
        if data_source_for_plot != None:
            wrapped_caption = wrapped_caption + "\n\nSource: " + data_source_for_plot
        
        # Add the caption to the plot
        ax.text(
            x=x_indent,
            y=caption_y_indent,
            s=wrapped_caption,
            fontname="Arial",
            fontsize=8,
            color="#666666",
            transform=ax.transAxes
        )
        
    # Show plot
    plt.show()
    
    # Clear plot
    plt.clf()


# # Test the function
# import numpy as np
# from sklearn import datasets
# iris = pd.DataFrame(datasets.load_iris(as_frame=True).data)
# iris['species'] = datasets.load_iris(as_frame=True).target
# iris['species'] = iris['species'].astype('category')
# # Group and summarize average petal length by species
# iris = iris.groupby('species').agg({'petal length (cm)': np.mean}).reset_index()
# PlotBarChart(
#     dataframe=iris,
#     categorical_variable='species',
#     value_variable='petal length (cm)',
#     title_for_plot='Species',
#     subtitle_for_plot='This is a subtitle',
#     caption_for_plot="Meta-lesson: if you're going to go through the effort of visualizing data, take the time to be thoughtful about your design choices!",
#     data_source_for_plot="https://archive.ics.uci.edu/ml/datasets/iris",
#     # top_n_to_highlight=1
#     # add_rare_category_line=True,
# )

# data = {
#     'Group': ['Pittsburgh', 'Denver', 'Tampa'],
#     'Current Performance': [.7997, .6933, .9339]
# }
# data = pd.DataFrame(data)
# PlotBarChart(
#     dataframe=data,
#     categorical_variable='Group',
#     value_variable='Current Performance',
#     title_for_plot='Test',
#     subtitle_for_plot='This is a subtitle',
#     caption_for_plot="Meta-lesson: if you're going to go through the effort of visualizing data, take the time to be thoughtful about your design choices!",
#     data_source_for_plot="https://archive.ics.uci.edu/ml/datasets/iris",
#     top_n_to_highlight=1
# )
