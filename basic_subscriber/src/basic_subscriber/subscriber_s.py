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
        self.x_left = []
        self.y_left = []
        self.x_right = []
        self.y_right = []
        self.sub_ = self.create_subscription(String, "points",self.msgCallback,10)
    def msgCallback(self, msg):
        arr = list(map(float,msg.data.split()))
        self.x.append(arr[0])
        self.x_left.append(arr[1])
        self.x_right.append(arr[2])
        self.y.append(arr[3])
        self.y_left.append(arr[4])
        self.y_right.append(arr[5])
        self.get_logger().info("%s %s %s %s" % (arr[0],arr[1],arr[2],arr[3]))
        self.counter += 1
        if self.counter == 155:
            result_x = np.array(self.x)
            result_y = np.array(self.y)
            x_total = np.array([])
            y_total = np.array([])
            for i in range(len(result_x)-1):
                if result_x[i+1]< result_x[i]:
                    cubic_spliner = interp1d([result_x[i+1],result_x[i]],[result_y[i+1],result_y[i]])
                    samples = np.linspace(result_x[i+1],result_x[i],101)
                    x_total = np.concatenate((x_total,samples[::-1]))
                    y_total = np.concatenate((y_total,cubic_spliner(samples)[::-1]))
                else:
                    cubic_spliner = interp1d([result_x[i],result_x[i+1]],[result_y[i],result_y[i+1]])
                    samples = np.linspace(result_x[i],result_x[i+1],101)
                    x_total = np.concatenate((x_total,samples))
                    y_total = np.concatenate((y_total,cubic_spliner(samples)))
            plt.plot(self.x_left+[self.x_left[0]],self.y_left+[self.y_left[0]],color='red')
            plt.plot(np.concatenate((x_total,np.array([x_total[0]]))),np.concatenate((y_total,np.array([y_total[0]]))),color="blue")
            plt.plot(self.x_right+[self.x_right[0]],self.y_right+[self.y_right[0]],color="green")
            plt.xlabel("X")
            plt.ylabel('y')
            plt.grid(True)
            plt.savefig("/ros2_ws/output/result.png", dpi = 300,bbox_inches='tight')
            plt.close('all')
            rclpy.shutdown()
            


def main():
    rclpy.init()
    basic_subscriber = BasicSubscriber()
    rclpy.spin(basic_subscriber)
if __name__ == '__main__':
    main()