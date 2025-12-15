import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
class BasicPublisher(Node):
    def __init__(self,x,y,x_left,y_left,x_right,y_right):
        super().__init__("basic_publisher")
        self.pub_ = self.create_publisher(String,"points",10)
        self.x = x
        self.y = y
        self.x_left = x_left
        self.y_left = y_left
        self.x_right = x_right
        self.x_left = x_left
        self.y_right = y_right
        self.counter = 0
        self.frequency_= 0.0625
        self.timer_ = self.create_timer(self.frequency_, self.timerCallback)
    def timerCallback(self):
        if self.counter < len(self.x):
            msg = String()
            msg.data = "%s %s %s %s %s %s" % (self.x[self.counter],self.x_left[self.counter],self.x_right[self.counter],self.y[self.counter],self.y_left[self.counter],self.y_right[self.counter])
            self.pub_.publish(msg)
            self.counter += 1
        else:
            self.destroy_node()
            rclpy.shutdown()
def mid(x,y):
    for i in range(1,len(x)-1):
        x0 = x[i-1]
        x1 = x[i+1]
        y0 = y[i-1]
        y1 = y[i+1]
        x_mid = (x0+x1)/2
        y_mid = (y0+y1)/2
        x[i] = (x[i]+x_mid)/2
        y[i] = (y[i]+y_mid)/2
    return x, y
def main():
    rclpy.init()
   
    df = pd.read_csv('BrandsHatchLayout.csv')
    num_rows, num_cols = df.shape
    x_left = np.array(df['x'][1:157])
    print(len(x_left))
    y_left = np.array(df['y'][1:157])
    x_left, y_left = mid(x_left,y_left)
    x_right = np.array(df['x'][158:])
    y_right = np.array(df['y'][158:])
    x_right, y_right = mid(x_right,y_right)
    x = 0.5*(x_left+x_right)
    y = 0.5*(y_left+y_right)
    basic_publisher = BasicPublisher(x,y,x_left,y_left,x_right,y_right)
    rclpy.spin(basic_publisher)


if __name__ == '__main__':
    main()