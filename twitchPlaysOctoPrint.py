#Define the imports
import twitch
import octoApi
import argparse

class TwitchPlaysOctoPrint:
    def __init__(self,twitch_username,twitch_key,octopi_ip,octopi_key):
        self.tw = twitch.Twitch()
        self.tw.twitch_connect(twitch_username, twitch_key)
        self.oc = octoApi.OctoApi(octopi_ip,octopi_key)

    def run(self):
        #The main loop
        while True:
            try:
                #Check for new mesasages
                new_messages = self.tw.twitch_recieve_messages();
            
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
                            self.oc.send_gcode(gcode_cmd)

            except KeyboardInterrupt:
                print("Closing...")
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Twitch Plays Octoprint')
    parser.add_argument('-u','--twitch_user', type=str, help='Twitch username', required=True)
    parser.add_argument('-t','--twitch_key', type=str, help='Twitch Key', required=True)
    parser.add_argument('-i','--oct_ip', type=str, help='Octoprint IP', required=True)
    parser.add_argument('-o','--oct_key', type=str, help='Octoprint API Key', required=True)

    args = parser.parse_args()

    twPlOct = TwitchPlaysOctoPrint(args.twitch_user,args.twitch_key,args.oct_ip,args.oct_key)
    twPlOct.run()
