#Define the imports
import twitch
import octoApi
import argparse
import math
import cmath
import math
import time

class TwitchPlaysOctoPrint:
    def __init__(self,twitch_username,twitch_key,octopi_ip,octopi_key):
        self.twitch_username = twitch_username
        self.twitch_key = twitch_key
        self.octopi_ip = octopi_ip
        self.octopi_key = octopi_key
        self.connect()

    def connect(self):
        self.tw = twitch.Twitch()
        self.tw.twitch_connect(self.twitch_username, self.twitch_key)
        self.oc = octoApi.OctoApi(self.octopi_ip,self.octopi_key)

    def gcode_send_delayed(self,gcode,delay=1):
        for g in gcode:
            self.gcode_send([g])
            time.sleep(delay)

    def gcode_send(self,gcode):
        try:
            self.oc.send_gcode(gcode)
        except:
            print("Error sending gcode. Will re-connect to try and fix the problem")
            self.connect()

    def gcode_shape_line(self,length=50):
        gcode_line_start = "G0 "
        gcode = [gcode_line_start+"X0 Y0 Z10"]
        for x in range(1,length):
            y = x
            gcode.append(gcode_line_start + "X" + str(x) + " Y" + str(y))
        return gcode

    def points_on_circumference(self,center=(0, 0), r=60, n=100):
        return [
            (
                center[0]+(math.cos(2 * math.pi / n * x) * r),  # x
                center[1] + (math.sin(2 * math.pi / n * x) * r)  # y

            ) for x in xrange(0, n + 1)]

    def gcode_shape_circle(self,radius):
        gcode_line_start = "G0 "
        gcode = []
        for p in self.points_on_circumference(r=radius):
            x = str(round(p[0],4))
            y = str(round(p[1],4))
            gcode.append(gcode_line_start + "X" + x + " Y" + y)
            
        return gcode

    def run(self):
        #The main loop
        while True:
            try:
                #Check for new mesasages
                new_messages = self.tw.twitch_recieve_messages()
            
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
                        print(username + ": " + msg_utf8)

                        msg_split = msg_utf8_upper.split(":")
                        print(msg_split)
                        if msg_split[0] == "GCODE":
                            gcode = msg_split[1:]
                            print(gcode)
                            print("Direct GCode turned off for safety")
                            #self.oc.send_gcode(gcode)
                        elif msg_split[0] == "POS":
                            msg_cmd = msg_split[1]
                            if msg_cmd == "X" or msg_cmd == "Y" or msg_cmd == "Z":
                                try:
                                    msg_val = round(float(msg_split[2]),4)
                                    if msg_cmd == "X":
                                        self.oc.set_pos_x(msg_val)
                                    elif msg_cmd == "Y":
                                        self.oc.set_pos_y(msg_val)
                                    elif msg_cmd == "Z":
                                        self.oc.set_pos_z(msg_val)
                                except Exception:
                                    print("Problem in message")
                            else:
                                #split comma seperated position
                                pos_cmd = msg_split[1].split(",")
                                pos_x = round(float(pos_cmd[0]),4)
                                pos_y = round(float(pos_cmd[1]),4)
                                pos_z = round(float(pos_cmd[2]),4)
                                self.oc.set_pos(pos_x,pos_y,pos_z)
                        elif msg_split[0] == "CMD":
                            msg_cmd = msg_split[1]
                            if msg_cmd == "HOME":
                                gcode = ["G28"]
                                self.gcode_send(gcode)
                        '''
                        elif msg_split[0] == "SHAPE":
                            msg_cmd = msg_split[1]
                            if msg_cmd == "CIRCLE":
                                radius = 60
                                if len(msg_split) > 2:
                                    radius = int(msg_split[2])
                                gcode = self.gcode_shape_circle(radius)
                                self.gcode_send_delayed(gcode,0.1)
                            elif msg_cmd == "LINE":
                                length = 50
                                if len(msg_split) > 2:
                                    length = int(msg_split[2])
                                gcode = self.gcode_shape_line(length)
                                self.gcode_send(gcode)
                        '''


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
