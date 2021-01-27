--- Infection Detection USERS MANUAL ---

# OVERVIEW 

Welcome to Infection Detection, where you can calculate the probability of COVID-19 infection in a given campus, in a given class, for a given semester. You will arrive at our homepage which describes what you can find in the website. If you scroll down, you can actually find 4 news articles related to COVID-19 on college campuses. If you are on Google Chrome, some
of these news articles will likely ask for you to sign in with a google account. Some articles such as "The Atlantic" and "AP" will also likely ask you to subscribe or sign up with an email to receive more articles.
All of these messages can be ignored to read more of the articles.

On the top of the homescreen, you can see 4 tabs, -- home, risk calculator, university policies, and CDC guidelines --. As an overview, the home page is the main page of the website. The risk calculator tab is where you will begin the process
of finding your probablity of infection for a given semester and given campus. After clicking a campus on the map, you will be redirected to a calculator page where you will be asked for inputs. Next is the university policies tab.
Here is a dropdown menu that includes the policies for returning to campus and mitigation of COVID-19. For many schools, you can see the PDF version of this policy, but for the university of chicago, you will actually find a video
the school created to describe their policies and what to expect for the return of the semester. The website is implemented so that only one file in the accordion can be opened at a time. If you open MIT's file, the file is opened
to see the university's manual and campus regulations. When you click on another universities file, the dropdown inlcuding MIT's manual will close, opening up the dropdown for the other university clicked. After this tab is the CDC
guidelines tab. Here you can find a quick run down of the CDC's reccomendations to prevent further mitigation of the virus as well as what to do if you have been in close contact with a person who has been confirmed or suspected
of having COVID. While this tab is only meant to advise people, we have also linked the CDC website on the bottom of the page to look into the official guidelines and regulations the CDC have posted. The final tab is the infection
probability tab. After submitting the calculation form for the given univeristy clicked in the map under risk calculator, you will be redirected to this tab with your probability of infection displayed as a percent. This will be your
probability of infection for a given class in a semester. If the probability is below 1%, the probability will be displayed in green. On the other hand, if the probability is above 1%, the probability will be displayed in red. Below
this probability you will also find two buttons guiding you to visit the university policicie's tab to look into what your college has implemented to prevent the mitigation of COVID, and also guiding you to visit the CDC guidelines
tab to learn more about how YOU could also prevent the spread and be safe.

To talk more about the calculations, after clicking for the desired college you are interested in, all forms will require you to input the campus positivity rate which we have linked on the page, classroom dimensions, the number of students who attend the class, the amount of time per day you
are in that class, and the number of times you attend that class per semester. Failiure to fill out any of these categories will render an error, asking you to go back and input the fields missed. Optionally, you can also include
the air exchange of the room and the mask filtration efficiency to receive a better probablity. If these areas are not inputted a base case scenario of 1.2 air exchanges and the filtation of a standard procedural mask are used to
create an upper bound to the proability.

Next, well talk more about the set of equations used to get the probability. The model used to calculate the actual probability was developed by The Harvard Doyle Research Group and further revamped by the ES96 Fall 2020
Risk Analysis Team. Using the positivity rate and number of students, which you the user will input, a set number of infecteded students predicted to be in the room is determined. Using this number, along with the viral
particle emission rate and the length of a class period, we calculated the # of viral particles emitted by the infected individuals in the room during the class. From this number and the volume of the room, we calculated
the density of the viral particles in the room. Using this density along with the air exchange rate of the room and the filtration efficiency of the mask being worn, we calculated the local density of viral particles in
the air that someone actually inhales. Then, from this local density, using the average breathing rate and the amount of class per day, we were able to calculate the viral load inhaled per student per semester.hen, finally,
using the infection constant for SARS-CoV-2 and this viral dose, we calculated the probability of infection for each student over the semester. This is the number you will ultimately see on the infection probability page.


-- We hope you enjoy our website! Happy Calculating! --

# SPECIFICATION

## Documentation
This folder contains a proposal folder for the documentation submitted to the CS50 staff for the proposal of this project and a status update on its completion submitted by the site creators. You will also see a file
DESIGN.md describing the technical creation of the website, and last is this document.

## Static
This folder you should see a map folder with the necessary JavaScript files from Simple Maps (the site used to create the Risk Calculator map) in order to visualize said map. Next will be a policies folder with the PDF
version of all college COVID-19 policies, without the sensitive information that previously prevented the creators from embedding the information (UChicago is stored as an MP4 rather than PDF). The stylesheet used
for the website is seen next as c19.css file. Last is an image used in the CDC tab labeled cdc_covid.png (the other image on the site is embedded from a web address).

## Templates
This contains all HTML files to make the website work. First is a colleges folder that has the college calculator pages for each college supported by the site. Following this is the apology HTML rendered when the user
commits an error 400. The rest of the files are the templates for each tab on the website and their design layout (c19layout.html).

## applications.py
Main python file that controls website actions. You will mainly see the functions defined in calculators.py called here along with the proper functions to render or redirect the correct files based off the user
inputs in the college calculator templates.

## calculators.py
Defines all the college calculator functions called in the POST method for the 18 supported U.S. colleges. You can view the method through which the positivity rate is extracted from the respective COVID-19
dashboards (for sites without the information embedded), the conditions that ensure the user completes all required fields in the college calculator forms, and last the calculation of the infection rate based off the
user inputs stored in unicases.db using the calculating methods described at the end of the OVERVIEW section.

## functions.py
Defines the apology function meant to render an image when a user has crashed the website.

## unicases.db
Stores the user form inputs and utilizes BEGIN TRANSACTION and COMMIT to avoid users viewing other user's information if the site is used simultaneously. Each column corresponds to one of the user inputs from the form,
aside from the infection column which is calculated using said inputs and is displayed on the infection probability tab.
