#!/usr/bin/env python
'''
Add margin guides,
extension by Samuel Dellicour,

The extension adds document margin guides: guides at a certain distance from the borders of the document.

# Licence
Licence GPL v2
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''


# IMPORT


from lxml import etree
import inkex
import gettext
_ = gettext.gettext


# FUNCTIONS


# To show debugging output
def printDebug(string):
    inkex.debug(_(str(string)))

# To show error to user


def printError(string):
    inkex.errormsg(_(str(string)))

# Draw single guide
# parameters: position (single length), orientation ("horizontal/vertical"), parent


def drawGuide(position, orientation, parent):

    if orientation == "vertical":
        orientationString = "1,0"
        positionString = str(position) + ",0"

    if orientation == "horizontal":
        orientationString = "0,1"
        positionString = "0," + str(position)

    # Create a sodipodi:guide node
    etree.SubElement(parent, '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide', {
        'position': positionString, 'orientation': orientationString})


# CLASS


class addMarginGuides(inkex.Effect):

    def __init__(self):
        """
        Constructor.
        Defines options of the script.
        """
        # Call the base class constructor.
        inkex.Effect.__init__(self)

        # Define string option "--unit"
        self.arg_parser.add_argument('--unit',
                                     type=str,
                                     dest="unit", default="mm",
                                     help="The unit of the values")

        # Define boolean option "--same_margins"
        self.arg_parser.add_argument('--same_margins',
                                     type=inkex.Boolean,
                                     dest='same_margins', default=False,
                                     help='Same margins on all four sides')

        # Define string option "--top_margin"
        self.arg_parser.add_argument('--top_margin',
                                     type=str,
                                     dest='top_margin', default='centered',
                                     help='Top margin, distance from top border')

        # Define string option "--right_margin"
        self.arg_parser.add_argument('--right_margin',
                                     type=str,
                                     dest='right_margin', default='centered',
                                     help='Right margin, distance from right border')

        # Define string option "--bottom_margin"
        self.arg_parser.add_argument('--bottom_margin',
                                     type=str,
                                     dest='bottom_margin', default='centered',
                                     help='Bottom margin, distance from bottom border')

        # Define string option "--left_margin"
        self.arg_parser.add_argument('--left_margin',
                                     type=str,
                                     dest='left_margin', default='centered',
                                     help='Left margin, distance from left border')

    def effect(self):

        # Get script's options values. Input.

        # Factor to multiply in order to get user units (pixels)
        factor = self.svg.unittouu('1' + self.options.unit)

        # boolean
        same_margins = self.options.same_margins

        # convert string to integer, in user units (pixels)
        top_margin = float(self.options.top_margin) * factor
        right_margin = float(self.options.right_margin) * factor
        bottom_margin = float(self.options.bottom_margin) * factor
        left_margin = float(self.options.left_margin) * factor

        # getting parent tag of the guides
        namedview = self.document.xpath(
            '/svg:svg/sodipodi:namedview', namespaces=inkex.NSS)[0]

        # getting the main SVG document element (canvas)
        svg = self.document.getroot()

        # getting the width and height attributes of the canvas
        canvas_width = self.svg.unittouu(svg.get('width'))
        canvas_height = self.svg.unittouu(svg.get('height'))

        # Get selection bounding box - TODO

        # now let's use the input:

        # draw margin guides (if not zero)
        if same_margins:
            right_margin = top_margin
            bottom_margin = top_margin
            left_margin = top_margin

        # start position of guides
        top_pos = canvas_height - top_margin
        right_pos = canvas_width - right_margin
        bottom_pos = bottom_margin
        left_pos = left_margin

        # Draw the four margin guides (if margin exists)
        if top_pos != canvas_height:
            drawGuide(top_pos, "horizontal", namedview)
        if right_pos != canvas_width:
            drawGuide(right_pos, "vertical", namedview)
        if bottom_pos != 0:
            drawGuide(bottom_pos, "horizontal", namedview)
        if left_pos != 0:
            drawGuide(left_pos, "vertical", namedview)


# APPLY

# Create effect instance and apply it. Taking in SVG, changing it, and then outputing SVG
effect = addMarginGuides()
effect.run()
