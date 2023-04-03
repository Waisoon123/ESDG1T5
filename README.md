# ESDG1T5 - SMU ESD Module 2022/23 Sem2 G1T5
## initial Setup
1. The folder should be placed under 'C:\wamp64\www\' e.g. folder ESDG1T5 will be at 'C:\wamp64\www\ESDG1T5'.
2. Run the Wamp and Docker server.
3. Navigate into the sql folder 'C:\wamp64\www\ESDG1T5\sql' and run the windows commpand prompt there by typing 'cmd' into the directory bar.
4. Open and edit 'load_sql_script.py' on line 28 of the file. Change the email to one you have access to. This is used later to send an OTP email. (preferably not a school outlook email as there is quite a delay or will be blocked).
5. Back to the windows command prompt, enter 'python load_sql_script.py' to populate MySQL database with dummy data.
6. Navigate back to 'C:\wamp64\www\ESDG1T5' folder and open another windows command prompt there.
7. In the prompt, run 'docker-compose build'.
8. Once the image has been built, run 'docker-compose up -d'.
9. On a new windows prompt tab, run 'app.py'. (This is used for making payment).
### Initial setup has been completed. There should be 3 windows commpand prompt tabs.

## Use Case 1
User browses for available rooms within a specified date.
1. Open a browser and go to the url 'http://localhost:5000'.
2. You will now be at the home page. At the bottom of the screen, there is a search box to indicate check in and check out dates.
3. Select '03/11/2023' for check-in and '03/15/2023' for check-out. (dummy data contains those 2 dates. you can add more by editing load_sql_script.py).
4. Click the 'Search' button on the right-side of the search box.
5. You will now be redirected to a page that shows all the rooms available within the specified check in and check out dates.
### End of Use Case 1

## Use Case 2
1. Navigate to ‘http://localhost:5000’ and select ‘Make Reservation’ in the top right nav bar.
2. Fill in the details. Name, gender, email, start date (03-04-2023), end date (03-04-2023), room type (Single Room), and quantity (any number < 50). The specifics are due to the dummy data populated in the database.
3. Select ‘Confirm’ to make the reservation.

### End of Use Case 2

## Use Case 3
User cancels a reservation.
1. Open a browser and go to the url 'http://localhost:5000/Reservation_Details.html'.
2. Type '1' into the input box and select 'Retrieve'. (Id of 1 is pre-defined in the database.)
3. An OTP will be sent to your email specified during the initial setup. You will be redirected to another page to enter the OTP.
4. When received, enter the OTP into the input box and select "Submit".
5. You will then be redirected to a page to confirm your cancellation.
6. Select 'Yes, I wish to cancel my reservation.'.
7. Your refund will be given and you will then be redirected to the home page. You will also be notified of the cancellation in your email.
### End of Use Case 3
