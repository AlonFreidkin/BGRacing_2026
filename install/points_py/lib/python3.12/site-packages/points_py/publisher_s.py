import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
class BasicPublisher(Node):
    def __init__(self,x,y):
        super().__init__("basic_publisher")
        self.pub_ = self.create_publisher(String,"points",10)
        self.x = x
        self.y = y
        self.counter = 0
        self.frequency_= 0.0625
        self.timer_ = self.create_timer(self.frequency_, self.timerCallback)
    def timerCallback(self):
        if self.counter < len(self.x):
            msg = String()
            msg.data = "%s %s" % (self.x[self.counter],self.y[self.counter])
            self.pub_.publish(msg)
            self.counter += 1
        else:
            self.destroy_node()
def main():
    rclpy.init()
   
    df = pd.read_csv('BrandsHatchLayout.csv')
    num_rows, num_cols = df.shape
    print(df['x'][160])
    x_left = np.array(df['x'][1:157])
    y_left = np.array(df['y'][1:157])
    x_right = np.array(df['x'][158:])
    y_right = np.array(df['y'][158:])
    x = 0.5*(x_left+x_right)
    y = 0.5*(y_left+y_right)
    basic_publisher = BasicPublisher(x,y)
    rclpy.spin(basic_publisher)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
