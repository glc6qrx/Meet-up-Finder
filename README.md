# project-2-13: Meetup-finder App

## Common requirements
### Google Login
We use google OAuth as a login, you can login in and out using the button on the top right off any page, and view profile information by clicking on the Profile button on the top menu.
### Something meaninful based on profile
You can save events you are attending to your profile, and you can view those events and information about your profile on the profile page (profile button in top menu)
### Third Party API
We use geodjango to display the location of the events on a map. This map can be viewed on the find events page in the top menu. We also use the Google Maps API to display this map, and the Google Geocoding API to convert user-provided event addresses to longitude/latitude coordinates that can be displayed on the map.
### Project architecture requirements
Our project is built with language (Python 3), framework (Django 3.1), build environment (Travis CI), source control management (GitHub), and cloud hosting (Heroku).
### Postgres
Postgres is our data engine, you can see so in the settings.py file

## Meetup-finder Requirements
### The system shall allow a user to save a set of event types, causes, etc. with their account.
The user can save events to a profile that is made by Google Login. 
### The system shall show events within a certain GPS radius of the user taking place within a specific time range
You can view event location using the map on the Find Events page and filter results with the form that is on the left of the Find Events page. The user can provide a starting address and a distance range, and can filter to only see events within the provided range of the starting address using this.
### Users shall be able to search for events based upon time, type, location, cause, etc
Users can filter events on the find events page using the form on the left side of the page, with parameters such as event name, date range, and event category. A map is also shown with markers for the different events.
### Users shall be able to submit events to the system for posting.
Users can add events using the Add Events page on the top menu


Notes for self:
used virtual environment (env/Scripts, then use activate command)
python manage.py makemigrations, python manage.py migrate, python manage.py makemigrations
