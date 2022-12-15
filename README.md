# birthday-reminder
Python script which sends an email reminder to all the people from the csv file, 7 days before the birthday of some other person, also from the same file.

## Run instructions
The script can be ran manually, by executing it as a standard Python script from terminal (python3 task.py), or periodically, by setting the cron job.
If data csv file is not valid, the script will print all the errors in it.

## Parameters
The script contains several parameters which can be configured inside the script, by editing variable values:
- smtp_server - email server
- port - email server port
- sender_email - email from which the messages will be sent
- password - password for authenticating to the email server
- file_path - path to the data csv file
