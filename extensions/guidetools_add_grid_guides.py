#!/usr/bin/env python
'''
Add Grid Guides
by Samuel Dellicour

Adds a grid of guides - in columns with gutters (spacing between columns)

heavily based on Guides creator - Copyright (C) 2008 Jonas Termeau - jonas.termeau **AT** gmail.com


## This extension allows you to automatically draw column and row guides in inkscape (including gutters - spacing between columns).

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

import guidetools
import gettext
from simplestyle import *
import inkex
import sys
sys.path.append('/usr/share/inkscape/extensions')
_ = gettext.gettext


# CLASS

class Grid_Guides(inkex.Effect):

    def __init__(self):
        """
        Constructor.
        Defines options of the script.
        """
        # Call the base class constructor.
        inkex.Effect.__init__(self)

        # Parse options and store them in self.options.[destination]

        self.arg_parser.add_argument("--tab",
                                     type=str,
                                     dest="tab", default="columns",
                                     help="")

        # COLUMNS (vertical guides)

        self.arg_parser.add_argument('--column_unit',
                                     type=str,
                                     dest="column_unit", default="mm",
                                     help="The unit of the values")

        self.arg_parser.add_argument('--column_alignment',
                                     type=str,
                                     dest='column_alignment', default='centered',
                                     help='Alignment of the columns in relation to the document')

        self.arg_parser.add_argument('--column_offset',
                                     type=float,
                                     dest='column_offset', default=0,
                                     help='Offset distance from the left')

        self.arg_parser.add_argument('--columns',
                                     type=float,
                                     dest='columns', default=0,
                                     help='Number of columns')

        self.arg_parser.add_argument('--column_width',
                                     type=float,
                                     dest='column_width', default=0,
                                     help='Width of each column')

        self.arg_parser.add_argument('--column_gutter',
                                     type=float,
                                     dest='column_gutter', default=0,
                                     help='Spacing between columns')

        self.arg_parser.add_argument('--include_center_col_guides',
                                     type='inkbool',
                                     dest='include_center_col_guides', default=False,
                                     help='Include centered guides inside gutters)')

        self.arg_parser.add_argument('--include_outer_col_gutter',
                                     type=inkex.Boolean,
                                     dest='include_outer_col_gutter', default=True,
                                     help='Include outer gutters (double guides)')

        self.arg_parser.add_argument('--delete_vert_guides',
                                     type=inkex.Boolean,
                                     dest='delete_vert_guides', default=False,
                                     help='Delete existing vertical guides')

        # ROWS (horizontal guides)

        self.arg_parser.add_argument('--row_unit',
                                     type=str,
                                     dest="row_unit", default="mm",
                                     help="The unit of the values")

        self.arg_parser.add_argument('--row_alignment',
                                     type=str,
                                     dest='row_alignment', default='centered',
                                     help='Alignment of rows in relation to the document')

        self.arg_parser.add_argument('--row_offset',
                                     type=float,
                                     dest='row_offset', default=0,
                                     help='Offset distance from the top')

        self.arg_parser.add_argument('--rows',
                                     type=float,
                                     dest='rows', default=0,
                                     help='Number of rows')

        self.arg_parser.add_argument('--row_height',
                                     type=float,
                                     dest='row_height', default=0,
                                     help='Width of each row')

        self.arg_parser.add_argument('--row_gutter',
                                     type=float,
                                     dest='row_gutter', default=0,
                                     help='Spacing between rows')

        self.arg_parser.add_argument('--include_outer_row_gutter',
                                     type=inkex.Boolean,
                                     dest='include_outer_row_gutter', default=True,
                                     help='Include outer gutters (double guides)')

        self.arg_parser.add_argument('--include_center_row_guides',
                                     type=inkex.Boolean,
                                     dest='include_center_row_guides', default=True,
                                     help='Include centered guides inside gutters')

        self.arg_parser.add_argument('--delete_hor_guides',
                                     type=inkex.Boolean,
                                     dest='delete_hor_guides', default=False,
                                     help='Delete existing horizontal guides')

    def effect(self):

        # Get script's option values from self.options

        tab = self.options.tab

        # columns

        # Factor to multiply in order to get value in user units (pixels)
        col_factor = self.svg.unittouu('1' + self.options.column_unit)
        col_alignment = self.options.column_alignment
        col_offset = float(self.options.column_offset) * col_factor
        cols = int(self.options.columns)
        col_width = float(self.options.column_width) * col_factor
        col_gut = float(self.options.column_gutter) * col_factor
        has_outer_col_gutter = self.options.include_outer_col_gutter
        has_center_col_guides = self.options.include_center_col_guides
        delete_hor = self.options.delete_hor_guides

        # rows
        row_factor = self.svg.unittouu('1' + self.options.row_unit)
        row_alignment = self.options.row_alignment
        row_offset = float(self.options.row_offset) * row_factor
        rows = int(self.options.rows)
        row_height = float(self.options.row_height) * row_factor
        row_gut = float(self.options.row_gutter) * row_factor
        has_outer_row_gutter = self.options.include_outer_row_gutter
        has_center_row_guides = self.options.include_center_row_guides
        delete_vert = self.options.delete_vert_guides

        # parent tag of the guides
        namedview = self.document.xpath(
            '/svg:svg/sodipodi:namedview', namespaces=inkex.NSS)[0]

        # main SVG document element (canvas)
        svg = self.document.getroot()
        canvas_width = self.svg.unittouu(svg.get('width'))
        canvas_height = self.svg.unittouu(svg.attrib['height'])

        # total width  (columns and gutters)
        if has_outer_col_gutter:
            total_col_width = cols*col_width + (cols+1)*col_gut
        else:
            total_col_width = cols*col_width + (cols-1)*col_gut

        # total height (rows and gutters)
        if has_outer_row_gutter:
            total_row_height = rows*row_height + (rows+1)*row_gut
        else:
            total_row_height = rows*row_height + (rows-1)*row_gut

        if (tab == "\"columns\""):

            # Delete existing vertical guides
            if (delete_vert):
                guidetools.deleteGuidesByOrientation(self.document, 'vertical')

            # Set horizontal starting position, depending on grid alignment
            if (col_alignment == 'left'):
                hor_start = col_offset

            if (col_alignment == 'centered'):
                hor_start = round(canvas_width/2) - \
                    round(total_col_width/2) + col_offset

            if (col_alignment == 'right'):
                hor_start = canvas_width - total_col_width + col_offset

            # Create column guides with column_spacings
            guidetools.drawDoubleGuides(
                cols, col_width, col_gut, hor_start, has_outer_col_gutter, "vertical", namedview)

            # Center guides columns
            if (has_outer_col_gutter == True):
                center_cols = cols
                center_hor_start = hor_start + (col_gut/2)
            else:
                center_cols = cols - 2
                center_hor_start = hor_start + (col_gut/2) + col_width
            # Draw centered guides if necessary
            if col_gut > 0 and has_center_col_guides == True:
                guidetools.drawDoubleGuides(
                    center_cols, col_width + col_gut, 0, center_hor_start, has_outer_col_gutter, "vertical", namedview)

        elif (tab == "\"rows\""):

            # Delete existing horizontal guides
            if (delete_hor):
                guidetools.deleteGuidesByOrientation(
                    self.document, 'horizontal')

            # Set vertical starting position, depending on grid alignment
            # 0,0 is at BOTTOM left of document, guides will be drawn bottom up
            if (row_alignment == 'top'):
                vert_start = round(canvas_height) - \
                    total_row_height - row_offset

            if (row_alignment == 'centered'):
                vert_start = round(canvas_height/2) - \
                    round(total_row_height/2) - row_offset

            if (row_alignment == 'bottom'):
                vert_start = -row_offset

            # Create row guides
            guidetools.drawDoubleGuides(
                rows, row_height, row_gut, vert_start, has_outer_row_gutter, "horizontal", namedview)

            # Center guides rows
            if (has_outer_row_gutter == True):
                center_rows = rows
                center_vert_start = vert_start + (row_gut/2)
            else:
                center_rows = rows - 2
                center_vert_start = vert_start + (row_gut/2) + row_height
            # Draw centered guides if necessary
            if row_gut > 0 and has_center_row_guides == True:
                guidetools.drawDoubleGuides(center_rows, row_height + row_gut, 0,
                                            center_vert_start, has_outer_row_gutter, "horizontal", namedview)


# Create effect instance and apply it.
effect = Grid_Guides()
effect.run()
