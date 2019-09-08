#Define the imports
import twitch
import octoApi
t = twitch.Twitch();
 
#Enter your twitch username and oauth-key below, and the app connects to twitch with the details.
#Your oauth-key can be generated at http://twitchapps.com/tmi/
username = "benknight135";
key = "oauth:p5s2xoxm08qq80ncspl0z4iop962fm";
t.twitch_connect(username, key);
#Enter your octoprint ip and api-key below.
ip = "192.168.0.29"
api_key = "2442EBE31F7E4D7AAA10255C493886D7"
o = octoApi.OctoApi(ip,api_key);
 
#The main loop
while True:
    try:
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
                msg_utf8 = (msg.encode('utf-8'))
                msg_utf8_upper = msg_utf8.upper()
                print(username + ": " + msg_utf8);

                msg_split = msg_utf8_upper.split(":")
                if msg_split[0] == "GCODE":
                    gcode_cmd = msg_split[1:]
                    print(gcode_cmd)
                    #Send message to printer
                    o.send_gcode(gcode_cmd)

    except KeyboardInterrupt:
        print("Closing...")
        break