library(readxl)
library(dplyr)
sales_df<- read_excel('SaleData.xlsx')
imdb_df<- read.csv(text = gsub("\\\\,", "-", readLines("imdb.csv")))
movie_df<- read.csv('movie_metadata.csv')
diamonds_df<-data.frame(read.csv('diamonds.csv'))
imdb_df$title<- sub("\\s*\\([^\\)]+\\)","",as.character(imdb_df$title))

least_sales<- function(sales_df){
  #1. Find the least amount sale that was done for each item.
  print(sales_df %>% group_by(Item) %>% summarize(Min.each.item=min(Sale_amt,na.rm=T)))
}

sales_year_region<- function(sales_df){
  sales_df1<-sales_df
  #2. Compute the total sales for each year and region across all items
  sales_df1$year<- format(sales_df1$OrderDate,format='%y')
  print(sales_df1 %>% group_by(year, Region) %>% summarize(Total.each.item=sum(Sale_amt,na.rm=T)))
}

d <- readline(prompt="Enter date (dd-mm-yyyy): ")
days_diff<- function(sales_df,d){
  #3. Create new column 'days_diff'
  sales_df$days_diff<- as.Date(d,"%d-%m-%Y")-as.Date(sales_df$OrderDate)
  print(head(sales_df))
}

mgr_slsmn<- function(sales_df){
  #4. Create a dataframe with two columns: 'manager', 'list_of_salesmen'
  print(sales_df %>% group_by(Manager,SalesMan) %>% summarize())
}

slsmn_units<- function(sales_df){
  #5. For all regions find number of salesman and total sales
  sales_df3<- sales_df %>% group_by(Region) %>% summarize(Total.sales=sum(Sale_amt,na.rm=T),SalesMan.count=length(unique(SalesMan)))
  print(sales_df3)
}

sales_pct<-function(sales_df){
  #6. Create a dataframe with total sales as percentage for each manager
  l2<- sum(sales_df$Sale_amt)
  print(sales_df %>% group_by(Manager) %>% summarize(percent.sales=(sum(Sale_amt,na.rm=T)/l2)*100))
}

fifth_movie<- function(imdb_df){
  #7. Get the imdb rating for fifth movie of dataframe
  print(imdb_df$imdbRating[5])
}

movies<- function(imdb_df){
  #8. Return titles of movies with shortest and longest run time
  max.1<- max(imdb_df$duration,na.rm=T)
  min.1<- min(imdb_df$duration,na.rm=T)
  print(paste("movie title with minimum length",imdb_df$title[which(imdb_df$duration==min.1)]))
  print(paste("movie title with maximum length",imdb_df$title[which(imdb_df$duration==max.1)]))
}

sort_df<- function(imdb_df){
  #9. Sort the data frame by in the order of when they where released and have higer ratings
  imdb_df2<- arrange(imdb_df,year,desc(imdb_df$imdbRating))
  print(head(imdb_df2))
}

subset_df<-function(movie_df){
  #10. Subset the dataframe
  movie_df1<- subset(movie_df,duration >= 30 & duration<=180 & budget<1000000 & gross>2000000)
  print(head(movie_df1))
}

dupl_rows<- function(diamonds_df){
  #11. Count the duplicate rows of diamonds DataFrame"
  res<- sum(complete.cases(diamonds_df))-sum(complete.cases(distinct(diamonds_df)))
  print(res)
}

drop_row<- function(diamonds_df){
  #"12. Drop rows in case of missing values in carat and cut columns"
  diamonds_df1<- diamonds_df[complete.cases(diamonds_df$carat,diamonds_df$cut),]
  print(diamonds_df1)
}

sub_numeric<- function(diamonds_df){
  #13. Subset the dataframe with only numeric columns"
  diamonds_df2<- select_if(diamonds_df, is.numeric)
  print(head(diamonds_df2))
}

volume<- function(diamonds_df){
  #"14. Compute volume as (xyz) when depth is greater than 60"
  vol=diamonds_df$x*diamonds_df$y*(as.numeric(diamonds_df$z))
  for(i in 1:nrow(diamonds_df)){
    if(diamonds_df$depth[i]>60){
      diamonds_df$volume[i]=vol[i]}
    else
    {diamonds_df$volume[i]=8
    }
  }
  print(diamonds_df)
}

impute<- function(diamonds_df){
  #"15. Impute missing price values with mean."
  diamonds_df$price[which(is.na(diamonds_df$price))]<- mean(diamonds_df$price,na.rm=T)
  print(head(diamonds_df$price))
}
