#from __future__ import print_function

import argparse
import os
import sys

PKG_XML_TEMPLATE = \
"""<?xml version="1.0"?>
<package format="2">
  <name>{0}</name>
  <version>0.0.0</version>
  <description>Catkin simple example package</description>
  <maintainer email="your.email@email.com">Your Name</maintainer>
  <license>None</license>

  <buildtool_depend>catkin</buildtool_depend>
  <buildtool_depend>catkin_simple</buildtool_depend>
  <depend>roscpp</depend>
</package>"""

# Extra "{" for real "{"
PKG_CMAKE_TEMPLATE = \
"""cmake_minimum_required(VERSION 2.8.3)
project({0})

add_definitions(-std=c++11)

find_package(catkin_simple REQUIRED)
find_package(Boost REQUIRED)

catkin_simple(ALL_DEPS_REQUIRED)

include_directories(
  ${{Boost_INCLUDE_DIRS}}
)

cs_add_library(
  ${{PROJECT_NAME}}
  src/{0}.cpp
)

cs_add_executable({0}_ros_node src/{0}_ros_node.cpp)
target_link_libraries({0}_ros_node ${{PROJECT_NAME}})

cs_install()
cs_export(LIBRARIES)"""

PKG_NODE_TEMPLATE = \
"""#include <ros/ros.h>
#include "{0}/{0}.h"

int main(int argc, char** argv) {{
  ros::init(argc, argv, "{0}_ros_node");
  ros::NodeHandle nh;
  ros::NodeHandle nh_private("~");

  rosex::DummyExample ex(nh, nh_private);
  ROS_WARN("ROS is spinning ...");
  ros::spin();
  return 0;
}}"""

PKG_SRC_TEMPLATE = \
"""#include "{0}/{0}.h"
// Implement here"""

PKG_HEADER_TEMPLATE = \
"""#ifndef {0}_H_
#define {0}_H_

#include <ros/ros.h>

namespace rosex {{
class DummyExample {{
 public:
  DummyExample(const ros::NodeHandle &nh, const ros::NodeHandle &nh_private)
      : count_(1), nh_(nh), nh_private_(nh_private) {{
    ROS_INFO("DummyExample: %d count", count_);
  }}

 private:
  int count_;
  ros::NodeHandle nh_;
  ros::NodeHandle nh_private_;
}};
}}
#endif"""

PKG_LAUNCH_TEMPLATE = \
"""<?xml version="1.0" encoding="utf-8"?>
<launch>
  <arg name="launch_prefix" default=""/>
  <arg name="config_file" default="$(find {0})/config/config.yaml"/>

  <node pkg="{0}" type="{0}_ros_node" name="{0}_ros_node" output="screen" launch-prefix="$(arg launch_prefix)">
    <rosparam command="load" file="$(arg config_file)" />
  </node>
</launch>"""

PKG_CONFIG_TEMPLATE = \
"""# Example
SensorParams:
  sensor_list:      ["Cam", "VLP16"]
  VLP16:
    type:           kLidar
    max_range:      50.0
    fov:            [rad(2*pi), rad(pi/6)]
  Cam:
    type:           kCamera
    max_range:      5.0
    fov:            [rad(pi/3.0), rad(pi/4.0)]"""

def printInfo(str): print(str)
def printWarn(str): print("\033[93m{}\033[00m".format(str))
def printError(str): print("\033[91m{}\033[00m".format(str))

class PackageTemplate:
  pkg_name = ''
  pkg_root_folder = ''
  pkg_src_folder = ''
  pkg_header_folder = ''
  pkg_launch_folder = ''
  pkg_config_folder = ''

  def __init__(self, name):
    self.pkg_name = name
    self.pkg_root_folder = os.getcwd()+ "/" + self.pkg_name
    self.pkg_src_folder = self.pkg_root_folder + "/src"
    self.pkg_header_folder = self.pkg_root_folder + "/include/" + self.pkg_name
    self.pkg_launch_folder = self.pkg_root_folder + "/launch"
    self.pkg_config_folder = self.pkg_root_folder + "/config"

  def create_folders(self):
    printInfo(self.pkg_name)
    self.create_folder(self.pkg_src_folder)
    self.create_folder(self.pkg_header_folder)
    self.create_folder(self.pkg_launch_folder)
    self.create_folder(self.pkg_config_folder)

  def create_xml(self):
    printInfo('package.xml')
    file_name = self.pkg_root_folder + "/package.xml"
    self.create_file(file_name, PKG_XML_TEMPLATE.format(self.pkg_name))

  def create_cmakelist(self):
    printInfo('CMakeLists.txt')
    file_name = self.pkg_root_folder + "/CMakeLists.txt"
    self.create_file(file_name, PKG_CMAKE_TEMPLATE.format(self.pkg_name))

  def create_node(self):
    printInfo(self.pkg_name + '_ros_node.cpp')
    file_name = self.pkg_src_folder + "/" + self.pkg_name + "_ros_node.cpp"
    self.create_file(file_name, PKG_NODE_TEMPLATE.format(self.pkg_name))

  def create_src(self):
    printInfo(self.pkg_name + '.cpp')
    file_name = self.pkg_src_folder + "/" + self.pkg_name + ".cpp"
    self.create_file(file_name, PKG_SRC_TEMPLATE.format(self.pkg_name))

  def create_header(self):
    printInfo(self.pkg_name + '.h')
    file_name = self.pkg_header_folder + "/" + self.pkg_name + ".h"
    self.create_file(file_name, PKG_HEADER_TEMPLATE.format(self.pkg_name.upper()))

  def create_launch(self):
    printInfo(self.pkg_name + '.launch')
    file_name = self.pkg_launch_folder + "/" + self.pkg_name + ".launch"
    self.create_file(file_name, PKG_LAUNCH_TEMPLATE.format(self.pkg_name))

  def create_config(self):
    printInfo('config.yaml')
    file_name = self.pkg_config_folder + "/" + "config.yaml"
    self.create_file(file_name, PKG_CONFIG_TEMPLATE)

  def done(self):
    printInfo("Finished --> You could compile, source, then launch the node")
    printWarn("roslaunch {0} {0}.launch".format(self.pkg_name))

  def create_file(self, path, content):
    try:
      f = open(path, "w")
      f.write(content)
      f.close()
    except:
      printError("[ERROR] Failed to create file: %s" % path)

  def create_folder(self, path):
    try:
      os.makedirs(path)
    except OSError:
      printError("[ERROR] Failed to create folder: %s" % path)