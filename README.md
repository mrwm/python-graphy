# python-graphy
Draws SVG graphs using python

***

Note: `graph.py` takes in a csv file that needs to be specifically formatted as such:

|-|A|B|C|D|E|F|G|H|
|1|Filename / color|mode [r|c]|<sup>1</sup>rectangle width / donut thickness|<sup>1</sup>offset|<sup>1</sup>line width|<sup>1</sup>dot size|<sup>1</sup>show rectangle / make donut|<sup>1</sup>show line|
|2|---|---|---|---|---|---|---|---|
|3|ExampleName|r|80|100|1|2.5|false|true|
|4|red|80|79|60|43|52|53|60|
|5|#ccc|72|80|84|84|82|81|83|

<sup>1</sup>Only applies to rectangle bar/line graphs

- The first line is kept as a legend
- To create a group, follow the legend in the first line.
- The first column (A) is for the file name for the group header, then color for the row data.
- (B) Used to set the graph mode: [r] rectangles / [r] line graph or [c] donut / [c] pie
- (C) is for the width of each rectangle or width of the donut graph
- (D) is for offsetting the bar graphs on the vertical axis
- (E) is used to set the thickness of the line graph
- (F) used for setting the line graph dots
- Then add the color, followed by the data that will be graphed in the same color


***
