# Load packages
import pandas as pd
import os
from math import ceil
from matplotlib import pyplot as plt
import seaborn as sns
from textwrap import wrap
sns.set(style="white",
        font="Arial",
        context="paper")

def PlotSingleVariableBarChart(dataframe,
                               categorical_variable,
                               fill_color=None,
                               top_n_to_highlight=None,
                               highlight_color="#b0170c",
                               fill_transparency=0.8,
                               title_for_plot=None,
                               subtitle_for_plot=None,
                               caption_for_plot=None,
                               data_source_for_plot=None,
                               title_y_indent=1.15,
                               subtitle_y_indent=1.1,
                               caption_y_indent=-0.15,
                               add_rare_category_line=False,
                               rare_category_line_color='#b5b3b3',
                               rare_category_threshold=0.05,
                               figure_size=(8, 6)):
    
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
        ax = sns.countplot(
            data=dataframe,
            y=categorical_variable,
            order=dataframe[categorical_variable].value_counts(ascending=False).index,
            palette=["#b8b8b8" if x not in dataframe[categorical_variable].value_counts().index[:top_n_to_highlight] else highlight_color for x in dataframe[categorical_variable].value_counts().index],
            alpha=fill_transparency
        )
    elif fill_color == None:
        ax = sns.countplot(
            data=dataframe,
            y=categorical_variable,
            order=dataframe[categorical_variable].value_counts(ascending=False).index,
            palette="Set1",
            alpha=fill_transparency
        )
    else:
        ax = sns.countplot(
            data=dataframe,
            y=categorical_variable,
            order=dataframe[categorical_variable].value_counts(ascending=False).index,
            color=fill_color,
            alpha=fill_transparency
        )
    
    # Add space between the title and the plot
    plt.subplots_adjust(top=0.85)
    
    # Wrap y axis label
    wrapped_variable_name = "\n".join(categorical_variable[j:j+30] for j in range(0, len(categorical_variable), 30))  # String wrap the variable name
    ax.set_ylabel(wrapped_variable_name)
    
    # Format and wrap y axis tick labels
    y_tick_labels = ax.get_yticklabels()
    wrapped_y_tick_labels = ['\n'.join(wrap(label.get_text(), 30)) for label in y_tick_labels]
    ax.set_yticklabels(wrapped_y_tick_labels, fontsize=10, fontname="Arial", color="#262626")
    
    # Move x-axis to the top
    ax.xaxis.tick_top()
    
    # Change x-axis colors to "#666666"
    ax.tick_params(axis='x', colors="#666666")
    ax.spines['top'].set_color("#666666")
    
    # Set x-axis title to "Count"
    ax.set_xlabel("Count", fontsize=10, fontname="Arial", color="#262626")
    
    # Remove bottom, left, and right spines
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Add data labels
    abs_values = dataframe[categorical_variable].value_counts(ascending=False)
    rel_values = dataframe[categorical_variable].value_counts(ascending=False, normalize=True).values * 100
    lbls = [f'{p[0]} ({p[1]:.0f}%)' for p in zip(abs_values, rel_values)]
    ax.bar_label(container=ax.containers[0],
                    labels=lbls,
                    padding=5)
    
    # Add rare category threshold line
    if add_rare_category_line:
        ax.axvline(
            x=rare_category_threshold * dataframe.shape[0],
            color=rare_category_line_color,
            alpha=0.5,
            linestyle='--',
            label='Rare category threshold'
        )
        
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
        if caption_for_plot != None:
            # Word wrap the caption without splitting words
            if len(caption_for_plot) > 120:
                # Split the caption into words
                words = caption_for_plot.split(" ")
                # Initialize the wrapped caption
                wrapped_caption = ""
                # Initialize the line length
                line_length = 0
                # Iterate through the words
                for word in words:
                    # If the word is too long to fit on the current line, add a new line
                    if line_length + len(word) > 120:
                        wrapped_caption = wrapped_caption + "\n"
                        line_length = 0
                    # Add the word to the line
                    wrapped_caption = wrapped_caption + word + " "
                    # Update the line length
                    line_length = line_length + len(word) + 1
        else:
            wrapped_caption = ""
        
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
# PlotSingleVariableBarChart(
#     dataframe=iris,
#     categorical_variable='species',
#     title_for_plot='Species',
#     subtitle_for_plot='This is a subtitle',
#     caption_for_plot="Meta-lesson: if you're going to go through the effort of visualizing data, take the time to be thoughtful about your design choices!",
#     data_source_for_plot="https://archive.ics.uci.edu/ml/datasets/iris"
# )
# # iris['species long label'] = np.where(
# #     iris['species'] == 0,
# #     "Longish label for 0",
# #     iris['species']
# # )
# # PlotSingleVariableBarChart(
# #     dataframe=iris,
# #     categorical_variable='species long label',
# #     title_for_plot='Species',
# #     subtitle_for_plot='This is a subtitle',
# #     caption_for_plot="Meta-lesson: if you're going to go through the effort of visualizing data, take the time to be thoughtful about your design choices!",
# #     data_source_for_plot="https://archive.ics.uci.edu/ml/datasets/iris",
# #     top_n_to_highlight=1
# # )
