import pandas as pd
import numpy as np
from functools import reduce


class AdhocAnalysis:


    @classmethod
    def compute_revenue(cls,df,column_name):

        try:
            if isinstance(df, pd.DataFrame):
               df[column_name] = df[column_name].str.lower();
               df_revenue      = df.groupby(column_name)['Due Agency'].sum().reset_index();
               df_revenue.columns = [column_name, 'revenue'];
               return df_revenue;

        except Exception as e:
            print(e);

    @classmethod
    def compute_payment(cls,df,column_name):

        try:
            if isinstance(df, pd.DataFrame):
                df[column_name] = df[column_name].str.lower();
                df_pay = df.groupby(column_name)['Pmt Amt Applied'].sum().reset_index();
                df_pay.columns = [column_name, 'payment'];
                return df_pay;

        except Exception as e:
            print(e);

    @classmethod
    def compute_transaction(cls,df,column_name):
        try:
            if isinstance(df, pd.DataFrame):
                df[column_name] = df[column_name].str.lower();
                df_trans = df.groupby(column_name)['Pmt Code'].count().reset_index();
                df_trans.columns = [column_name, 'transaction'];
                return df_trans;

        except Exception as e:
            print(e);


    @classmethod
    def merge_frames(cls,li,column_name):

        frame = reduce(lambda x,y:pd.merge(x,y,on=[column_name],how='inner'),li);
        return frame

    @classmethod
    def yearly_computation(cls,df,year,column_name):

        try:
            if isinstance(df, pd.DataFrame):

                df_filter = df.loc[df['Year']==year];
                df_rev = cls.compute_revenue(df_filter,column_name);
                df_pay = cls.compute_payment(df_filter,column_name);
                df_tr  = cls.compute_transaction(df_filter,column_name);
                li =[df_rev,df_pay,df_tr];
                frame = cls.merge_frames(li,column_name);
                frame = frame[[column_name, "payment", "revenue", "transaction"]];

                return frame;

        except Exception as e:
            print(e);

    @classmethod
    def monthly_computation(cls,df,year,column_name):

        try:
            if isinstance(df, pd.DataFrame):

                frame = cls.yearly_computation(df,year,column_name);
                frame[column_name] = frame[column_name].str.capitalize()
                frame["mon"] = pd.to_datetime(frame.Month_Name, format='%b', errors='coerce').dt.month
                frame = frame.sort_values(by="mon")
                frame = frame[[column_name, "payment", "revenue", "transaction"]];
                return frame;

        except Exception as e:

            print(e);

    @classmethod
    def overall_metric(cls,df):

     try:
        if isinstance(df, pd.DataFrame):
            revenue = round(df['Due Agency'].sum(), 2);
            transaction = df['Pmt Code'].count();
            payment = round(df['Pmt Amt Applied'].sum(), 2);

            my_dict = {};
            my_dict['overall_details'] = {"payment": payment, "revenue": revenue,
                                          "transaction": np.int64(transaction).item(), "legal_actions": " "};

            return my_dict

     except Exception as e:
        print(e);








