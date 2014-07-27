Code Book for Samsung Data Analysis
===================================

###Description: 

This file describes the logic used to produce the output data set. The data is a set of measurements while subject performed the labelled activity. See data readme file for futher details. We take a subset of the measurements for all subjects for analysis.

###Raw files used:

* UCI HAR Dataset\train\subject_train.txt: The ID of each subject for each observation (training set)
* UCI HAR Dataset\train\X_train.txt: The data collected for each observation (training set)
* UCI HAR Dataset\train\y_train.txt: The label for the activity actually being performed by observation (training set)
* UCI HAR Dataset\test\subject_test.txt: The ID of each subject for each observation (training set)
* UCI HAR Dataset\test\X_test.txt: The data collected for each observation (training set)
* UCI HAR Dataset\test\y_test.txt: A code for the activity actually being performed by observation (training set)
* UCI HAR Dataset\activity_labels.txt: A mapping between the code in the data above with a descriptive label
* UCI HAR Dataset\features.txt: A listing of the descriptive column names for the X_train.txt and X_test.txt data above
	
###Logic performed in run_analysis.R:

1. Section 'Read in flat files'
	* We read in the data (X_train.txt and X_test.txt) as numeric fields
	* Since the subject_id and activity labels are in the same row order, we simply attach them to the data frame
	* We name the columns using the field names in features.txt
2. Section 'Retain only the data we want'
	* We are only interested in the mean and standard deviation columns, so we parse the field names to get their column indexes
3. Section 'Merge the two data sets'
	* Use rbind to combine the training and test data sets
4. Section 'Merge in activity names'
	* We merge in the activity_labels.txt data to get descriptive names for fields
5. Section 'Summarize the variables by subject and activity'
	* We create a second data set which averages all fields by subject and activity
	* To perform this, we create a data frame subjectActivity which contains unique combinations of subject_id and activity_name
	* Then, use mapply to run over these combinations, and use apply within each combination to average columns for that particular combination
	* Note the use of the transpose (t) to appropriately combine each row average
6. Section 'Write out the data set'
	* We write out the data set as 'tidyData.csv'

###Variable Descriptions 

Please also refer to original data description features_info.txt

* labels
	* subject_id: ID of the subject
	* activity_cd: code for the activity subject is performing
	* activity_name: name for the activity subject is performing
* Variable kinds (combine the kind with the transform below to get the specific column name)
	* tBodyAcc-XYZ
	* tGravityAcc-XYZ	
	* tBodyAccJerk-XYZ
	* tBodyGyro-XYZ
	* tBodyGyroJerk-XYZ
	* tBodyAccMag
	* tGravityAccMag
	* tBodyAccJerkMag
	* tBodyGyroMag
	* tBodyGyroJerkMag
	* fBodyAcc-XYZ
	* fBodyAccJerk-XYZ
	* fBodyGyro-XYZ
	* fBodyAccMag
	* fBodyAccJerkMag
	* fBodyGyroMag
	* fBodyGyroJerkMag
* Variable transform
	* mean (average value)
	* meanFreq (Weighted average of the frequency components to obtain a mean frequency)
	* std (standard deviation)