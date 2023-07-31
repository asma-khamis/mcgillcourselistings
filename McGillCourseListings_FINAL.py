#June 2023
#Web Scraping Program for SUS Syllabus Repository

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

#Get webdriver
driver=webdriver.Chrome()

#Create a list for each element
codes=[]
titles=[]
faculties=[]
depts=[]
credits=[]
semesters=[]
levels=[] 
courselinks=[] 

#Open URL - could use the main one, but I've used the one already filtered by Fac of Sci
driver.get("https://www.mcgill.ca/study/2023-2024/courses/search?f%5B0%5D=field_faculty_code%3ASC")

#Extract content
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

#Each course is in its own views-row class, so loop through each of them. This is the loop for the first page of course results.
for a in soup.findAll('div', attrs={'class':'views-row'}):
    
    code=a.find('div', attrs={'class':'views-field-field-course-title-long'})
    codes.append(code.text)
    
    title=a.find('div', attrs={'class':'views-field-field-course-title-long'})
    titles.append(title.text)
    
    faculty=a.find('span', attrs={'class':'views-field-field-faculty-code'})
    faculties.append(faculty.text)
    #These should already all be Science since the webpage is filtered
    
    dept=a.find('span', attrs={'class':'views-field-field-dept-code'})
    depts.append(dept.text)
    
    credit=a.find('div', attrs={'class':'views-field-field-course-title-long'})
    credits.append(credit.text)
    
    semester=a.find('span', attrs={'class':'views-field-terms'})
    semesters.append(semester.text)
    
    level=a.find('span', attrs={'class':'views-field-level'})
    levels.append(level.text)
    
#Open each of the subsequent pages of course results, and loop through them. Manually check how many pages there are to edit the for loop accordingly- here it's 68.
for i in range(1,68):
    
    pagenumber=str(i)
    driver.get("https://www.mcgill.ca/study/2023-2024/courses/search?f%5B0%5D=field_faculty_code%3ASC"+"&page="+pagenumber)
    
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    
    for a in soup.findAll('div', attrs={'class':'views-row'}):
        
        code=a.find('div', attrs={'class':'views-field-field-course-title-long'})
        codes.append(code.text)
        
        title=a.find('div', attrs={'class':'views-field-field-course-title-long'})
        titles.append(title.text)
        
        faculty=a.find('span', attrs={'class':'views-field-field-faculty-code'})
        faculties.append(faculty.text)
        
        dept=a.find('span', attrs={'class':'views-field-field-dept-code'})
        depts.append(dept.text)
        
        credit=a.find('div', attrs={'class':'views-field-field-course-title-long'})
        credits.append(credit.text)
        
        semester=a.find('span', attrs={'class':'views-field-terms'})
        semesters.append(semester.text)
        
        level=a.find('span', attrs={'class':'views-field-level'})
        levels.append(level.text)       

#Store data in CSV file. Codes, titles, and credits are in the same line. 
df=pd.DataFrame({'Codes, Titles, Credits':codes,'Faculty':faculties, 'Department':depts, 'Semester':semesters, 'Level':levels, 'Instructors':instructors})
df.to_csv('courses.csv', index=False, encoding='utf-8')

#Save to excel file 
read_file = pd.read_csv (r'courses.csv')
read_file.to_excel (r'courses_excel.xlsx', index = None, header=True)