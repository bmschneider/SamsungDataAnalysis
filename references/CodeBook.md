# Code Book for Samsung Data Analysis

## Description: 

This file describes the logic used to produce the output data set. The data is a set of measurements while subject performed the labelled activity. See data readme file for futher details. We take a subset of the measurements for all subjects for analysis.

## Raw files used:

* UCI HAR Dataset\train\subject_train.txt: The ID of each subject for each observation (training set)
* UCI HAR Dataset\train\X_train.txt: The data collected for each observation (training set)
* UCI HAR Dataset\train\y_train.txt: The label for the activity actually being performed by observation (training set)
* UCI HAR Dataset\test\subject_test.txt: The ID of each subject for each observation (training set)
* UCI HAR Dataset\test\X_test.txt: The data collected for each observation (training set)
* UCI HAR Dataset\test\y_test.txt: A code for the activity actually being performed by observation (training set)
* UCI HAR Dataset\activity_labels.txt: A mapping between the code in the data above with a descriptive label
* UCI HAR Dataset\features.txt: A listing of the descriptive column names for the X_train.txt and X_test.txt data above
	
## Variable Descriptions 

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