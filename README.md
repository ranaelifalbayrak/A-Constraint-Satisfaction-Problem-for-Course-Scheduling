# A Constraint Satisfaction Problem for Course Scheduling 

## Overview

The objective is to assign time slots and classrooms to courses while adhering to specified constraints.

## Problem Statement

The available time slots are predetermined: Mon1, Mon2, ..., Mon8, Tue1, Tue2, ..., Tue8, ..., Fri1, Fri2, ..., Fri8. 
These represent the first, second, ..., eighth hours of Monday, Tuesday, ..., Friday, respectively.
The constraints are below:
- Exclusive Classroom Assignment: Classrooms can be assigned to only one course at a time.
- Capacity Compliance: The number of students in a course must NOT exceed the capacity of the assigned classroom.
- Instructor Availability: Instructors can teach only one course at a time.
- Consecutive Scheduling: The time slots assigned to a course must be consecutive. For instance, Mon1 and Mon2 are consecutive time slots.
There is a lunch break between the 4th and 5th hour each day. Thus, for instance, Mon4 and Mon5 are NOT consecutive time slots!
- Instructor Preferences Compliance: Instructor preferences must be accommodated. For example, an instructor may wish to teach only on Tuesdays. These preferences are mandatory, NOT soft constraints.
- Coordination Restrictions: Coordinated courses, which are typically taken together by the same students, must NOT be scheduled at the same time.

## Files Provided  

Courses are specified in courses.csv. Each row is dedicated to one course, with columns for:
- Course name (unique identifier)
- Instructor
- Number of students (the classroom must accommodate at least this number)
- Number of hours per week (indicating the consecutive hours needed for the course)
Classrooms are specified in classrooms.csv. Each row is dedicated to a classroom, with columns for:
- Classroom name (unique identifier)
- Capacity \n
Instructor preferences are specified in preferences.csv. Each instructor is listed at most once, with each row reflecting their preferred time slots. Columns are for:
- Instructor name (unique identifier)
- Preferred time slots (a subset of all time slots, listed as a space-separated sequence)
Coordinated courses are specified in coordinations.csv. Each row lists a group of coordinated courses, separated by space. A course name may appear in multiple coordination groups.
As solutions, files are created and named as 1.csv, 2.csv, ..., with each file representing a distinct solution.

## Execution
Two command line arguments: the first for the input directory, the second for the output directory. For instance:
- python3 ceng461_hw1_123456.py "/home/ceng461/hw1/problem1" "/home/ceng461/hw1/solutions1"
For the above example, courses.csv etc. must be found in /home/ceng461/hw1/problem1 and 1.csv etc. is generated in /home/ceng461/hw1/solutions1.
