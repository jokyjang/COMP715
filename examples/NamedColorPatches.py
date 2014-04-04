#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
'''
=========================================================================
 
  Program:   Visualization Toolkit
  Module:    NamedColorPatches.py
 
  Copyright (c) Ken Martin, Will Schroeder, Bill Lorensen
  All rights reserved.
  See Copyright.txt or http://www.kitware.com/Copyright.htm for details.
 
     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notice for more information.
 
=========================================================================
 
Produce a HTML page called VTKNamedColorPatches.html showing the available
 colors in vtkNamedColors.
 
It also shows how to select the text color based on luminance.
In this case Digital CCIR601 is used which gives more weight to the
 red and blue components of a color.
 
We also create an auxiliary class called NamedColors, to facilitate the
interaction with the class vtkNamedColors.
 
'''
 
import vtk
 
class NamedColors(object):
 
    def __init__(self):
        '''
            Define a single instance of the NamedColors class here.
        '''
        self.namedColors = vtk.vtkNamedColors()
 
    def GetRGBColor(self, colorName):
        '''
            Return the red, green and blue components for a
            color as doubles.
        '''
        rgb = [0.0, 0.0, 0.0] # black
        self.namedColors.GetColorRGB(colorName, rgb)
        return rgb
 
    def GetRGBColorInt(self, colorName):
        '''
            Return the red, green and blue components for a
            color as integer.
        '''
        return self.GetRGBAColorInt(colorName)[:3]
 
    def GetRGBAColor(self, colorName):
        '''
            Return the red, green, blue and alpha
            components for a color as doubles.
        '''
        rgba = [0.0, 0.0, 0.0, 1.0] # black
        self.namedColors.GetColor(colorName, rgba)
        return rgba
 
    def GetRGBAColorInt(self, colorName):
        '''
            Return the red, green, blue and alpha
            components for a color as integer.
        '''
        rgba = [int(0), int(0), int(0), int(255)] # black
        self.namedColors.GetColor(colorName, rgba)
        return rgba
 
    def GetColorNames(self):
        '''
            Return a list of color names.
        '''
        colorsNames = self.namedColors.GetColorNames()
        colorsNames = colorsNames.split('\n')
        return colorsNames
 
    def RGBToHTMLColor(self, rgb):
        '''
            Convert an [R, G, B] list to #RRGGBB.
        '''
        hexcolor = '#%02x%02x%02x' % tuple(rgb)
        # '%02x' means zero-padded, 2-digit hex values
        return hexcolor
 
    def HTMLColorToRGB(self, colorString):
        '''
            Convert #RRGGBB to a [R, G, B] list.
        '''
        colorString = colorString.strip()
        if colorString[0] == '#': colorString = colorString[1:]
        if len(colorString) != 6:
            raise ValueError, "Input #%s is not in #RRGGBB format" % colorString
        r, g, b = colorString[:2], colorString[2:4], colorString[4:]
        r, g, b = [int(n, 16) for n in (r, g, b)]
        return [r, g, b]
 
    def RGBToLumaCCIR601(self, rgb):
        '''
            RGB -> Luma conversion
            Digital CCIR601 (gives more weight to the R and B components)
        '''
        Y = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
        return Y
 
 
    def GetSynonyms(self):
        '''
            Return a list of synonyms.
        '''
        syn = self.namedColors.GetSynonyms()
        syn = syn.split('\n\n')
        synonyms = []
        for ele in syn:
            synonyms.append(ele.split('\n'))
        return synonyms
 
    def FindSynonyms(self, colorName):
        '''
            Find any synonyms for a specified color.
        '''
        availableColors = self.GetColorNames()
        synonyms = []
        # We use lower case for comparison and 
        # just the red, green, and blue components
        # of the color.
        lcolorName = colorName.lower()
        myColor = self.GetRGBColorInt(colorName)
        for color in availableColors:
            rgb = self.GetRGBColorInt(color)
            if myColor == rgb:
                synonyms.append(color)
        return synonyms
 
 
class MakeColorPatches(object):
    def __init__(self):
        self.cn = {'Red':['IndianRed', 'LightCoral', 'Salmon', 'DarkSalmon', 'LightSalmon', 'Red', 'Crimson', 'FireBrick', 'DarkRed'],
            'Pink':['Pink', 'LightPink', 'HotPink', 'DeepPink', 'MediumVioletRed', 'PaleVioletRed'],
            'Orange':['LightSalmon', 'Coral', 'Tomato', 'OrangeRed', 'DarkOrange', 'Orange'],
            'Yellow':['Gold', 'Yellow', 'LightYellow', 'LemonChiffon', 'LightGoldenrodYellow', 'PapayaWhip', 'Moccasin', 'PeachPuff', 'PaleGoldenrod', 'Khaki', 'DarkKhaki'],
            'Purple':['Lavender', 'Thistle', 'Plum', 'Violet', 'Orchid', 'Fuchsia', 'Magenta', 'MediumOrchid', 'MediumPurple', 'BlueViolet', 'DarkViolet', 'DarkOrchid', 'DarkMagenta', 'Purple', 'Indigo', 'DarkSlateBlue', 'SlateBlue', 'MediumSlateBlue'],
            'Green':['GreenYellow', 'Chartreuse', 'LawnGreen', 'Lime', 'LimeGreen', 'PaleGreen', 'LightGreen', 'MediumSpringGreen', 'SpringGreen', 'MediumSeaGreen', 'SeaGreen', 'ForestGreen', 'Green', 'DarkGreen', 'YellowGreen', 'OliveDrab', 'Olive', 'DarkOliveGreen', 'MediumAquamarine', 'DarkSeaGreen', 'LightSeaGreen', 'DarkCyan', 'Teal'],
            'Blue/Cyan':['Aqua', 'Cyan', 'LightCyan', 'PaleTurquoise', 'Aquamarine', 'Turquoise', 'MediumTurquoise', 'DarkTurquoise', 'CadetBlue', 'SteelBlue', 'LightSteelBlue', 'PowderBlue', 'LightBlue', 'SkyBlue', 'LightSkyBlue', 'DeepSkyBlue', 'DodgerBlue', 'CornflowerBlue', 'RoyalBlue', 'Blue', 'MediumBlue', 'DarkBlue', 'Navy', 'MidnightBlue'],
            'Brown':['Cornsilk', 'BlanchedAlmond', 'Bisque', 'NavajoWhite', 'Wheat', 'BurlyWood', 'Tan', 'RosyBrown', 'SandyBrown', 'Goldenrod', 'DarkGoldenrod', 'Peru', 'Chocolate', 'SaddleBrown', 'Sienna', 'Brown', 'Maroon'],
            'White':['White', 'Snow', 'Honeydew', 'MintCream', 'Azure', 'AliceBlue', 'GhostWhite', 'WhiteSmoke', 'Seashell', 'Beige', 'OldLace', 'FloralWhite', 'Ivory', 'AntiqueWhite', 'Linen', 'LavenderBlush', 'MistyRose'],
            'Gray':['Gainsboro', 'LightGrey', 'Silver', 'DarkGray', 'Gray', 'DimGray', 'LightSlateGray', 'SlateGray', 'DarkSlateGray', 'Black']
            }
        # Ordering of the tables and when to start and end a column of tables in the layout.
        self.cnOrder = ['Red', 'Pink', 'Orange', 'Yellow', 'Purple', 'Green', 'Blue/Cyan', 'Brown', 'White', 'Gray']
        self.cnStartTable = ['Red', 'Green', 'Brown']
        self.cnEndTable = ['Purple', 'Blue/Cyan', 'Gray']
 
        self.vtkcn = {'Whites':['antique_white', 'azure', 'bisque', 'blanched_almond', 'cornsilk', 'eggshell', 'floral_white', 'gainsboro', 'ghost_white', 'honeydew', 'ivory', 'lavender', 'lavender_blush', 'lemon_chiffon', 'linen', 'mint_cream', 'misty_rose', 'moccasin', 'navajo_white', 'old_lace', 'papaya_whip', 'peach_puff', 'seashell', 'snow', 'thistle', 'titanium_white', 'wheat', 'white', 'white_smoke', 'zinc_white'],
            'Greys':['cold_grey', 'dim_grey', 'grey', 'light_grey', 'slate_grey', 'slate_grey_dark', 'slate_grey_light', 'warm_grey'],
            'Blacks':['black', 'ivory_black', 'lamp_black'],
            'Reds':['alizarin_crimson', 'brick', 'cadmium_red_deep', 'coral', 'coral_light', 'deep_pink', 'english_red', 'firebrick', 'geranium_lake', 'hot_pink', 'indian_red', 'light_salmon', 'madder_lake_deep', 'maroon', 'pink', 'pink_light', 'raspberry', 'red', 'rose_madder', 'salmon', 'tomato', 'venetian_red'],
            'Browns':['beige', 'brown', 'brown_madder', 'brown_ochre', 'burlywood', 'burnt_sienna', 'burnt_umber', 'chocolate', 'deep_ochre', 'flesh', 'flesh_ochre', 'gold_ochre', 'greenish_umber', 'khaki', 'khaki_dark', 'light_beige', 'peru', 'rosy_brown', 'raw_sienna', 'raw_umber', 'sepia', 'sienna', 'saddle_brown', 'sandy_brown', 'tan', 'van_dyke_brown'],
            'Oranges':['cadmium_orange', 'cadmium_red_light', 'carrot', 'dark_orange', 'mars_orange', 'mars_yellow', 'orange', 'orange_red', 'yellow_ochre'],
            'Yellows':['aureoline_yellow', 'banana', 'cadmium_lemon', 'cadmium_yellow', 'cadmium_yellow_light', 'gold', 'goldenrod', 'goldenrod_dark', 'goldenrod_light', 'goldenrod_pale', 'light_goldenrod', 'melon', 'naples_yellow_deep', 'yellow', 'yellow_light'],
            'Greens':['chartreuse', 'chrome_oxide_green', 'cinnabar_green', 'cobalt_green', 'emerald_green', 'forest_green', 'green', 'green_dark', 'green_pale', 'green_yellow', 'lawn_green', 'lime_green', 'mint', 'olive', 'olive_drab', 'olive_green_dark', 'permanent_green', 'sap_green', 'sea_green', 'sea_green_dark', 'sea_green_medium', 'sea_green_light', 'spring_green', 'spring_green_medium', 'terre_verte', 'viridian_light', 'yellow_green'],
            'Cyans':['aquamarine', 'aquamarine_medium', 'cyan', 'cyan_white', 'turquoise', 'turquoise_dark', 'turquoise_medium', 'turquoise_pale'],
            'Blues':['alice_blue', 'blue', 'blue_light', 'blue_medium', 'cadet', 'cobalt', 'cornflower', 'cerulean', 'dodger_blue', 'indigo', 'manganese_blue', 'midnight_blue', 'navy', 'peacock', 'powder_blue', 'royal_blue', 'slate_blue', 'slate_blue_dark', 'slate_blue_light', 'slate_blue_medium', 'sky_blue', 'sky_blue_deep', 'sky_blue_light', 'steel_blue', 'steel_blue_light', 'turquoise_blue', 'ultramarine'],
            'Magentas':['blue_violet', 'cobalt_violet_deep', 'magenta', 'orchid', 'orchid_dark', 'orchid_medium', 'permanent_red_violet', 'plum', 'purple', 'purple_medium', 'ultramarine_violet', 'violet', 'violet_dark', 'violet_red', 'violet_red_medium', 'violet_red_pale']
            }
        # Ordering of the tables and when to start and end a column of tables in the layout.
        self.vtkcnOrder = ['Whites', 'Greys', 'Blacks', 'Reds', 'Oranges', 'Browns', 'Yellows', 'Greens', 'Cyans', 'Blues', 'Magentas']
        self.vtkcnStartTable = ['Whites', 'Browns', 'Cyans']
        self.vtkcnEndTable = ['Oranges', 'Greens', 'Magentas']
 
    def MakeHTMLHeader(self):
        s = '<!DOCTYPE html>\n'
        s += '<html lang="en" dir="ltr" class="client-nojs">\n'
        s += '<head>\n'
        s += '<title>vtkNamedColors</title>\n'
        s += '<meta charset="UTF-8" />\n'
        s += '</head>\n'
        return s
 
    def MakeTableHeader(self):
        s = '<tr>\n'
        s += '<th style="background:lightgrey">HTML name</th>\n'
        s += '<th style="background:lightgrey">Decimal code<br />\n'
        s += 'R &#160; G &#160; B</th>\n'
        s += '</tr>\n'
        return s
 
    def MakeTD(self, name):
        s = '<tr>\n'
        s += '<td colspan="2" style="background:whitesmoke;color:slategray;text-align:left"><big><b>' + name + '</b></big></td>\n'
        s += '</tr>\n'
        return s
 
    def MakeTR(self, name, rgb, textColor):
        s = '<tr>\n'
        s += '<td style="background:' + name + ';color:' + textColor + '">' + name + '</td>\n'
        s += '<td style="background:' + name + ';color:' + textColor + '"><tt>' + str(rgb[0]) + '&#160;&#160;' + str(rgb[1]) + '&#160;&#160;' + str(rgb[2]) + '</tt></td>\n'
        s += '</tr>\n'
        return s
 
    def MakeVTKTR(self, name, nameColor, rgb, textColor):
        s = '<tr>\n'
        s += '<td style="background:' + nameColor + ';color:' + textColor + '">' + name + '</td>\n'
        s += '<td style="background:' + nameColor + ';color:' + textColor + '"><tt>' + str(rgb[0]) + '&#160;&#160;' + str(rgb[1]) + '&#160;&#160;' + str(rgb[2]) + '</tt></td>\n'
        s += '</tr>\n'
        return s
 
    def FindLongestColorName(self):
        ''' Find the longest color name. '''
        maxLength = -1;
        for key, value in self.cn.iteritems():
            for val in value:
                if len(val) > maxLength:
                    maxLength = len(val)
        for key, value in self.vtkcn.iteritems():
            for val in value:
                if len(val) > maxLength:
                    maxLength = len(val)
        return maxLength
 
    def MakeWebColorTables(self):
        colors = NamedColors()
        res = ''
        for key in self.cnOrder:
            if key in self.cnStartTable:
                res += '<td>\n'
                res += '<table>\n'
                res += self.MakeTableHeader()
            res += self.MakeTD(key + ' colors')
            values = self.cn[key]
            for name in values:
                rgb = colors.GetRGBColorInt(name)
                Y = colors.RGBToLumaCCIR601(rgb)
                textColor = '#000000' # Black
                if Y < 255 / 2.0:
                    textColor = '#ffffff' # White
                res += self.MakeTR(name, rgb, textColor)
            if key in self.cnEndTable:
                res += '</table>\n'
                res += '</td>\n'
        return res
 
    def MakeVTKColorTables(self):
        colors = NamedColors()
        res = ''
        for key in self.vtkcnOrder:
            if key in self.vtkcnStartTable:
                res += '<td>\n'
                res += '<table>\n'
                res += self.MakeTableHeader()
            res += self.MakeTD(key)
            values = self.vtkcn[key]
            for name in values:
                rgb = colors.GetRGBColorInt(name)
                Y = colors.RGBToLumaCCIR601(rgb)
                textColor = '#000000' # Black
                if Y < 255 / 2.0:
                    textColor = '#ffffff' # White
                nameColor = colors.RGBToHTMLColor(rgb)
                res += self.MakeVTKTR(name, nameColor, rgb, textColor)
            if key in self.vtkcnEndTable:
                res += '</table>\n'
                res += '</td>\n'
        return res
 
    def MakeSynonymColorTable(self):
        colors = NamedColors()
        synonyms = colors.GetSynonyms()
        cn = list()
        for key, value in self.cn.iteritems():
           cn = cn + value
        # Create a dictionary where the key is the lowercase name.
        d = dict()
        for n in cn:
            d.update({n.lower():n})
        res = '<td>\n'
        res += '<table>\n'
        for colorNames in colors.GetSynonyms():
            for idx, name in enumerate(colorNames):
                if name in d:
                    colorNames[idx] = d[name]
            colorNames.sort()
            name = ", ".join(colorNames)
            rgb = colors.GetRGBColorInt(colorNames[0])
            Y = colors.RGBToLumaCCIR601(rgb)
            textColor = '#000000' # Black
            if Y < 255 / 2.0:
                textColor = '#ffffff' # White
            nameColor = colors.RGBToHTMLColor(rgb)
            res += self.MakeVTKTR(name, nameColor, rgb, textColor)
        res += '</table>\n'
        res += '</td>\n'
        return res
 
    def MakeWebColorPage(self):
        res = self.MakeHTMLHeader()
        res += '<body>\n'
        res += '<h1>Colors available in vtkNamedColors</h1>\n'
        res += '<table style="font-size:90%" cellpadding="4">\n'
        res += '<caption style="background:lightgrey">Web Color Names</caption>\n'
        res += '<tr valign="top">\n'
        res += self.MakeColorTables()
        res += '</table>\n'
        res += '</body>\n'
        return res
 
    def MakeVTKColorPage(self):
        res = self.MakeHTMLHeader()
        res += '<body>\n'
        res += '<h1>Colors available in vtkNamedColors</h1>\n'
        res += '<p>The web colors take precedence over colors of the same name in VTK Color Names.</p>\n'
        res += '<table style="font-size:90%" cellpadding="4">\n'
        res += '<caption style="background:lightgrey">VTK Color Names</caption>\n'
        res += '<tr valign="top">\n'
        res += self.MakeVTKColorTables()
        res += '</table>\n'
        res += '</body>\n'
        return res
 
    def MakeSynonymColorPage(self):
        res = self.MakeHTMLHeader()
        res += '<body>\n'
        res += '<h1>Synonyms in vtkNamedColors</h1>\n'
        res += '<table style="font-size:90%" cellpadding="4">\n'
        res += '<caption style="background:lightgrey">Synonyms</caption>\n'
        res += '<tr valign="top">\n'
        res += self.MakeSynonymColorTable()
        res += '</table>\n'
        res += '</body>\n'
        return res
 
    def MakeCombinedColorPage(self):
        res = self.MakeHTMLHeader()
        res += '<body>\n'
        res += '<h1>Colors available in vtkNamedColors</h1>\n'
        res += '<p>The class vtkNamesColors provides color names and their values for the convenience of the user.</p>\n'
        res += '<p>The following tables show the available colors along with their red, green and blue values.</p>\n'
        res += '<h2>Web color Names</h2>'
        res += 'These colors correspond to those in <a href="http://en.wikipedia.org/wiki/Web_colors" title="Web Colors">Web Colors</a>.\n'
        res += '<table style="font-size:90%" cellpadding="4">\n'
        res += '<caption style="background:lightgrey">Web Color Names</caption>\n'
        res += '<tr valign="top">\n'
        res += self.MakeWebColorTables()
        res += '</table>\n'
        res += '<h2>VTK color Names</h2>'
        res += '<p>The colors mainly correspond to those in vtkColors.txt.\n</p>\n'
        res += '<p>The web colors (above) take precedence over colors of the same name in vtkColors.txt.</p>\n'
        res += '<table style="font-size:90%" cellpadding="4">\n'
        res += '<caption style="background:lightgrey">VTK Color Names</caption>\n'
        res += '<tr valign="top">\n'
        res += self.MakeVTKColorTables()
        res += '</table>\n'
        res += '<h2>Synonyms</h2>'
        res += '<table style="font-size:90%" cellpadding="4">\n'
        res += '<caption style="background:lightgrey">Synonyms</caption>\n'
        res += '<tr valign="top">\n'
        res += self.MakeSynonymColorTable()
        res += '</table>\n'
        res += '</body>\n'
        return res
 
if __name__ == "__main__":
     cp = MakeColorPatches()
     res = cp.MakeCombinedColorPage()
     f = open("VTKNamedColorPatches.html", "wb")
     f.write(res)