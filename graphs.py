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


print("Please input CSV file name (including the .cvs extention)")
print("Default: sample_data.csv")
csv_file = input("File name: ")
if not csv_file:
  csv_file = "sample_data.csv"

print("===")


def line_count(file_name):
  """
    returns the number of lines in a file
  """
  count = 0
  with fragile(open(file_name, "r")) as file_input:
    for line in file_input:
      count += 1
  return count

def conf_graph(line_buffer):
  """
    Parses the given csv file and returns the configuration and colors.
    Will skip to whatever line number given, excluding the initial line.
  """
  height_dictionary = {}
  color_dictionary = {}
  line_count = 0 # keep track of the number of lines read
  # Open the csv file
  with fragile(open(csv_file, "r")) as csv_input:
    csv_input.readline() # skip the first line

    # skip through the lines that have already been read.
    if line_buffer != 0:
      for num in range(0, line_buffer):
        csv_input.readline()

    # read through the line contents
    c_line_content = ""
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
      elif c_line_content[1] != "r" :
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

      if c_line_content[1] == "r" and line_count != 0:
        #print(c_line_content)

        # Break out of the with loop once a dataset is collected
        raise fragile.Break

      line_count += 1
  #print(line_count, line_buffer)
  line_buffer = line_count
  return [line_buffer, config, height_dictionary, color_dictionary]


def draw_rect_graph(config, height_dictionary, color_dictionary):
  """
    Draws the rectangle graph with the given hight and color values
  """
  dwg = svgwrite.Drawing(config["filename"] + '.svg', profile="full")
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



line_buffer = 0
capture = conf_graph(line_buffer)
line_buffer = capture[0]
draw_rect_graph(capture[1], capture[2], capture[3])
for i in range(line_buffer, line_count(csv_file), line_buffer):
  capture = conf_graph(line_buffer)
  line_buffer = capture[0]
  draw_rect_graph(capture[1], capture[2], capture[3])






