import pandas as pd
import numpy as np
from functools import reduce


#A class being utilized for the analysis
class AdhocAnalysis:

    #Loading file to pandas dataframe
    df_pandas = pd.read_csv("/home/nithin/Desktop/Deaconess/Master_File_New.csv")

    #Function for revenue,transaction and payment computations
    @classmethod
    def compute_metric(cls,column_to_be_grouped):

        try:
         if isinstance(cls.df_pandas, pd.DataFrame):

            cls.df_pandas[column_to_be_grouped] = cls.df_pandas[column_to_be_grouped].str.lower();


            df_revenue = cls.df_pandas.groupby(column_to_be_grouped)['Due Agency'].sum().reset_index();
            df_revenue.columns = [column_to_be_grouped,'revenue'];

            df_pay =cls.df_pandas.groupby(column_to_be_grouped)['Pmt Amt Applied'].sum().reset_index();
            df_pay.columns = [column_to_be_grouped, 'payment'];

            df_transaction =cls.df_pandas.groupby(column_to_be_grouped)['SSN'].count().reset_index();
            df_transaction.columns = [column_to_be_grouped, 'transaction'];

            li = [df_pay, df_revenue, df_transaction]

            frame = reduce(lambda x, y: pd.merge(x, y, on=[column_to_be_grouped], how='inner'),li);

            if(column_to_be_grouped=='Month_Name'):

                frame["Month_Name"] = frame["Month_Name"].str.capitalize()
                frame["mon"] = pd.to_datetime(frame.Month_Name, format='%b', errors='coerce').dt.month
                frame = frame.sort_values(by="mon")
                frame = frame[["Month_Name","payment","revenue","transaction"]]

            frame['legal_actions'] = " "
            frame.set_index(column_to_be_grouped, inplace=True);

            return  frame;

        except Exception as e:

            print(e);



    @classmethod
    def overall_metric_computation(cls):

        try:
            if isinstance(cls.df_pandas, pd.DataFrame):

              revenue      = round(cls.df_pandas['Due Agency'].sum(),2);
              transaction  = cls.df_pandas['SSN'].count();
              payment      = round(cls.df_pandas['Pmt Amt Applied'].sum(),2);

              my_dict = {};
              my_dict['overall_details'] ={"payment":payment,"revenue":revenue,"transaction":np.int64(transaction).item(),"legal_actions":" "};

              return my_dict

        except Exception as e:
             print(e);







