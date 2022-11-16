import csv
import random
import smtplib
from email.message import EmailMessage

PARTICIPANTS_FILE_PATH = 'participants.csv'

# set your email and password
# please use App Password
email_address = "email_address@gmail.com"
app_password = 'mail app password'

def load_participants(file):
    with open(file, newline='') as csvfile:
        file = csv.reader(csvfile, delimiter=',', quotechar='|')

        participants = {}
        for name, email, buy_present_for_name in file:
            participants[name] = dict(email=email, name=name, buy_present_for_name=buy_present_for_name)
        return participants
    
def lottery_machine(participants):
    
    occupied = []
    
    for name, _ in participants.items():
        buys_present_for = name
        while buys_present_for == name: 
            buys_present_for, buys_present_for_data  = random.choice(list(participants.items()))

            if buys_present_for in occupied:
                buys_present_for = name
        
        occupied.append(buys_present_for)
        participants[name]['buys_present_for'] = buys_present_for_data['buy_present_for_name']
    return participants

def send_sms(receiver):        
    message=f"UWAGA UWAGA! To nie są ćwiczenia! {receiver['name']}, w tym roku (czy Ci się to podoba czy nie) sprawisz radość {receiver['buys_present_for']}. Tylko się postaraj! ;)"
    
    # create email
    msg = EmailMessage()
    msg['Subject'] = "Świąteczna loteria na Konwaliowej! Wersja online!"
    msg['From'] = "szwajkajakub@gmail.com"
    msg['To'] = receiver['email']
    msg.set_content(str(message))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, app_password)
        smtp.send_message(msg)


def main( ):
    participants = load_participants(PARTICIPANTS_FILE_PATH)
    print(participants)
    print('Starting lottery machine...')
    result = lottery_machine(participants)
    print('Machine stopped!')
    
    for _ ,participant in result.items():
        send_sms(participant)
        print(f"email wyslany do: {participant['name']}")
        

if __name__ == "__main__":
    main( )