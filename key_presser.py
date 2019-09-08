#Define the imports
import twitch
import keypresser
import keyholder
t = twitch.Twitch();
k = keypresser.Keypresser();
 
#Enter your twitch username and oauth-key below, and the app connects to twitch with the details.
#Your oauth-key can be generated at http://twitchapps.com/tmi/
username = "benknight135";
key = "oauth:p5s2xoxm08qq80ncspl0z4iop962fm";
t.twitch_connect(username, key);
 
#The main loop
while True:
    #Check for new mesasages
    new_messages = t.twitch_recieve_messages();
 
    if not new_messages:
        #No new messages...
        continue
    else:
        for message in new_messages:
            #Wuhu we got a message. Let's extract some details from it
            msg = message['message'].lower()
            username = message['username'].lower()
            print(username + ": " + msg.encode('utf-8'));
 
            #This is where you change the keys that shall be pressed and listened to.
            #The code below will simulate the key q if "q" is typed into twitch by someone
            #.. the same thing with "w"
            #Change this to make Twitch fit to your game!
            if msg == "w": keyholder.holdForSeconds(msg, 0.3);
            if msg == "s": keyholder.holdForSeconds(msg, 0.3);
            if msg == "a": keyholder.holdForSeconds(msg, 0.1);
            if msg == "d": keyholder.holdForSeconds(msg, 0.1);
            if msg == "e": keyholder.holdForSeconds(msg, 0.5);
            if msg == "q": keyholder.holdForSeconds(msg, 0.1);
            if msg == "t": keyholder.holdForSeconds(msg, 0.5);