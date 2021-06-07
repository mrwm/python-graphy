#!/usr/bin/env python3
#coding:utf-8

# graphs.py
# Author: William Chung
# Last Updated: 
# Purpose: Creates line or bar graph(s) or donut graphs with the given data
#          points given within a CSV file.
# Program Uses: ./graphs.py
# Notes: 
#       - Requires svgwrite python module
#       - Requires a scecifically formatted csv file.
#
import svgwrite
import math     # for the trig functions
import os       # for file checking

# breaking `with` using `with`
# https://stackoverflow.com/a/23665658
class fragile(object):
  class Break(Exception):
    """Break out of the with statement"""

  def __init__(self, value):
    self.value = value

  def __enter__(self):
    return self.value.__enter__()

  def __exit__(self, etype, value, traceback):
    error = self.value.__exit__(etype, value, traceback)
    if etype == self.Break:
      return True
    return error

def header_count(file_name):
  """
    returns the number of headers in a file
  """
  count = 0
  with fragile(open(file_name, "r")) as file_input:
    for line in file_input:
      c_line_content = line.rstrip("\n").split(",")

      # Check if this is the start of a set of data using config information
      if c_line_content[1] == "r" or c_line_content[1] == "r":
        count += 1
  return count

def dict_to_list(dictionary_in):
  """
    Converts the given dictionary to two separate lists
  """
  item_list = []
  for key, value in dictionary_in.items():
    if type(value) is not list:
      item_list.append(value)
    else:
      item_list.append(value[0])
  return item_list

def conf_graph(line_buffer):
  """
    Parses the given csv file and returns the configuration and colors.
    Will skip to whatever line number given, excluding the initial line.
  """
  config = {}
  height_dictionary = {}
  color_dictionary = {}
  # Open the csv file
  with fragile(open(csv_file, "r")) as csv_input:
    csv_input.readline() # skip the first line

    # skip through the lines that have already been read.
    if line_buffer != 0:
      for num in range(0, line_buffer):
        csv_input.readline()

    # read through the line contents
    c_line_content = ""
    line_count = 0 # keep track of the number of lines read
    for csv_line in csv_input:
      c_line_content = csv_line.rstrip("\n").split(",")

      # Check if this is the start of a set of data using config information
      if c_line_content[1] == "r" and line_count == 0:
        config = {
          "filename" : c_line_content[0],
          "draw_mode" : c_line_content[1],
          "rect_width" : float(c_line_content[2]),
          "v_offset" : float(c_line_content[3]),
          "st_width" : float(c_line_content[4]),
          "dot_radius" : float(c_line_content[5]),
          "show_rect" : c_line_content[6].lower(),
          "show_line" : c_line_content[7].lower(),
        }
      # Check if the config is for circles
      elif c_line_content[1] == "c" and line_count == 0:
        config = {
          "filename" : c_line_content[0],
          "draw_mode" : c_line_content[1],
          "line_stroke_width" : c_line_content[2],
          "make_donut" : c_line_content[6].lower(),
        }

      # Add the rest of the data below the config line (r)
      elif (c_line_content[1] != "r" and c_line_content[1] != "c") and \
          line_count != 0:
        # Set the color of the bars
        c_name = "color_" + str(line_count - 1)
        color_dictionary[c_name] = c_line_content[0]

        # Then set the bar heights
        h_name = "height_list_" + str(line_count - 1)
        h_list = c_line_content[1:]
        # Remove blanks
        while("" in h_list):
          h_list.remove("")
        # Convert the strings to numbers
        for h_index in range(0, len(h_list)):
          h_list[h_index] = float(h_list[h_index])
        height_dictionary[h_name] = h_list

      # Exit the loop if we see another data configuration
      if (c_line_content[1] == "r" and line_count != 0) or \
          (c_line_content[1] == "c" and line_count != 0):
        # Break out of the with loop once a dataset is collected
        raise fragile.Break

      line_count += 1

  line_buffer = line_count
  return [line_buffer, config, height_dictionary, color_dictionary]

#######################################
#######################################
### 
### RECTANGLE
###
#######################################
#######################################
def draw_rect_graph(config, height_dictionary, color_dictionary):
  """
    Draws the rectangle graph with the given hight and color values
  """
  if config["draw_mode"] != "r":
    # toss the data to make a round graph
    draw_round_graph(config, height_dictionary, color_dictionary)
    return

  dwg = svgwrite.Drawing(config["filename"] + ".svg", profile="full")
  v_offset_origin = config["v_offset"]

  if config["show_rect"] == "true":
    # For making the bar graphs
    for group_index in range(1, len(height_dictionary)):
      x_index = 0
      for list_index in range(1, len(height_dictionary["height_list_"+str(group_index)])):
        # draw the boxes
        r_size = height_dictionary["height_list_"+str(group_index)][list_index]
        dwg.add(dwg.rect((x_index, -r_size + v_offset_origin), (config["rect_width"], r_size),
          fill=color_dictionary["color_"+str(group_index)])
        )
        x_index += config["rect_width"]
      v_offset_origin += config["v_offset"]

  if config["show_line"] == "true":
    # For connecting the dots together
    config["v_offset"] = v_offset_origin
    for group_index in range(0, len(height_dictionary)):
      line_points = "M"
      x_index = 0
      l_max = len(height_dictionary["height_list_"+str(group_index)])
      for list_index in range(0, l_max):
        # draw the boxes
        r_size = height_dictionary["height_list_"+str(group_index)][list_index]
        if list_index < l_max-1:
          line_points = line_points + str(x_index) + "," + str(-r_size + v_offset_origin) + ", "
        else:
          line_points = line_points + str(x_index) + "," + str(-r_size + v_offset_origin)
        x_index += config["rect_width"]

      # draw a cubic-bezier-curve path
      dwg.add(dwg.path( d=line_points,
        stroke=color_dictionary["color_"+str(group_index)],
        fill="none",
        stroke_width=config["st_width"])
      )
      v_offset_origin += config["v_offset"]

    # For making the dots at the corner of each rectangle
    v_offset_origin = config["v_offset"]
    for group_index in range(0, len(height_dictionary)):
      x_index = 0
      for list_index in range(0, len(height_dictionary["height_list_"+str(group_index)])):
        # draw the boxes
        r_size = height_dictionary["height_list_"+str(group_index)][list_index]
        dwg.add(dwg.circle(center=(x_index, -r_size + v_offset_origin),
          r=config["dot_radius"],
          fill=color_dictionary["color_"+str(group_index)])
        )
        x_index += config["rect_width"]
      v_offset_origin += config["v_offset"]

  # output our svg image as raw xml
  #print(dwg.tostring())

  # write svg file to disk
  dwg.save()
  print("Exported file:", config["filename"] + ".svg")

#######################################
#######################################
### 
### CIRCLE
###
#######################################
#######################################
def addArc(dwg, current_group, p0, p1, radius, f_color, line_stroke_width):
    """ Adds an arc that bulges to the right as it moves from p0 to p1 """
    args = {'x0':p0[0], 
        'y0':p0[1], 
        'xradius':radius, 
        'yradius':radius, 
        'ellipseRotation':0, #has no effect for circles
        'x1':(p1[0]-p0[0]), 
        'y1':(p1[1]-p0[1])}
    current_group.add(dwg.path(d="M %(x0)f,%(y0)f a %(xradius)f,%(yradius)f %(ellipseRotation)f 0,0 %(x1)f,%(y1)f M0,0"%args,
             fill='none', 
             stroke=f_color, stroke_width=line_stroke_width
            ))

def anglept(angle=0):
  """Finds the location of a point on the circle. This assumes the center is at 0,0"""
  # convert degree to radian, then back to degree
  # reason: python trig functions use radians, but we want degrees
  x_point = math.degrees(math.cos(math.radians(angle)))
  y_point = math.degrees(math.sin(math.radians(angle)))

  # Offset number taken from the calculation for circle_size
  center_offset = 57.29577951308232 * 1.5
  point=[x_point + center_offset, y_point + center_offset]
  return point

def num_to_degree(index=0, list_given=None):
  """
    Calculates the degrees of 360° from the total of the given list
    Note: Degree is cumulative.
          Eg: index=1 will have the degree of 360° of index=0 + index=1
  """
  if list_given == None:
    print("num_to_percent wasn't given a list")
    exit(1)
  total = 0
  divisor = 0
  for num in range(0,len(list_given)):
    total += list_given[num] # add all the list numbers
    if num <= index:
      divisor += list_given[num] # get the sum up to the index given
  return round((divisor / total)*360)

def draw_round_graph(config, height_dictionary, color_dictionary):
  """
    Draws the donut or pie graph with the given hight and color values
  """
  line_stroke_w = 0
  name="circle" # we need a name for the graph, tho it doesn't matter what it is
  dwg = svgwrite.Drawing(filename=config["filename"] + ".svg", size=(175,175))
  current_group = dwg.add(dwg.g(id=name, stroke='red', stroke_width=3, fill='red', fill_opacity=1 ))


  # This is kinda arbitrary, but we want a constant radius, so here it is.
  circle_size = math.degrees(math.sin(math.radians(90)))
  #print(circle_size)

  # Make a solid circle if we don't want a donut
  if config["make_donut"] != "true":
    line_stroke_w = circle_size*2
  else:
    line_stroke_w = config["line_stroke_width"]

  graph_numbers = dict_to_list(height_dictionary)
  graph_colors = dict_to_list(color_dictionary)

  # Look thru all the numbers in the list and graph them out!
  for index in range(0, len(graph_numbers)):
    # Set the starting and ending angles for the circle
    if index == 0 and index != len(graph_numbers):
      # start the first slice at 0
      start_angle = 0
      end_angle = num_to_degree(index, graph_numbers)
    elif index != len(graph_numbers):
      # Start at the last slice calculated
      start_angle = num_to_degree(index-1, graph_numbers)
      end_angle = num_to_degree(index, graph_numbers)
    else:
      # Start the last slice backwards since we're ending the slice at 0
      start_angle = num_to_degree(index, graph_numbers)
      end_angle = 0

    # Set the slice color  
    fill_color = graph_colors[index]
    addArc(dwg, current_group, p0=anglept(end_angle), p1=anglept(start_angle), radius=circle_size, f_color=fill_color, line_stroke_width=line_stroke_w)

  dwg.save()
  print("Exported file:", config["filename"] + ".svg")


################################################################################
################################################################################
print("Please input CSV file name (including the .cvs extention)")
print("Default: sample_data.csv")
csv_file = input("File name: ")

if not os.path.isfile(csv_file):
  csv_file = "sample_data.csv"

print("===")


line_buffer = 0
capture = conf_graph(line_buffer)
line_buffer += capture[0]
draw_rect_graph(capture[1], capture[2], capture[3])
for i in range(0, header_count(csv_file)):
  capture = conf_graph(line_buffer)
  line_buffer += capture[0]
  draw_rect_graph(capture[1], capture[2], capture[3])

#capture = conf_graph(line_buffer)
#line_buffer += capture[0]
#draw_rect_graph(capture[1], capture[2], capture[3])

#capture = conf_graph(line_buffer)
#line_buffer += capture[0]
#draw_rect_graph(capture[1], capture[2], capture[3])

#capture = conf_graph(line_buffer)
#line_buffer = capture[0]
#draw_rect_graph(capture[1], capture[2], capture[3])




