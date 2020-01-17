# import pandas, numpy
# Create the required data frames by reading in the files
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

sales_df=pd.read_excel("SaleData.xlsx")
movie_df=pd.read_csv("movie_metadata.csv")
diamonds_df=pd.read_csv("diamonds.csv")
imdb_df=pd.read_csv("imdb.csv",escapechar="\\")

date = pd.to_datetime(input('Input date in mm-dd-yyyy format'))

# Q1 Find least sales amount for each item
# has been solved as an example
def least_sales(sales_df):
    ls = sales_df.groupby(["Item"])["Sale_amt"].min().reset_index()
    return ls

# Q2 compute total sales at each year X region
def sales_year_region(sales_df):
    Year=sales_df.OrderDate.dt.year
    print(sales_df.groupby([sales_df.OrderDate.dt.year,'Region']).Sale_amt.sum())

# Q3 append column with no of days difference from present date to each order date
def days_diff(sales_df,date):
    sales_df['days_diff']=sales_df['OrderDate'].apply(lambda x: (date-x).days)
    print(sales_df.head())

# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.
def mgr_slsmn(sales_df):
    df1=sales_df.groupby(['Manager','SalesMan']).describe()
    df1.drop(df1[['Units','Sale_amt','days_diff','Unit_price']],axis=1,inplace=True)
    print(df1)

# Q5 For all regions find number of salesman and number of units
def slsmn_units(sales_df):
    sales_df2=sales_df.groupby('Region').agg({'Sale_amt':['sum'],'SalesMan':['nunique']}).reset_index()
    sales_df2.columns=['Region','Total_Sales','SalesMan_count']
    print(sales_df2)


# Q6 Find total sales as percentage for each manager
def sales_pct(sales_df):
    q10=sales_df.groupby('Manager').Sale_amt.sum().reset_index()
    q10.columns=['Manager','Percent_sales']
    print(q10)

# Q7 get imdb rating for fifth movie of dataframe
def fifth_movie(movie_df):
	print(movie_df.imdb_score[4])

# Q8 return titles of movies with shortest and longest run time
def movies(movie_df):
	print(movie_df.movie_title[movie_df['duration'].idxmax()])
	print(movie_df.movie_title[movie_df['duration'].idxmin()])

# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)
def sort_df(movie_df):
	print(movie_df.sort_values(by=['title_year', 'imdb_score'], ascending=[True, False]))

# Q10 subset revenue more than 2 million and spent less than 1 million & duration between 30 mintues to 180 minutes
def subset_df(movie_df):
    movie_df1=movie_df.loc[(movie_df['duration'] >= 30) & (movie_df['duration'] <= 180) & (movie_df['budget']<1000000) & (movie_df['gross']>2000000)]
    print(movie_df1.head())

# Q11 count the duplicate rows of diamonds DataFrame.
def dupl_rows(movie_df):
    diamonds_df1=pd.DataFrame(diamonds_df)
    dupl=len(diamonds_df1)-len(diamonds_df1.drop_duplicates())
    print(dupl)

# Q12 droping those rows where any value in a row is missing in carat and cut columns
def drop_row(diamonds_df):
    diamonds_df2=pd.DataFrame(diamonds_df.dropna(how='any',subset=['carat','cut']))
    print(diamonds_df2.head())

# Q13 subset only numeric columns
def sub_numeric(diamonds_df):
    diamonds_df3=diamonds_df._get_numeric_data()
    print(diamonds_df3.head())

# Q14 compute volume as (x*y*z) when depth > 60 else 8
def volume(diamonds_df):
    diamonds_df.loc[diamonds_df['depth'] > 60, 'volume'] = diamonds_df['x']*diamonds_df['y']*pd.to_numeric(diamonds_df['z'],errors='coerce')
    diamonds_df.loc[diamonds_df['depth'] <= 60, 'volume'] = 8 
    print(diamonds_df.head())

# Q15 impute missing price values with mean
def impute(diamonds_df):
    diamonds_df['price'].fillna(value=diamonds_df['price'].mean(),inplace=True)
    print(diamonds_df.head())

# BONUS-QUESTION:

# Q1 Generate a report that tracks the various Genere combinations for each type year on year. The result data frame should contain type, Genere_combo, year, avg_rating, min_rating, max_rating, total_run_time_mins 
def report_genre(imdb_df):
    imdb_df1=imdb_df.groupby('year').sum().reset_index()
    imdb_df2=pd.DataFrame(imdb_df1)
    imdb_df2.drop(imdb_df2[['year', 'imdbRating', 'ratingCount', 'duration', 'nrOfWins','nrOfNominations', 'nrOfPhotos', 'nrOfNewsArticles', 'nrOfUserReviews','nrOfGenre']],axis=1,inplace=True)
    imdb_df3=pd.DataFrame(imdb_df1.year)
    imdb_df3['type']=imdb_df["type"].str.split(".", n = 1, expand = True)[1]
    imdb_df3['Genre_combo']=imdb_df2.apply(lambda x: "|".join(x.index[x>=1]),axis=1)
    imdb_df4=imdb_df.groupby('year').agg({'imdbRating': ['mean','min', 'max'],'duration':['sum']}).reset_index()
    imdb_df4.columns=['year','avg_rating','min_rating','max_rating','total_run_time_mins ']
    res=pd.merge(imdb_df3,imdb_df4,how='inner',on='year')
    print(res.head())

#Q2 Is there a realation between the length of a movie title and the ratings ? Generate a report that captures the trend of the number of letters in movies titles over years. We expect a cross tab between the year of the video release and the quantile that length fall under. The results should contain year, min_length, max_length, num_videos_less_than25Percentile, num_videos_25_50Percentile , num_videos_50_75Percentile, num_videos_greaterthan75Precentile 
def relation(imdb_df):
    imdb_df['title']=imdb_df['title'].str.replace('\(.*\)','')
    imdb_df['title_len']=imdb_df.title.str.len()
    print(imdb_df[['title_len','imdbRating']].corr(method="spearman"))
    imdb_df5=pd.DataFrame(imdb_df.groupby('year')['title_len'].sum().dropna().reset_index())
    imdb_df5.set_index('year',inplace=True)
    print(trend_plot(imdb_df5))
    imdb_df6=imdb_df.groupby('year')['title_len'].agg([('min_length','min'),('max_length','max')]).reset_index()
    imdb_df7=pd.DataFrame(imdb_df.year)
    imdb_df7['a']=(imdb_df.title_len < imdb_df.title_len.quantile(.25))
    imdb_df7['b']=(imdb_df.title_len >= imdb_df.title_len.quantile(.25)) & (imdb_df.title_len < imdb_df.title_len.quantile(.50))
    imdb_df7['c']=(imdb_df.title_len >= imdb_df.title_len.quantile(.50)) & (imdb_df.title_len < imdb_df.title_len.quantile(.75))
    imdb_df7['d']=imdb_df.title_len >= imdb_df.title_len.quantile(.75)
    imdb_df7.columns=['year','num_videos_less_than25Percentile','num_videos_25_50Percentile','num_videos_50_75Percentile','num_videos_greaterthan75Precentile']
    imdb_df8=imdb_df7.groupby('year').sum().reset_index()
    res=pd.merge(imdb_df6, imdb_df8, how ='inner', on ='year')
    print(res.head())

def trend_plot(imdb_df5): #This function is used to show the trend between title length and Year
    imdb_df5.plot(figsize=(10,5), linewidth=3, fontsize=12)
    plt.xlabel('Year', fontsize=10);
    plt.ylabel('Length',fontsize=10);

#Q3 In diamonds data set Using the volumne calculated above, create bins that have equal population within them. Generate a report that contains cross tab between bins and cut. Represent the number under each cell as a percentage of total. 
def cross_tab(diamonds_df):
    diamonds_df['bins'] = pd.qcut(diamonds_df['volume'], q=6,precision=0)
    diamonds_df3=pd.crosstab(diamonds_df.dropna().bins.astype(str), diamonds_df.cut, normalize='all',margins=False).round(4)*100
    print(diamonds_df3)
    
#Q4 Generate a report that tracks the Avg. imdb rating quarter on quarter, in the last 10 years, for movies that are top performing. You can take the top 10% grossing movies every quarter. Add the number of top performing movies under each genere in the report as well. 
def top_10(movie_df):
    moviedf1=movie_df.groupby('title_year')['gross'].sum().reset_index()
    moviedf1['10']=moviedf1['gross']*0.9
    movie_df=pd.merge(movie_df,moviedf1[['title_year','10']],how='inner',on='title_year')
    movie_df.loc[movie_df['gross'] >= movie_df['10'],'avg_score'] = movie_df['imdb_score']
    moviedf2=movie_df.groupby('title_year')['avg_score'].mean().dropna().reset_index()
    print(moviedf2)

#Q5  Bucket the movies into deciles using the duration. Generate the report that tracks various features like nomiations, wins, count, top 3 geners in each decile
def movie_decile(imdb_df):
    imdb_df['decile'] = pd.qcut(imdb_df['duration'], 10, labels=False)
    data=pd.DataFrame(imdb_df)
    data.drop(data[['fn', 'tid', 'title', 'wordsInTitle', 'url', 'imdbRating','ratingCount', 'duration', 'year', 'type','nrOfPhotos', 'nrOfNewsArticles', 'nrOfUserReviews','nrOfGenre']],axis=1,inplace=True)
    test1 = data.groupby('decile', sort=True).sum().reset_index()
    test_2=pd.DataFrame(test1[['decile', 'nrOfWins', 'nrOfNominations']])
    test_2['count']=imdb_df.groupby('decile').count()
    test_3=test1.drop(test1[['nrOfWins', 'nrOfNominations']],axis=1).set_index('decile')
    test_4 = pd.DataFrame(test_3.columns.values[np.argsort(-test_3.values, axis=1)[:, :3]], index=test_3.index,columns = ['1st Max','2nd Max','3rd Max']).reset_index()
    res=pd.merge(test_2, test_4, how ='inner', on ='decile')
    print(res)