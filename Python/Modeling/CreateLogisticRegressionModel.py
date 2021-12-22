import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import statsmodels.api as sm
import seaborn as sns

def CreateLogisticRegressionModel(dataframe,
                                  outcome_variable,
                                  list_of_predictors,
                                  share_to_use_as_test_set = .20,
                                  show_diagnostic_plots = True,
                                  show_help = True):
    
    # Select columns specified
    arr_columns = list_of_predictors.copy()
    arr_columns.append(outcome_variable)
    dataframe = dataframe[arr_columns]
    
    # Remove NAN and inf values
    print("Count of records in dataset:", len(dataframe.index))
    complete_case_dataframe = dataframe.dropna()
    complete_case_dataframe = complete_case_dataframe[np.isfinite(complete_case_dataframe).all(1)]
    print("Count of complete observations eligible for inclusion in regression model:", len(complete_case_dataframe.index))
    
    # Shuffle the rows of dataframe
    complete_case_dataframe = complete_case_dataframe.sample(frac = 1)
    
    # Create predictor/independent variables
    X = complete_case_dataframe[list_of_predictors]
    X = sm.add_constant(X)
    
    # Create outcome/dependent variables
    Y = complete_case_dataframe[outcome_variable]
    
    # Determine size of test dataset
    test_size = round(len(complete_case_dataframe.index) * share_to_use_as_test_set, 0)
    test_size = int(test_size)
    
    # Split the data into training/testing sets
    X_train = X[:-test_size]
    X_test = X[-test_size:]
    
    # Split the outcomes into training/testing sets
    Y_train = Y[:-test_size]
    Y_test = Y[-test_size:]
    
    # Create linear regression model
    model = sm.Logit(Y_train, X_train)
    model_res = model.fit()
    model_summary = model_res.summary()
    
    # If requested, show diagnostic plots
    if show_diagnostic_plots:
        for variable in list_of_predictors:
            fig = plt.figure(figsize=(12, 8))
            sns.lmplot(
                x=variable, 
                y=outcome_variable, 
                data=complete_case_dataframe,
                logistic=True, 
                y_jitter=.03
            )
            # Show plots
            plt.show()
    
    # If requested, show help text
    if show_help:
        print(
            "Quick guide on accessing output of CreateLogisticRegressionModel function:",
            "\nThe ouput of the CreateLogisticRegressionModel function is a dictionary containing the regression results, a test dataset of predictors, and a test dataset of outcomes.",
            "\n\t--To access the linear regression model, use the 'Fitted Model' key."
            "\n\t--To view the model's statistical summary, use the 'Model Summary' key.",
            "\n\t--To access the test dataset of predictors, use the 'Predictor Test Dataset' key.",
            "\n\t--To access the test dataset of outcomes, use the 'Outcome Test Dataset' key.",
            "\n\nRemember that you can utilize the TestLogisticRegressionModelCI function to test the accuracy of the 95% confidence interval of your fitted regression model."
        )
    
    # Create dictionary of objects to return
    dict_return = {
        "Fitted Model": model_res,
        "Model Summary": model_summary,
        "Predictor Test Dataset": X_test,
        "Outcome Test Dataset": Y_test
    }
    return dict_return

# ## Testing
# # Import data
# df_bitcoin = pd.read_csv("C:/Users/oneno/OneDrive/Data/BitcoinWeeklyData_20180101_20211222.csv")
# # Run regression
# dict_bitcoin_model = CreateLogisticRegressionModel(
#     dataframe = df_bitcoin,
#     outcome_variable = 'Is Price Higher than Previous Week',
#     list_of_predictors = [
#         'Week Count from 1/1/2018', 
#         # 'Normalized Google Search Volume of Previous Week - bitcoin',
#         'Close Price in USD of Previous Week'
#     ],
#     share_to_use_as_test_set = .20,
#     show_diagnostic_plots = True,
#     show_help = True
# )
# # Show the model summary
# dict_bitcoin_model['Model Summary']
