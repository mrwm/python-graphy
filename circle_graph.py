#!/usr/bin/env python3

# circle_graph.py
# Author: William Chung
# Last Updated: 
# Purpose: Creates circle or donut graph with the given data points
# Program Uses: ./circle_graph.py
# Notes: 
#       - Requires svgwrite python module
#       - The resulting graph is upside down, make sure to vertically flip after
#
import math # for the trig functions
import svgwrite # for making the svg's

## Config

#
# (you can delete this line) The # below is for Head count in ch3.7
graph_numbers = [15177, 12922, 8111] # no need for totals
graph_colors = ["cyan", "#f9f06b", "#ff416c"]

line_stroke_width = "18"
file_name = "3.7-headcount.svg"

make_donut = True # False for full circle graph and True for donuts


################################################################################
###### Main part of the program
name="circle" # we need a name for the graph, tho it doesn't matter what it is
dwg = svgwrite.Drawing(filename=file_name, debug=True, size=(100,100))
current_group = dwg.add(dwg.g(id=name, stroke='red', stroke_width=3, fill='red', fill_opacity=1 ))

def addArc(dwg, current_group, p0, p1, radius, f_color):
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
  point=[x_point,y_point]
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

# This is kinda arbitrary, but we want a constant radius, so here it is.
circle_size = math.degrees(math.sin(math.radians(90)))

# Make a solid circle if we don't want a donut
if not make_donut:
  line_stroke_width = circle_size*2

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
  addArc(dwg, current_group, p0=anglept(end_angle), p1=anglept(start_angle), radius=circle_size, f_color=fill_color)

dwg.save()

