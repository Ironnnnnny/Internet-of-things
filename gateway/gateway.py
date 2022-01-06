import serial
import time
import binascii
import paho.mqtt.client as mqtt
import pymysql
# import threading

# SQL连接
db = MySQLdb.connect(host = "47.113.202.253", user = "root", password = "123456", database = "TEST")
cursor = db.cursor()

# 串口连接
ser = serial.Serial("/dev/ttyAMA0", 115200)

# mqtt定义
MQTTHOST = "47.113.202.253"
MQTTPORT = 1883
client = mqtt.Client()
client_cmd = mqtt.Client()

# 接收数据
data = ""
# 存温度数据
temp = ""
wet = ""

# 订阅主题数据
str_Gate_I = ""

# mqtt协议连接+订阅主题
def client_connect():
    client.connect(MQTTHOST, MQTTPORT, 60)
    client.loop_start()
    client_cmd.connect(MQTTHOST, MQTTPORT, 60)
    client_cmd.loop_start()
    client_cmd.subscribe("MODE", 1)
    client_cmd.on_message = on_message_come_cmd


# 处理订阅主题数据+数据处理+发送数据到终端
def on_message_come_cmd(client, userdata, msg):
    global str_Gate_I
    str_Gate_I = str(msg.payload)
    str_Gate_I = str_Gate_I[2:len(str_Gate_I)-1]
    print("订阅主题数据", str_Gate_I)
    if str_Gate_I == "open1":
        value = [0xFC , 0x03 , 0x01 , 0x01 , 0x3D]
    elif str_Gate_I == "close1":
        value = [0xFC , 0x03 , 0x01 , 0x01 , 0x3E]
    elif str_Gate_I == "open2":
        value = [0xFC , 0x03 , 0x01 , 0x01 , 0x3F]
    elif str_Gate_I == "close2":
        value = [0xFC , 0x03 , 0x01 , 0x01 , 0x40]
    ser.write(value)
    print("sendata")


# 收集终端数据+发布主题+添加数据库
def Serial_SendCMD_or_RecvData():
    global data, temp ,wet
    data = ser.inWaiting()
    try:
        if data != 0:
            print(1)
            data = ser.read(2).decode()
            wet = ord(data[0:1])
            temp = ord(data[1:])
            print(2)
            print("温湿度: ",temp,wet)
            client.publish("TH", str(wet)+" "+str(temp), qos=0, retain=False)
            insert_data(temp,wet)
            ser.flushInput()
    except UnicodeDecodeError:
        print("UnicodeDecodeError")




# 创建表格
def create_table():
    #cursor.execute("drop table if exists test2")
    global cursor
    sql = """CREATE TABLE IF NOT EXISTS test3 (
         `id` int NOT NULL AUTO_INCREMENT,
         `time` varchar(20),
         `temperature` int,
         `humidity` int,
         PRIMARY KEY (`id`)
         )"""
    cursor.execute(sql)

# 添加数据
def insert_data(temp,wet):
    global db, cursor
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    sql = "INSERT INTO test3 (time, temperature,humidity) VALUES('{0}',{1},{2});".format(t, temp, wet)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

#执行函数
if __name__=='__main__':
    client_connect()
    create_table()
    while True:
        Serial_SendCMD_or_RecvData()