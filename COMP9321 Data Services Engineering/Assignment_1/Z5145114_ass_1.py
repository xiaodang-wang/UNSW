import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

def print_dataframe(dataframe, print_column=True, print_rows=True):
    # print column names
    if print_column:
        print(",".join([column for column in dataframe]))
    # print rows one by one
    if print_rows:
        for index, row in dataframe.iterrows():
            print(",".join([str(row[column]) for column in dataframe]))

# merge two datasets
def merge():
    # read files
    df1 = pd.read_csv('Olympics_dataset1.csv', skiprows=1, thousands=',')
    df2 = pd.read_csv('Olympics_dataset2.csv', skiprows=1, thousands=',')
    # merge the two datasets
    df3 = pd.merge(df1,df2,how='outer', on=['Unnamed: 0'])
    # modify
    df3 = df3.rename(columns={'Unnamed: 0':'country','Number of Games the country participated in_x':'Number of Games the country participated in_summer',
        'Gold_x':'Gold_summer','Silver_x':'Silver_summer','Bronze_x':'Bronze_summer','Total_x':'Total_summer',
        'Number of Games the country participated in_y':'Number of Games the country participated in_winter',
        'Gold_y':'Gold_winter','Silver_y':'Silver_winter','Bronze_y':'Bronze_winter','Total_y':'Total_winter',
        'Number of Games the country participated in.1':'Number of Games the country participated in_total',
        'Gold.1':'Gold_total','Silver.1':'Silver_total','Bronze.1':'Bronze_total','Total.1':'Total_total'})
    return df3  

def question_1():
    return merge().head(5)

def question_2():
    df = merge()
    df = df.set_index(['country'])
    return df.head(1)

def question_3():
    df = merge()
    df = df.drop(columns=['Rubish'])
    return df.head(5)

def question_4():
    df = merge()
    df = df.dropna()
    return df.tail(10)

def question_5():
    df = merge()
    # drop total line
    df = df.drop(df.index[-1])
    # sort values by gold medals in summer games['Gols_x']
    df = df.sort_values(by=['Gold_summer'], ascending=False)
    country = df.iloc[0]['country']
    return country

def question_6():
    df = merge()
    df = df.drop(df.index[-1])
    df['difference'] = abs(df.Gold_summer - df.Gold_winter)
    df = df.sort_values(by=['difference'], ascending=False)
    country = df.iloc[0]['country']
    return country

def question_7():
    df = merge()
    # drop total line
    df = df.drop(df.index[-1])
    # sort
    df = df.sort_values('Total_total', ascending = False)
    df1 = df.head(5)
    df2 = df.tail(5)
    df3 = pd.concat([df1, df2], axis=0)
    return df3

def question_8():
    df = merge()
    df = df.drop(df.index[-1])
    df = df.sort_values('Total_total', ascending = False)
    df = df.head(10)
    # cleaning columns
    df = df.drop(columns=['Rubish','Number of Games the country participated in_summer','Gold_summer','Silver_summer','Bronze_summer',
      'Number of Games the country participated in_winter','Gold_winter','Silver_winter','Bronze_winter',
      'Number of Games the country participated in_total','Gold_total','Silver_total','Bronze_total','Total_total'])
    df = df.rename(columns={'Total_summer':'Summer games','Total_winter':'Winter games'})
    df['country'] = df['country'].apply(lambda x: re.split('[\(\[]',x)[0][1:-1])
    df = df.set_index(['country'])
    # plot
    df.plot.barh(stacked = True, title ="Medals for Winter and Summer Games")
    plt.tight_layout()
    plt.show()

def question_9():
    df = merge()
    df = df.drop(df.index[-1])
    df = df.sort_values('Total_total', ascending = False)
    # cleaning columns
    df = df.drop(columns=['Rubish','Number of Games the country participated in_summer','Gold_summer','Silver_summer','Bronze_summer','Total_summer',
      'Number of Games the country participated in_winter','Total_winter',
      'Number of Games the country participated in_total','Gold_total','Silver_total','Bronze_total','Total_total'])
    df = df.rename(columns={'Gold_winter':'Gold','Silver_winter':'Silver','Bronze_winter':'Bronze'})
    df['country'] = df['country'].apply(lambda x: re.split('[\(\[]',x)[0][1:-1])
    df = df.query('country == "United States" | country == "Australia" | country == "Great Britain" | country == "Japan" | country == "New Zealand"')
    df = df.set_index(['country'])
    # plot
    df.plot.bar(title = "Winter Games")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    print('question_1:')
    print_dataframe(question_1())
    print()
    print('question_2:')
    print_dataframe(question_2())
    print()
    print('question_3:')
    print_dataframe(question_3())
    print()
    print('question_4:')
    print_dataframe(question_4())
    print()
    print('question_5:')
    print(question_5())
    print()
    print('question_6:')
    print(question_6())
    print()
    print('question_7:')
    print_dataframe(question_7())
    question_8()
    question_9()


