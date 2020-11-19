# project-2-13: Meetup-finder App

## Common requirements
### Google Login
We use google OAuth as a login, you can login in and out using the button on the top right off any page, and view profile information by clicking on the Profile button on the top menu.
### Something meaninful based on profile
You can save events you are attending to your profile, and you can view those events and information about your profile on the profile page (profile button in top menu)
### Third Party API
We use geodjango to display the location of the events on a map. This map can be viewed on the find events page in the top menu. 
### Project archetecture requirements
Our project is built with language (Python 3), framework (Django 3.1), build environment (Travis CI), source control management (GitHub), and cloud hosting (Heroku).
### Postgres
Postgres is our data engine, you can see so in the settings.py file

## Meetup-finder Requirements
### The system shall allow a user to save a set of event types, causes, etc. with their account.
The user can save events to a profile that is made by Google Login. 
### The system shall show events within a certain GPS radius of the user taking place within a specific time range
You can view event location using the map on the Find events page, or filter results with the form that is on the right of the Find Events page. You can filter what events show up on the map using this. 
### Users shall be able to search for events based upon time, type, location, cause, etc
Users can filter events on the find events page using the form on the right side of the page
### Users shall be able to submit events to the system for posting.
Users can add events using the Add events page on the top menu
