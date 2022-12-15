from datetime import date, timedelta
import smtplib, ssl, csv
from email.message import EmailMessage

smtp_server = "smtp.gmail.com"
port = 587
sender_email = "marija.versada.reminder@gmail.com"
password = 'dwzbodworwnpenwj'
file_path = "persons.csv"
persons = []

def validate_file(file_name):
    list_of_errors = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            if len(row) == 3:
                persons.append({
                    "name": row[0],
                    "email": row[1],
                    "birthdate": row[2]
                })
            else:
                list_of_errors.append(f"Row [{row}] doesn't have 3 columns.")

    for person in persons:
        if "name" not in person or not person["name"]:
            list_of_errors.append(f"Person {person} doesn't have the 'name' set.")
        if "email" not in person or not person["email"]:
            list_of_errors.append(f"Person {person} doesn't have the 'email' set.")
        
        try:
            year, month, day = person["birthdate"].split('-')
            birthdate = date(int(year), int(month), int(day))
            if birthdate >= date.today():
                list_of_errors.append(f"Birhdate of the person {person} is in the future. It must be in the past.")
        except ValueError:
            list_of_errors.append(f"Cannot parse birthdate for person {person}")

    if list_of_errors:
        return False, list_of_errors

    return True, list_of_errors

def get_message(person, birthday_person, birthday):
    msg = EmailMessage()
    message = f"""
    Hi {person['name']},
    This is a reminder that {birthday_person['name']} will be celebrating birthday on {birthday}.
    There are 7 days left to get a present!
    """
    msg.set_content(message)

    msg['Subject'] = f"Birthday Reminder: {birthday_person['name']}'s birthday on {birthday}"
    msg['From'] = sender_email
    msg['To'] = person["email"]

    return msg

def send_email(message):
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.connect(smtp_server,port)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)
    except Exception as e:
        print(e)
    finally:
        server.quit()


if not file_path:
    print("You must provide file as an option when executing the script!")
else:
    valid, list_of_errors = validate_file(file_path)
    if valid:
        for birthday_person in persons:
            year, month, day = birthday_person["birthdate"].split('-')
            birthdate = date(int(year), int(month), int(day))
            today = date.today()
            birthday = date(today.year, birthdate.month, birthdate.day)

            # birthday is in 7 days
            if today + timedelta(days=7) == birthday:
                for person in persons:
                    # do not send email to the birthday person
                    if person != birthday_person:
                        message = get_message(person, birthday_person, birthday)
                        send_email(message)
    else:
        print("File is not valid! List of errors:")
        for error in list_of_errors:
            print(error)



