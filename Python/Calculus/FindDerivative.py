import matplotlib.pyplot as plt
import numpy as np

# Define a function that finds the derivative of a function
def FindDerivative(f_of_x, 
                   point,
                   step=0.0001,
                   plot_function=True,
                   plot_derivative_function=True,
                   x_minimum=-10,
                   x_maximum=10,
                   n=100,
                   tangent_line_window=None,
                   return_derivative_values=False):
    """_summary_
    This function finds the derivative of a function at a given point. It also plots the function and the tangent line at the point of interest.

    Args:
        f_of_x (lambda): The function of x.
        point (int or float): The point at which to find the derivative.
        step (float, optional): The step size to use when calculating the derivative. Defaults to 0.0001.
        plot_function (bool, optional): Whether or not to plot the function. Defaults to True.
        x_minimum (int, optional): The minimum value of x to use when plotting the function. Defaults to -10.
        x_maximum (int, optional): The maximum value of x to use when plotting the function. Defaults to 10.
        n (int, optional): The number of points to use when plotting the function. Defaults to 100.
        tangent_line_window (_type_, optional): The window to use when plotting the tangent line. Defaults to None, which will use 1/5 of the x range.
    """
    # Create array of values based on the function
    x = np.linspace(x_minimum, x_maximum, n)
    y = np.zeros(len(x))
    for i in range(len(x)):
        y[i] = f_of_x(x[i])
    
    # Calculate the derivative
    y_derivative = np.gradient(y)
    
    # Calculate the limit at the point of interest
    try:
        limit = f_of_x(point)
        print("The limit at x={0} is ~{1}".format(point, limit))
        
        # # Print the slope of the tangent line
        rise = f_of_x(point) - f_of_x(point - 1)
        # run = 1
        # print("The slope of the tangent line is {0}/{1}".format(round(rise, 2), round(run, 2)))
        
        # # Create tangent line
        # if tangent_line_window==None:
        #     tangent_line_window_1 = (y.max() - y.min()) / 5
        #     tangent_line_window_2 = (x.max() - x.min()) / 5
        #     tangent_line_window = min(tangent_line_window_1, tangent_line_window_2)
        # x_tangent = np.linspace(point - tangent_line_window, point + tangent_line_window, 3)
        # y_tangent = limit * (x_tangent - point) + f_of_x(point)
        # if rise < 0:
        #     y_tangent = np.flip(y_tangent)
        
        # # Plot tangent line
        # plt.plot(x_tangent, y_tangent, color="red")
        
        # Plot the function if requested
        if plot_function:
            # Plot point at the point of interest
            plt.plot(point, f_of_x(point), "ro")
        
    except ZeroDivisionError:
        print("The limit at x={0} is undefined.".format(point))
    
    # Plot the function if requested
    if plot_function:
        # Plot the function
        plt.plot(x, y, color="black")
        
        # Add title
        plt.title("f(x)")
        
        # Show plot
        plt.show()
        plt.clf()
    
    # Plot the derivative function if requested
    if plot_derivative_function:
        plt.plot(x, y_derivative, color="red", alpha=0.25)
        plt.title("Derivative of f(x)")
        plt.show()
    
    # Return derivative values if requested
    if return_derivative_values:
        return(y_derivative)


# Test the function
# FindDerivative(
#     f_of_x=lambda x: np.power(x, 2),
#     point=0
# )
# FindDerivative(
#     f_of_x=lambda x: 1/x, 
#     point=0
# )
# FindDerivative(
#     f_of_x=lambda x: math.sin(x), 
#     point=0
# )
# FindDerivative(
#     f_of_x=lambda x: np.exp(1) ** x, 
#     point=1,
#     x_minimum=0,
#     x_maximum=10
# )
# FindDerivative(
#     f_of_x=lambda x: np.log(x), 
#     point=1,
#     x_minimum=0,
#     x_maximum=10
# )
