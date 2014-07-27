## Coursera: Getting and Cleaning Data
## Project: Explore Smartphone data set
## Description: Read in selected data from flat files into a tidy data set
#

library(stringr)
library(plyr)

## Read in flat files

columnNames <- read.table(file= 'UCI HAR Dataset/features.txt', col.names = c('col_index', 'col_name'),
                          header= FALSE, colClasses= c('numeric', 'character')
                          )
activityNames <- read.table(file= 'UCI HAR Dataset/activity_labels.txt', 
                            col.names = c('activity_cd', 'activity_name'),
                          header= FALSE, colClasses= c('numeric', 'character')
                          )
trainData <- read.table(file= 'UCI HAR Dataset/train/X_train.txt', col.names = columnNames$col_name,
                        header= FALSE
)
trainDataActivity <- read.table(file= 'UCI HAR Dataset/train/y_train.txt', col.names = c('activity_cd'),
                                    header= FALSE, colClasses= 'character'
)
trainDataSubject <- read.table(file= 'UCI HAR Dataset/train/subject_train.txt', col.names = c('subject_id'),
                                   header= FALSE, colClasses= 'character'
)
trainData$activity_cd <- trainDataActivity$activity_cd
trainData$subject_id <- trainDataSubject$subject_id

testData <- read.table(file= 'UCI HAR Dataset/test/X_test.txt', col.names = columnNames$col_name,
                        header= FALSE
)
testDataActivity <- read.table(file= 'UCI HAR Dataset/test/y_test.txt', col.names = c('activity_cd'),
                                    header= FALSE, colClasses= 'character'
)
testDataSubject <- read.table(file= 'UCI HAR Dataset/test/subject_test.txt', col.names = c('subject_id'),
                                   header= FALSE, colClasses= 'character'
)
testData$activity_cd <- testDataActivity$activity_cd
testData$subject_id <- testDataSubject$subject_id

## Retain only the data we want

selectedVarIndex <- c(grep(columnNames$col_name, pattern= 'mean()', value = FALSE), 
                      grep(columnNames$col_name, pattern= 'Mean()', value = FALSE),
                      grep(columnNames$col_name, pattern= 'std()', value = FALSE),
                      grep(names(testData), pattern= 'subject_id', value = FALSE),
                      grep(names(testData), pattern= 'activity_cd', value = FALSE))

selectedTrainData <- trainData[, selectedVarIndex]
selectedTestData <- testData[, selectedVarIndex]

## Merge the two data sets

selectedData <- rbind(selectedTrainData, selectedTestData)

## Merge in activity names

selectedData <- merge(x= selectedData, y= activityNames, by= 'activity_cd', sort= FALSE)

## Summarize the variables by subject and activity

# Get all the unique values
subjectActivity <- selectedData[!duplicated(selectedData[, c('subject_id', 'activity_name')]), c('subject_id', 'activity_name')]

result <- mapply(subjectActivity$subject_id, subjectActivity$activity_name, 
                 FUN = function(s, a){
                   subset <- selectedData[selectedData$subject_id == s & selectedData$activity_name == a, ]
                   # we don't want to sum these columns, so delete them
                   subset$subject_id <- NULL
                   subset$activity_name <- NULL
                   subset$activity_cd <- NULL
                   sums <- apply(subset, 2, mean, na.rm= TRUE)
                   sums_df <- data.frame(t(sums))
                   sums_df$subject_id <- s
                   sums_df$activity_name <- a
                   return(sums_df)
                   }
                 )
averageBySubjectActivity <- t(result)

## Write out the data set

write.csv(selectedData, 'tidyData.csv', sep= ',')


