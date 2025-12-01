import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d
class BasicSubscriber(Node):
    def __init__(self):
        super().__init__("basic_subscriber")
        self.counter = 0
        self.x = []
        self.y = []
        self.sub_ = self.create_subscription(String, "points",self.msgCallback,10)
    def msgCallback(self, msg):
        arr = list(map(float,msg.data.split()))
        self.x.append(arr[0])
        self.y.append(arr[1])
        self.get_logger().info("%s %s" % (arr[0],arr[1]))
        if self.counter == 155:
            result_x = np.array(self.x)
            result_y = np.array(self.y)
            np.concatenate((result_x,[self.x[0]]))
            np.concatenate((result_y,[self.y[0]]))
            cubic_spliner = interp1d(result_x,result_y,kind='cubic')
            plt.figure(figsize=(10,6))
            plt.plot(result_x,result_y)
            plt.xlabel("X")
            plt.ylabel('y')
            plt.grid(True)
            plt.savefig("/ros2_ws/output/result.png", dpi = 300,bbox_inches='tight')
            self.destroy_node()
            rclpy.shutdown()
        self.counter += 1
            


def main():
    rclpy.init()
    basic_subscriber = BasicSubscriber()
    rclpy.spin(basic_subscriber)
if __name__ == '__main__':
    main()