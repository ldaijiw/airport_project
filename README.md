# Airport Project

Created by:
- [Leo Waltmann](https://github.com/ldaijiw)
- [Jared Solano](https://github.com/jaredsparta)
- [Sam Turton](https://github.com/samturton2)
- [Maciej Sokol](https://github.com/mattsokol79) 
- [Ubaid-ir-rehman Muhammad](https://github.com/ubaid97)

<br>
 
# Contents

1. [Introduction](#Introduction)
2. [Agile and Scrum](#Agile-and-Scrum)
3. [Database](#Database)
4. [Python Classes](#Python-Classes)
5. [Terminal UI](#Terminal-UI)

<br>

## Introduction

In this project we were tasked to design a flight trip booking system for airport staff and create a user-friendly Terminal UI. We were given a list of user stories that outlined the basic requirements for the product. The specification detailed that staff using the UI should be able to:
- Create a new Passenger using their basic personal information such as a name and passport number
- Create a flight trip with a specific destination
- Assign and/or change a plane to a given flight trip
- Login to perform any necessary actions
- Add passengers to a flight trip, and sell tickets to them
- Generate a flight attendees list detailing a passenger's name and passport number for a given flight 

We also added the following features as an increment after delivering the initial product:
- Ability for passengers to log in (once their details have been added to the database) and view available flights, as well as their current flight details (if a booking has been made in their name)
- Encryption of the login details for both staff and passengers in the database
- Added a hierarchy of staff with 2 levels: level 1 having restricted access, and level 2 having unrestricted access to all functions
- Ability for staff level 2 to find total profit made for a given flight trip
- Began a front-web application to create an intuitive way to perform the methods outlined by the initial requirements.

<br>

### Tools

For this project we used the following tools, methods, and languages:
- Python
- SQL
- AWS Relational Database Service (RDS)
- Test Driven Development
- HTML

<br>

## Agile and Scrum

- As a group we decided to use the Scrum framework to implement Agile, with a focus on the continuous delivery of smaller incremental changes. 
    - Rather than planning out the entire week, we created a product backlog outlining the user stories and potential additional features as epic stories 
    - We used a scrum board created via [Trello](https://www.trello.com/en) to track our progress
    - We planned out daily sprints, starting with sprint planning meetings and ending with sprint retrospectives, which enabled us to be flexible and constantly reassess and reprioritise work as required

- Here was our Trello board, pictured after the completion of the project:
    ![](images/trello.jpg)

<br>

## Database

- A main point of the project was to design a database in which the Airport would store their data

### Entity Relationship Diagram

- We used ERD diagrams to help us in the designing of the database
    - Using diagrams, each of us would have a very clear vision of how our app would connect to our database, thus reducing bugs and errors
    - It allowed us to create optimal SQL scripts to ensure the database was seeded how we wanted it to be

![](images/erd.png)

### Seeding the database
- Testing the app required the database to be seeded as without any data, queries could not be made

- We made use of a random data generator called [mockaroo](https://www.mockaroo.com/)
    - The SQL files with mock data can be found in `data` 
<br>

## Python Classes
- We implemented OOP as our main programming paradigm, allowing us to very easily implement DRY and build atop already existing code

<br>

### Git branching
- create new branch
```git branch <new_branch>```
- switch to new branch
```git checkout <new_branch>```
- add, commit and push your changes to the repo branch
```git push -u origin <new_branch>```
- On github request a merge to main
- Discuss and accept the pull request
- Delete the old branch locally
```git branch -d <branch_to_delete>```

<br>

## Terminal UI
- The terminal UI represented a way for staff and passengers at the airport to be able to do what they needed to do, as outlined previously in the `Introduction`

- We created three separate classes to outline the different possibilities:
    1. A base class called 