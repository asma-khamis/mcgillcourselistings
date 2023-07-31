# McGill Course Listings
### Description
Written in Python, this web scraping program compiles all courses offered by McGill's Faculty of Science in a given eCalendar year, in this case 2023-2024. The code, title, credits, department, semesters offered, and level of each course is obtained and formatted into a spreadsheet.

This course information can then be used or sorted as desired- in this case, the subsequent application was to obtain recent syllabi from instructors of all courses offered in the upcoming year, then upload these entries to the McGill Science Undergraduate Society's publicly-accessible syllabus repository, [found here.](https://susmcgill.ca/science-syllabus-repository)

### How to Run
The libraries I used were Selenium, BeautifulSoup, and Pandas, which I installed using pip3. I also downloaded Chrome WebDriver for Selenium to properly operate the browser.

Afterwards, the `McGillCourseListings_FINAL.py` program can be run by command line or in your Python IDE of choice.

### Explanation
These lines open the libraries and declare the driver to be used.
```
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver=webdriver.Chrome()
```
Then, the program initializes a list for each course property, opens the eCalendar page already filtered by Faculty so it displays solely Science courses, and extracts the content.
```
codes=[]
titles=[]
faculties=[]
depts=[]
credits=[]
semesters=[]
levels=[] 

driver.get("https://www.mcgill.ca/study/2023-2024/courses/search?f%5B0%5D=field_faculty_code%3ASC")
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")
```
This loop then finds the div tag for each course property and appends it to the appropriate list, shown below for course codes as an example.
```
for a in soup.findAll('div', attrs={'class':'views-row'}):
    
    code=a.find('div', attrs={'class':'views-field-field-course-title-long'})
    codes.append(code.text)
```
Since the above loop only goes through the first page of courses, the remaining eCalendar pages are cycled through below, again with each course property appended to its list. Note that course codes are again shown as the example, but the `.find` and `.append` methods are repeated for each course property.
```
for i in range(1,68):
    
    pagenumber=str(i)
    driver.get("https://www.mcgill.ca/study/2023-2024/courses/search?f%5B0%5D=field_faculty_code%3ASC"+"&page="+pagenumber)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    
    for a in soup.findAll('div', attrs={'class':'views-row'}):
        
        code=a.find('div', attrs={'class':'views-field-field-course-title-long'})
        codes.append(code.text)
```
All the information is put into a dataframe, then converted to both .csv and .xlsx files.
```
df=pd.DataFrame({'Courses':codes,'Faculty':faculties, 'Department':depts, 'Semester':semesters, 'Level':levels, 'Instructors':instructors})
df.to_csv('courses.csv', index=False, encoding='utf-8')

read_file = pd.read_csv (r'courses.csv')
read_file.to_excel (r'courses_excel.xlsx', index = None, header=True)
```
### Future Directions
A useful addition would be to implement further HTML parsing to extract the instructors for each course. This information is contained in each individual course page.
