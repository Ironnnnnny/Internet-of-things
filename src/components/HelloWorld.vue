<template>
  <div class="test">
    <el-card class="box-card">
    <el-row><pre style="font-size: 20px">温度:  {{ data2 }}    ℃</pre></el-row>
    <el-divider></el-divider>
    <el-row><pre style="font-size: 20px">湿度:  {{ data1 }}   %RH</pre></el-row>
    <el-divider></el-divider>
    <el-switch
      v-model = "value1"
      on-color = "#13ce66"
      off-color = "#ff4949"
      on-text = "开"
      off-text = "关"
      @change = "changeSwitch1(value1)"
    >
    </el-switch>
    <el-divider></el-divider>
    <el-switch
      v-model = "value2"
      active-color = "#13ce66"
      inactive-color = "#ff4949"
      active-text = "on"
      inactive-text = "off"
      @change = "changeSwitch2(value2)"
    >
    </el-switch>
    </el-card>
  </div>
</template>

<script>
import mqtt from "mqtt";
import { MQTT_SERVICE, MQTT_USERNAME, MQTT_PASSWORD } from "../sysconstant.js";
var client;
const options = {
  connectTimeout: 40000,
  clientId: "mqtitId-Home",
  username: MQTT_USERNAME,
  password: MQTT_PASSWORD,
  clean: true,
};
client = mqtt.connect(MQTT_SERVICE, options);
export default {
  name: "viewtest",
  data() {
    return {
      msg: "",
      data1: "0",
      data2: "0",
      value1: false,
      value2: false,
      mqttData: [],
    };
  },
  created() {
    this.mqttMSG();
  },
  methods: {
    mqttMSG() {
      // mqtt连接
        client.on("connect", () => {
          console.log("连接成功:");
          client.subscribe("TH", { qos: 0 }, (error) => {
            if (!error) {
              console.log("订阅成功");
            } else {
              console.log("订阅失败");
            }
          });
        // 接收消息处理
          client.on("message", (topic, message) => {
            console.log("收到来自", topic, "的消息", message.toString());
            this.msg = message.toString();
            this.mqttData = this.msg.split(" ");
            this.data1 = this.mqttData[0];
            this.data2 = this.mqttData[1];
            console.log(this.data1 , this.data2);
          });
          // 断开发起重连
          // client.on("reconnect", (error) => {
          //   console.log("正在重连:", error);
          // });
          // 链接异常处理
          client.on("error", (error) => {
            console.log("连接失败:", error);
          });
       })
    },
    changeSwitch1(data) {
      console.log(data)
      if(data == true){
        client.publish("MODE", "open1",{ qos: 0}, (error) =>{
            if (!error) {
              console.log("发布成功");
            } else {
              console.log("发布失败");
            }
          });
      }
      else{
        client.publish("MODE","close1",{ qos: 0}, (error) =>{
            if (!error) {
              console.log("发布成功");
            } else {
              console.log("发布失败");
            }
          });
      }
    },
    changeSwitch2(data) {
      console.log(data)
      if(data == true){
        client.publish("MODE", "open2",{ qos: 0}, (error) =>{
            if (!error) {
              console.log("发布成功");
            } else {
              console.log("发布失败");
            }
          });
      }
      else{
        client.publish("MODE","close2",{ qos: 0}, (error) =>{
            if (!error) {
              console.log("发布成功");
            } else {
              console.log("发布失败");
            }
          });
      }
    }
      
  },
}
</script>

<style scoped>
.test {
  white-space: pre-wrap;
  line-height: 20px;
 
  position: absolute;
  top: 40%;
  left: 47%;
  transform: translate(-40%, -50%);
  
}
.box-card {

  width: 250px;
    
}
</style>
