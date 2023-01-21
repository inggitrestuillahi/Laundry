import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import curses
import time

class mqtt_chat:
    def __init__(self,host,port,topic,nick_name,curse):
        self.host = host
        self.port = int(port)
        self.topic = topic
        self.nick_name = nick_name
        self.curse = curse
        self.subscribe_msg()
    def subscribe_msg(self):
        self.subscriber = mqtt.Client()
        self.subscriber.on_connect = self.on_connect
        self.subscriber.on_message = self.on_message
        self.subscriber.connect(self.host,self.port);
        self.subscriber.loop_start()
    def send_msg(self,msg):
        waktu = time.localtime()
        msg = time.strftime("%H:%M:%S", waktu)+"  [" +self.nick_name + "] : "+msg
        publish.single(self.topic,msg, hostname=self.host, port=self.port)
    def on_connect(self,client, userdata, flags, rc):
        client.subscribe(self.topic);
    def on_message(self,client,user_data,msg):        
        self.curse.draw_received_msg(msg.payload.decode('utf-8'))

class my_curses:
    def __init__(self):
        self.stdscr = curses.initscr()
        self.show_row = self.show_col = 0 
        self.input_col = 0 
        (self.max_row,self.max_col) = self.stdscr.getmaxyx()
        curses.cbreak()
    def draw_text(self,row,col,msg):
        self.stdscr.addstr(row,col,' '*(self.max_col-1))
        self.stdscr.addstr(row,col,msg)
        self.stdscr.refresh()
    def get_input(self):
        user_input = ''
        while True:
            c = self.stdscr.get_wch()
            if c == '\n':
                self.input_col=2 
                break
            elif c == curses.KEY_BACKSPACE:
                print('!')
                pass
            else:
                user_input+=str(c)
            self.input_col+=1
        return user_input
    def draw_start_window(self):
        self.stdscr.clear()
        self.draw_text(1,0,"#"*(self.max_col-1))
        self.draw_text(2,0,"MQTT antara client dan laundry")
        self.draw_text(3,0,"#"*(self.max_col-1))
    def draw_main_window(self):
        self.stdscr.clear()
        self.draw_text(1,0,"#"*(self.max_col-1));
        self.draw_text(2,0,"Laundry Soang Chatroom");
        self.draw_text(3,0,"#"*(self.max_col-1))
        row = self.max_row-2
        self.draw_text(row,0,"-"*(self.max_col-1))
        self.draw_user_input_area()
        self.show_row = 3
    def draw_user_input_area(self):
        self.draw_text(self.max_row-1,0,' '*(self.max_col-1))
        self.draw_text(self.max_row-1,0,">>")
    def draw_received_msg(self,msg):
        self.show_row+=1
        if self.show_row == self.max_row-2:
            self.show_row = 4   
        self.draw_text(self.show_row,0,msg)
        self.stdscr.move(self.max_row-1,self.input_col)
        self.stdscr.refresh()

if __name__ == "__main__":
    curse = my_curses()
    curse.draw_start_window()
    nick_name = "Laundry Soang"
    topic = "soang"
    chat = mqtt_chat("test.mosquitto.org","1883",str(topic),str(nick_name),curse);
    curse.draw_main_window()
    while True:
        msg = curse.get_input()
        curse.draw_user_input_area()
        chat.send_msg(msg)