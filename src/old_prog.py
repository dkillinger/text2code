import argparse
from datetime import datetime as dt
import random
import sys
import os
import re

'''
******************************************************************
Regular_Expressions class is the class that stores all regular
expressions throughout every process of ren_form.py. By default,
the Regular_Expressions contains no regular expression, but
using the init methods will initiate specific regular expressions 
to use.
'''
class Regular_Expressions:
    def __init__(self, new_set = '') -> None:
        if new_set == '':
            self.char_set = r'[A-Z0-9\s_-]+?' #r'[^a-z`~!@#$%^&*\[{\]};:\'\",<\.>/?\(\)\-=+\\|]+?'
        else:
            self.char_set = '['+new_set+']'
    
    def init_script(self) -> None:
        self.script_beg = re.compile(r'^\s*\/\/\/\s*SCRIPT\s+BEG\s*\\\\\\\s*$')
        self.script_end = re.compile(r'^\s*\\\\\\\s*SCRIPT\s+END\s*\/\/\/\s*$')
        self.empty_line = re.compile(r'^\s*$')
        self.cmmnt_line = re.compile(r'^\s*#.+$')
        
    def init_characters(self) -> None:
        self.chrct_name = re.compile(r'^\s*\s*((?:[A-Z0-9\s_-]{2,5}\.)?\s*'+self.char_set+r')(?:\s+\(\s*(O.S.|V.O.)\s*\))?\s*$')
        self.chrct_prnth = re.compile(r'^\s*\((\w+)\)\s*$')
    
    def init_headers(self) -> None:
        header_start = r'INT\.|EXT\.|LOC\.|IMG\.'
        self.scene_trans = re.compile(r'^\s*('+self.char_set+r')\s+TO:\s*$')
        self.scene_headr = re.compile(r'^\s*('+header_start+r')\s+('+self.char_set+r')(?:\s+(-|,)\s+('+self.char_set+r'))?\s*$')
    
    def init_directions(self) -> None:
        self.chng_drct = re.compile(r'\s*\[\s*('+self.char_set+r')\s+(?:\:|IS|GETS|GROWS|GOES|TURNS|BECOMES)\s+('+self.char_set+r')\s*\]\s*')
        self.appr_drct = re.compile(r'\s*\[\s*(ENTER|EXIT)\s+('+self.char_set+r')\s*\]\s*')
        
    def init_render_styles(self) -> None:
        self.rendr_style = re.compile(r'^\s*<\s*(?:(SNAP|IDLE|CMMN|COMMON)\s*)?(BUBL|AVL|NVL|BUBBLE|AVL-MODE|NVL-MODE)?(?:\s*(SNAP|IDLE|CMMN|COMMON))?\s*>\s*$')
        # self.rendr_style = re.compile(r'^\s*<\s*('+self.char_set+r')\s*>\s*$')
        self.reset_rendr = re.compile(r'^\s*<\s*(?:RESET)?\s*>\s*$')
        
    def init_text_styles(self) -> None:
        self.text_style = re.compile(r'^\s*{\s*((?:\s*[A-Z]+(?:\s*=\s*[\w\d\.#]+?)?\s*,\s*)*?(?:\s*[A-Z]+(?:\s*=\s*[\w\d\.#]+?)?))\s*}\s*$')
        self.reset_text = re.compile(r'^\s*{\s*(?:RESET)?\s*}\s*$')
        
    def init_audio(self) -> None:
        self.sound_stmt = re.compile(r'^\s*\*\s*(?:(?:S|SOUND)\s*\:\s*)?('+self.char_set+r')\s*(!)?\s*\*\s*$')
        self.music_stmt = re.compile(r'^\s*\*\s*(?:(?:M|MUSIC)\s*\:)\s*('+self.char_set+r')\s*\?\s*$')
        self.voice_stmt = re.compile(r'^\s*\*\s*(?:(?:V|VOICE)\s*\:)\s*('+self.char_set+r')\s*\*\s*$')
        self.audio_stmt = re.compile(r'^\s*\*\s*('+self.char_set+r')\s*\:\s*('+self.char_set+r')\s*\*\s*$')
    
    def init_all(self) -> None:
        self.init_script()
        self.init_render_styles()
        self.init_characters()
        self.init_headers()
        self.init_directions()
        self.init_text_styles()
        self.init_audio()
        
    def init_quality_assurance(self) -> None:
        self.unknw_extn = re.compile(r'^\s*'+self.char_set+r'\s+\(\s*(.+)\s*\)\s*$')
        self.unkwn_drct = re.compile(r'^\s*(\[\s*'+self.char_set+r'\s*\])\s*$')
        self.unkwn_rendr = re.compile(r'^\s*(<\s*'+self.char_set+r'\s*>)\s*$')
        
        self.potnt_headr = re.compile(r'^\s*([A-Z]+\.\s+[A-Z-\s]+?)\s*$')
        self.potnt_drct = re.compile(r'^\s*(\[\s*.+?\s*\])\s*$')
        self.potnt_rendr = re.compile(r'^\s*(<\s*.+\s*>)\s*$')
        self.potnt_text = re.compile(r'^\s*({.+})\s*$')

'''
******************************************************************
Scene_Handler is a class which handles scene transitions by
determining capturing scene transitions properly, and by storing
information for use in Run_Manager.
'''
class Scene_Handler:
    def __init__(self) -> None:
        self.is_atl = False
        self.last_headr: str = ''
        self.curr_trnstn: str = ''
    
    def is_predefined(self, transition: str) -> bool:
        transition = transition.strip()
        predefined_transitions = \
            ['CUT',
             'FADE', 
             'DISSOLVE', 
             'PIXELATE', 
             'MOVE', 
             'MOVEINRIGHT', 
             'MOVEINLEFT', 
             'MOVEINTOP', 
             'MOVEINBOTTOM', 
             'MOVEOUTRIGHT', 
             'MOVEOUTLEFT', 
             'MOVEOUTTOP', 
             'MOVEOUTBOTTOM', 
             'EASE', 
             'EASEINRIGHT', 
             'EASEINLEFT', 
             'EASEINTOP', 
             'EASEINBOTTOM', 
             'EASEOUTRIGHT', 
             'EASEOUTLEFT', 
             'EASEOUTTOP', 
             'EASEOUTBOTTOM', 
             'ZOOMIN', 
             'ZOOMOUT', 
             'ZOOMINOUT', 
             'VPUNCH', 
             'HPUNCH', 
             'BLINDS', 
             'SQUARES', 
             'WIPELEFT', 
             'WIPERIGHT', 
             'WIPEUP', 
             'WIPEDOWN', 
             'SLIDELEFT', 
             'SLIDERIGHT', 
             'SLIDEUP', 
             'SLIDEDOWN', 
             'SLIDEAWAYLEFT', 
             'SLIDEAWAYRIGHT', 
             'SLIDEAWAYUP', 
             'SLIDEAWAYDOWN', 
             'PUSHRIGHT', 
             'PUSHLEFT', 
             'PUSHUP', 
             'PUSHDOWN', 
             'IRISIN', 
             'IRISOUT']
        if transition in predefined_transitions:
            return True
        else:
            return False
        
    def format_predefined(self, transition: str) -> str:
        format_trnstn: str = ''
        if transition == 'cut':
            format_trnstn = ''
        else:
            format_trnstn = 'with '+transition
        return format_trnstn
    
    def format_atl(self, transition: str, old_widget: str, new_widget: str) -> str:
        return 'at '+transition+'(old_widget=\''+('bg '+old_widget).rstrip()+'.webp\', new_widget=\''+('bg '+new_widget).rstrip()+'.webp\', sec=1.0)'
    
    def format_header(self, image_name: str, transition: str) -> str:
        return ('scene '+image_name+' '+transition).rstrip()+'\n'

'''
******************************************************************
Tag_Attributes is a class which automatically generates the start 
and end formats for a Ren'Py text tag. If the tag originally has 
no value, the value can be generated later using the create_value 
method.
'''
class Tag_Attributes:
    def create_value(self, value: str) -> None:
        self.tag_start = self.tag_start+value+'}'
    
    def __init__(self, tag: str, needs_value: bool = False, value: str = None, self_closing: bool = False) -> None:
        self.tag_start = '{'+tag
        self.needs_value = needs_value
        self.no_value = True if value is None else False
        if needs_value:
            self.tag_start = self.tag_start+'='
            if value:
                self.tag_start = self.tag_start+value+'}'
        else:
            self.tag_start = self.tag_start+'}'
        self.tag_end = '{/'+tag+'}'
        if self_closing:
            self.tag_end = None
            
class TS_Keywords:
    upper_case: str = 'UPPER' # ADDED
    lower_case: str = 'LOWER' # ADDED
    swap_case: str = 'SWAP' # ADDED
    random_case: str = 'RANDOM' # ADDED
    # wave_case: str = 'WAVE'
    count_cond: str = 'COUNT' # ADDED

'''
******************************************************************
Text_Style_Handler is a class which handles how some/all 
narration/dialogue lines text is presented. Namely, what text tags 
are applied to the text which can be found at:
https://www.renpy.org/doc/html/text.html#styling-and-text-tags
This class also adds the ability to alter the case of text, and
the user can control how many lines of text are styled by using
the condition keywords found in conds_dict.
'''
class Text_Style_Handler:
    def __init__(self) -> None:
        self.is_active: bool = False
        self.curr_case: str = None
        self.curr_cond: str = TS_Keywords.count_cond
        self.line_count: int = 1
        self.tag_prefix: str = ''
        self.tag_suffix: str = ''
        self.cases_dict = \
            {'UP': TS_Keywords.upper_case,
             'LOW': TS_Keywords.lower_case,
             TS_Keywords.upper_case: TS_Keywords.upper_case,
             TS_Keywords.lower_case: TS_Keywords.lower_case,
             TS_Keywords.random_case: TS_Keywords.random_case,
             TS_Keywords.swap_case: TS_Keywords.swap_case,
             'UPPERCASE': TS_Keywords.upper_case,
             'LOWERCASE': TS_Keywords.lower_case,
             'RANDOMCASE': TS_Keywords.random_case,
             'SWAPCASE': TS_Keywords.swap_case}
        self.conds_dict = \
            {# Condition flags
             'SPEAK': 'SPEAK',
             'NARRATE': 'NARRATE',
             'WHILESPEAKING': 'SPEAK',
             'WHILENARRATING': 'NARRATE',
             # Line counts
             TS_Keywords.count_cond: TS_Keywords.count_cond,
             'LINECOUNT':TS_Keywords.count_cond,
             'INF': 'INF',
             'INFINITY': 'INF',
             'FOREVER': 'INF'}
        self.tags_dict = \
            {# Predefined text tags
             '': Tag_Attributes('', True, self_closing=True), # Style Text Tags
             'A': Tag_Attributes('a', True),
             'ANCHOR': Tag_Attributes('a', True),
             'ALPHA': Tag_Attributes('alpha', True),
             'ALT': Tag_Attributes('alt'),
             'B': Tag_Attributes('b'),
             'BOLD': Tag_Attributes('b'),
             'COLOR': Tag_Attributes('color', True),
             'CPS': Tag_Attributes('cps', True),
             'FONT': Tag_Attributes('font', True),
             'I': Tag_Attributes('i'),
             'ITALICS': Tag_Attributes('i'),
             'K': Tag_Attributes('k', True),
             'KERNING': Tag_Attributes('k', True),
             'NOALT': Tag_Attributes('noalt'),
             'OUTLINECOLOR': Tag_Attributes('outlinecolor', True),
             'PLAIN': Tag_Attributes('plain'),
             'S': Tag_Attributes('s'),
             'STRIKETHROUGH': Tag_Attributes('s'),
             'SIZE': Tag_Attributes('size', True),
             'U': Tag_Attributes('u'),
             'UNDERLINED': Tag_Attributes('u'),
             # Pre-defined alpha tags
             'TRANSLUCENT': Tag_Attributes('alpha', True, '*0.75'),
             'TRANSPARENT': Tag_Attributes('alpha', True, '*0.5'),
             'LIMPID': Tag_Attributes('alpha', True, '*0.1'),
             # Pre-defined cps tags
             'QUICK': Tag_Attributes('cps', True, '*4'),
             'SWIFT': Tag_Attributes('cps', True, '*2'),
             'STEADY': Tag_Attributes('cps', True, '*0.5'),
             'SLOW': Tag_Attributes('cps', True, '*0.25'),
             'CRAWL': Tag_Attributes('cps', True, '*0.1'),
             # Pre-defined size tags
             'HUGE': Tag_Attributes('size', True, '*4'),
             'BIG': Tag_Attributes('size', True, '*2'),
             'SMALL': Tag_Attributes('size', True, '*0.5'),
             'TINY': Tag_Attributes('size', True, '*0.25'),
             # Pre-defined color tags
             'WHITE': Tag_Attributes('color', True, '#FFFFFF'),
             'BLACK': Tag_Attributes('color', True, '#000000'),
             'GREY': Tag_Attributes('color', True, '#888888'),
             'RED': Tag_Attributes('color', True, '#FF0000'),
             'ORANGE': Tag_Attributes('color', True, '#FF7700'),
             'YELLOW': Tag_Attributes('color', True, '#FFFF00'),
             'LIME': Tag_Attributes('color', True, '#77FF00'),
             'GREEN': Tag_Attributes('color', True, '#00FF00'),
             'TURQUOISE': Tag_Attributes('color', True, '#00FF77'),
             'CYAN': Tag_Attributes('color', True, '#00FFFF'),
             'AZURE': Tag_Attributes('color', True, '#0077FF'),
             'BLUE': Tag_Attributes('color', True, '#0000FF'),
             'VIOLET': Tag_Attributes('color', True, '#7700FF'),
             'MAGENTA': Tag_Attributes('color', True, '#FF00FF'),
             'ROSE': Tag_Attributes('color', True, '#FF0077')}
        
    def reset_all(self) -> None:
        self.is_active: bool = False
        self.curr_case: str = None
        self.curr_cond: str = TS_Keywords.count_cond
        self.line_count: int = 1
        self.tag_prefix: str = ''
        self.tag_suffix: str = ''
    
    def print_all(self) -> None:
        print(' Text_Style_Handler Report:')
        print('   is_active = '+str(self.is_active))
        print('   curr_case = \''+str(self.curr_case)+'\'')
        print('   curr_cond = \''+str(self.curr_cond)+'\'')
        print('   line_count = \''+str(self.line_count)+'\'')
        print('   tag_prefix = \''+str(self.tag_prefix)+'\'')
        print('   tag_suffix = \''+str(self.tag_suffix)+'\'')
    
    def randomize_case(self, line: str) -> str:
        rtrn_str = ''
        swap_prev = False
        space_prev = False
        for char in line:
            if char.isalpha():
                if space_prev:
                    char = char.lower()
                    space_prev = False
                elif swap_prev:
                    swap_prev = False
                else:
                    should_swap = random.choice([True, True, False])
                    if should_swap:
                        char = char.swapcase()
                        swap_prev = True
            elif char.isspace():
                space_prev = True
            rtrn_str = rtrn_str + char
        return rtrn_str
    
    def apply_case(self, line: str) -> str:
        if self.curr_case == TS_Keywords.lower_case:
            line = line.lower()
        elif self.curr_case == TS_Keywords.upper_case:
            line = line.upper()
        elif self.curr_case == TS_Keywords.random_case:
            line = self.randomize_case(line)
        elif self.curr_case == TS_Keywords.swap_case:
            line = line.swapcase()
        return line
    
    def is_cond(self, cond: str) -> str:
        if cond in self.conds_dict: return self.conds_dict[cond]
        else: return None
    
    def is_case(self, case: str) -> str:
        if case in self.cases_dict: return self.cases_dict[case]
        else: return None
        
    def is_tag(self, tag: str) -> Tag_Attributes:
        if tag in self.tags_dict: return self.tags_dict[tag]
        else: return None
        
    def set_attributes(self, attributes: list[str]) -> None:
        attr_name: str = ''
        attr_value: str = ''
        for attr in attributes:
            if attr.find('=') != -1:
                attr_split = attr.split('=', 1)
                attr_name = attr_split[0]
                attr_value = attr_split[1].lower()
            else:
                attr_name = attr
            if curr_cond := self.is_cond(attr_name):
                self.curr_cond = curr_cond
                if curr_cond == TS_Keywords.count_cond and attr_value != '':
                    self.line_count = int(attr_value) if int(attr_value) > 0 else 1
                else:
                    self.line_count = -1
            elif curr_case := self.is_case(attr_name):
                self.curr_case = curr_case
            elif curr_tag := self.is_tag(attr_name):
                if curr_tag.no_value and curr_tag.needs_value:
                    curr_tag.create_value(attr_value)
                self.tag_prefix = self.tag_prefix + curr_tag.tag_start
                if curr_tag.tag_end:
                    self.tag_suffix = self.tag_suffix + curr_tag.tag_end
            else:
                new_tag = Tag_Attributes(attr_name.lower(), True if attr_value != '' else False, attr_value)
                self.tag_prefix = self.tag_prefix + new_tag.tag_start
                self.tag_suffix = self.tag_suffix + new_tag.tag_end
    
    def split_styles(self, styles) -> list[str]:
        style_list = styles.split(',')
        for i in range(0,len(style_list)):
            style_list[i] = style_list[i].replace(' ', '')
        return style_list
            
    def get_text_styles(self, stmt: str) -> None:
        style_list = self.split_styles(stmt)
        self.set_attributes(style_list)

'''
******************************************************************
Render_Style_Handler is a class which handles the render style in 
which segments of the read file will be written into the resulting 
.rpy file. By "render style" I mean two things:
    - How dialogue/speech is rendered (AVL/NVL/Speech Bubbles)
    - How sprites, backgrounds, and snap images are handled
'''
class Render_Style_Handler:
    # ALL Style Statements are surrounded by <> and contain set 
    # keywords in the following format:
    #                  <IMAGE_TYPE DIALOGUE_TYPE>
    # Where IMAGE_TYPE is one of the following:
    #   - SNAP
    #   - IDLE
    #   - COMMON\CMMN
    #   - Or Nothing At All :)
    # And where DIALOGUE_TYPE is one of the following:
    #   - BUBL/BUBBLE
    #   - AVL/AVL-MODE
    #   - NVL/NVL-MODE
    #   - Or Nothing At All :)
    # THIS IS CASE-SENSITIVE; ALL BLOCKS MUST CONTAIN ALL CAPS,
    # AND THE LINE MUST ONLY CONTAIN ONE OF EACH STYLE STATEMENT
    # AT A MAXIMUM
    def __init__(self) -> None:
        self.in_snap: bool = False
        self.in_idle: bool = False
        self.in_bubl: bool = False
        self.in_nvl: bool = False
    
    def set_image_style(self, style: str) -> list[bool]:
        is_idle = is_snap = False
        if style == 'IDLE':
            is_idle = True
        elif style == 'SNAP':
            is_snap = True
        return is_idle, is_snap
    
    def set_speech_style(self, style: str) -> list[bool]:
        is_bubl = is_nvl = False
        bubl_keywords: list[str] = ['BUBL', 'BUBBLE']
        nvl_keywords: list[str] = ['NVL', 'NVL-MODE']
        if style in bubl_keywords:
            is_bubl = True
        elif style in nvl_keywords:
            is_nvl = True
        return is_bubl, is_nvl
    
    def redefine_narrator(self, kind: str = '') -> str:
        narrator_obj = '$ narrator = Character(name=None'
        if kind == 'BUBBLE':
            narrator_obj = narrator_obj + ',kind=bubble'
        elif kind == 'NVL':
            narrator_obj = narrator_obj + ',kind=nvl'
        narrator_obj = narrator_obj + ')\n'
        return narrator_obj
    
    def format_image_name(self, label: str, image_num: int = 0) -> str:
        image_name = 'img '+label+'_num'+str(image_num)
        return image_name

'''
******************************************************************
Character_Attributes is a class which stores information about
a character in a script. Not only is it used as a helper class 
for Character_Object_Handler, but it is also used to write the 
resulting report file created by Run_Reporter.
'''
class Character_Attributes:
    def __init__(self) -> None:
        self.is_onscreen: bool = False
        self.last_prnth: str = ''
        self.lines_spoken: int = 0
        self.sprites_used: list[str] = []
  
'''
******************************************************************
Character_Object_Handler is a class which handles all things pertaining
to the Character Objects needed for writing dialogue. It achieves
this by recording lines that match the following format:
    * Character name DOES NOT contain any:
        - lowercase letters
        - punctuation
        - special characters
    * Line OPTIONALLY ends with text enveloped in parentheses
      (This is know as a CHARACTER EXTENSION)
'''
class Character_Object_Handler:
    # ALL Character names are ALL CAPS, no punctuation, and no 
    # special characters. UNLESS there is a (V.O.) or (O.S.) at the end

    def obj_names_helper(self, chrct_names: list[str], prefix = '') -> dict:
        var_name = re.compile(r'^([^a-z])[AEIOU]*([^AEIOU])')
        is_num = re.compile(r'^[0-9]{2}')
        char_obj_names = {} # final character object names
        used_obj_names = [] # list to keep track what's been added
                            # to char_obj_names
        
        for char in chrct_names:
            obj_name: str = ''
            if char_match := var_name.match(char):
                obj_name = (prefix+char_match.group(1)+char_match.group(2)).lower()
            else:
                obj_name = (prefix+char[0]+char[0]).lower()
            if char_match := is_num.match(obj_name):
                obj_name = 'c'+obj_name
            if obj_name in used_obj_names:
                num_suffix = 0
                while obj_name in used_obj_names:
                    num_suffix += 1
                    if obj_name + str(num_suffix) not in used_obj_names:
                        used_obj_names.append(obj_name+str(num_suffix))
                        char_obj_names[char] = obj_name+str(num_suffix)
                        break
            else:
                used_obj_names.append(obj_name)
                char_obj_names[char] = obj_name
        
        return char_obj_names
    
    def create_chrct_obj_names(self) -> None:
        self.avl_objs = self.obj_names_helper(self.avl_chrctrs)
        self.bubl_objs = self.obj_names_helper(self.bubl_chrctrs, prefix='bubl_')
        self.nvl_objs = self.obj_names_helper(self.nvl_chrctrs, prefix='nvl_')
    
    def create_chrct_objs(self, chrct_name: str, obj_names: dict, kind = 'AVL') -> str:
        char_obj: str = '$ ' + obj_names[chrct_name] + ' = Character(name=\''+chrct_name.title()+'\''
        if kind == 'BUBBLE':
            char_obj = char_obj + ',kind=bubble'
        if kind == 'NVL':
            char_obj = char_obj + ',kind=nvl'
        char_obj = char_obj + ')\n'
        return char_obj
    
    def chrct_overseers_helper(self, chrctr_names: list[str]) -> dict[Character_Attributes]:
        overseer_dict = {}
        for chrctr in chrctr_names:
            overseer_dict[chrctr] = Character_Attributes()
        return overseer_dict
    
    def create_chrct_overseers(self) -> None:
        self.avl_ovrs = self.chrct_overseers_helper(self.avl_chrctrs)
        self.bubl_ovrs = self.chrct_overseers_helper(self.bubl_chrctrs)
        self.nvl_ovrs = self.chrct_overseers_helper(self.nvl_chrctrs)
        
    def create_all(self):
        self.create_chrct_obj_names()
        self.create_chrct_overseers()
        
    def reset_onscreen(self) -> None:
        for chrctr in self.bubl_chrctrs:
            self.bubl_ovrs[chrctr].is_onscreen = False
        for chrctr in self.nvl_chrctrs:
            self.nvl_ovrs[chrctr].is_onscreen = False
        for chrctr in self.avl_chrctrs:
            self.avl_ovrs[chrctr].is_onscreen = False
        
    def format_show_chrctr(self, curr_chrct: str, curr_prnth: str = '') -> str:
        show_str: str = 'show '+curr_chrct.lower()
        if curr_prnth:
            show_str = show_str+' '+curr_prnth.lower()
        return show_str
    
    def format_hide_chrctr(self, curr_chrct: str) -> str:
        return 'hide '+curr_chrct.lower()
    
    def set_ovrs(self, curr_chrct: str, is_onscreen: bool, curr_prnth: str = '', kind: str = 'AVL') -> None:
        if kind == 'BUBBLE':
            self.bubl_ovrs[curr_chrct].is_onscreen = is_onscreen
            if curr_prnth:
                self.bubl_ovrs[curr_chrct].last_prnth = curr_prnth
        elif kind == 'NVL':
            self.nvl_ovrs[curr_chrct].is_onscreen = is_onscreen
            if curr_prnth:
                self.nvl_ovrs[curr_chrct].last_prnth = curr_prnth
        else:
            self.avl_ovrs[curr_chrct].is_onscreen = is_onscreen
            if curr_prnth:
                self.avl_ovrs[curr_chrct].last_prnth = curr_prnth
    
    def is_necessary_prnth(self, curr_chrct: str, curr_prnth: str = '', kind : str = 'AVL') -> bool:
        if kind == 'BUBBLE':
            if self.bubl_ovrs[curr_chrct].last_prnth != curr_prnth and curr_prnth:
                return True
            elif self.bubl_ovrs[curr_chrct].last_prnth and not curr_prnth:
                return True
        elif kind == 'NVL':
            if self.nvl_ovrs[curr_chrct].last_prnth != curr_prnth and curr_prnth:
                return True
            elif self.nvl_ovrs[curr_chrct].last_prnth and not curr_prnth:
                return True
        else:
            if self.avl_ovrs[curr_chrct].last_prnth != curr_prnth and curr_prnth:
                return True
            elif self.avl_ovrs[curr_chrct].last_prnth and not curr_prnth:
                return True
        return False
    
    def format_chrctr_dialg(self, dialogue: str, chrctr_name: str = '', chrctr_objs: dict = {}) -> str:
        chrctr_dialg = ''
        if chrctr_name:
            chrctr_dialg = chrctr_objs[chrctr_name]+' \"'+dialogue+'\"\n'
        else:
            chrctr_dialg = '\"'+dialogue+'\"\n'
        return chrctr_dialg
    
    def collect_characters(self) -> None:
        self.all_chrctr: dict[Character_Attributes] = {}
        for chrctr in self.avl_chrctrs:
            if chrctr not in self.all_chrctr:
                self.all_chrctr[chrctr] = self.avl_ovrs[chrctr]
            else:
                self.all_chrctr[chrctr].lines_spoken += self.avl_ovrs[chrctr].lines_spoken
                for sprite in self.avl_ovrs[chrctr].sprites_used:
                    if sprite not in self.all_chrctr[chrctr].sprites_used:
                        self.all_chrctr[chrctr].sprites_used.append(sprite)
            if chrctr in self.bubl_ovrs:
                if chrctr not in self.all_chrctr:
                    self.all_chrctr[chrctr] = self.bubl_ovrs[chrctr]
                else:
                    self.all_chrctr[chrctr].lines_spoken += self.bubl_ovrs[chrctr].lines_spoken
                    for sprite in self.bubl_ovrs[chrctr].sprites_used:
                        if sprite not in self.all_chrctr[chrctr].sprites_used:
                            self.all_chrctr[chrctr].sprites_used.append(sprite)
            if chrctr in self.nvl_ovrs:
                if chrctr not in self.all_chrctr:
                    self.all_chrctr[chrctr] = self.nvl_ovrs[chrctr]
                else:
                    self.all_chrctr[chrctr].lines_spoken += self.nvl_ovrs[chrctr].lines_spoken
                    for sprite in self.nvl_ovrs[chrctr].sprites_used:
                        if sprite not in self.all_chrctr[chrctr].sprites_used:
                            self.all_chrctr[chrctr].sprites_used.append(sprite)
        for chrctr in self.bubl_chrctrs:
            if chrctr not in self.all_chrctr:
                self.all_chrctr[chrctr] = self.bubl_ovrs[chrctr]
            else:
                self.all_chrctr[chrctr].lines_spoken += self.bubl_ovrs[chrctr].lines_spoken
                for sprite in self.bubl_ovrs[chrctr].sprites_used:
                    if sprite not in self.all_chrctr[chrctr].sprites_used:
                        self.all_chrctr[chrctr].sprites_used.append(sprite)
            if chrctr in self.nvl_ovrs:
                if chrctr not in self.all_chrctr:
                    self.all_chrctr[chrctr] = self.nvl_ovrs[chrctr]
                else:
                    self.all_chrctr[chrctr].lines_spoken += self.nvl_ovrs[chrctr].lines_spoken
                    for sprite in self.nvl_ovrs[chrctr].sprites_used:
                        if sprite not in self.all_chrctr[chrctr].sprites_used:
                            self.all_chrctr[chrctr].sprites_used.append(sprite)
        for chrctr in self.nvl_chrctrs:
            if chrctr not in self.all_chrctr:
                self.all_chrctr[chrctr] = self.nvl_ovrs[chrctr]
            else:
                self.all_chrctr[chrctr].lines_spoken += self.nvl_ovrs[chrctr].lines_spoken
                for sprite in self.nvl_ovrs[chrctr].sprites_used:
                    if sprite not in self.all_chrctr[chrctr].sprites_used:
                        self.all_chrctr[chrctr].sprites_used.append(sprite)
        pass
    
    def __init__(self, read_path: str) -> None:
        res = Regular_Expressions()
        res.init_script()
        res.init_characters()
        res.init_render_styles()
        res.init_directions()
        res.init_headers()
        
        self.avl_chrctrs: list[str] = []
        self.nvl_chrctrs: list[str] = []
        self.bubl_chrctrs: list[str] = []
        
        self.is_spkng: bool = False
        self.curr_chrct: str = ''
        self.curr_extnt: str = ''
        self.curr_prnth: str = ''
        
        in_script: bool = False
        in_bubl: bool = False
        in_nvl: bool = False
        is_spkng: bool = False
        
        with open(read_path, 'r', encoding='utf-8') as read_file:
            try:
                for line in read_file:
                    if res.script_beg.match(line): in_script = True
                    elif res.script_end.match(line): break
                    elif in_script == True:
                        if curr_match := res.empty_line.match(line):
                            is_spkng = False
                            continue
                        elif res.scene_headr.match(line): continue 
                        elif res.cmmnt_line.match(line): continue
                        elif curr_match := res.chrct_name.match(line):
                            clean_name = curr_match.group(1).strip()
                            if not is_spkng:
                                is_spkng = True
                                if in_bubl:
                                    if clean_name not in self.bubl_chrctrs:
                                        self.bubl_chrctrs.append(clean_name)
                                elif in_nvl:
                                    if clean_name not in self.nvl_chrctrs:
                                        self.nvl_chrctrs.append(clean_name)
                                else:
                                    if clean_name not in self.avl_chrctrs:
                                        self.avl_chrctrs.append(clean_name)
                        elif curr_match := res.chng_drct.match(line):
                            clean_name = curr_match.group(1).strip()
                            if in_bubl:
                                if clean_name not in self.bubl_chrctrs:
                                    self.bubl_chrctrs.append(clean_name)
                            elif in_nvl:
                                if clean_name not in self.nvl_chrctrs:
                                    self.nvl_chrctrs.append(clean_name)
                            else:
                                if clean_name not in self.avl_chrctrs:
                                    self.avl_chrctrs.append(clean_name)
                        elif curr_match := res.appr_drct.match(line):
                            clean_name = curr_match.group(2).strip()
                            if in_bubl:
                                if clean_name not in self.bubl_chrctrs:
                                    self.bubl_chrctrs.append(clean_name)
                            elif in_nvl:
                                if clean_name not in self.nvl_chrctrs:
                                    self.nvl_chrctrs.append(clean_name)
                            else:
                                if clean_name not in self.avl_chrctrs:
                                    self.avl_chrctrs.append(clean_name)
                        elif curr_match := res.reset_rendr.match(line):
                            rsh = Render_Style_Handler()
                            in_bubl, in_nvl = rsh.set_speech_style('AVL')
                        elif curr_match := res.rendr_style.match(line):
                            rsh = Render_Style_Handler()
                            if curr_match.group(2) is not None:
                                in_bubl, in_nvl = rsh.set_speech_style(curr_match.group(2))
                            else:
                                in_bubl, in_nvl = rsh.set_speech_style('AVL')
            finally:
                read_file.close()
            
        print('STANDARD CHARACTERS:') 
        for char in self.avl_chrctrs:
            print(' - ' + char)
        
        print('BUBBLE CHARACTERS:')
        for char in self.bubl_chrctrs:
            print(' - ' + char)
            
        print('NVL CHARACTERS:')
        for char in self.nvl_chrctrs:
            print(' - ' + char)
            
        self.create_all()

'''
******************************************************************
QA_Keywords is a class that stores any keywords used by any of the
Quality Assurance classes to promote consistency in all Quality
Assurance Code.
'''
class QA_Keywords:
    error_type: str = 'ERROR'
    warn_type: str = 'WARNING'

'''
******************************************************************
Quality_Assurance_Message is a class that stores any information 
pertaining to an error/warning message. This object is stored in
Quality_Assurance_Report's 'messages' list whenever an 
error/warning is found.
'''
class Quality_Assurance_Message:
    def __init__(self, msg_type: str, msg_text: str, msg_tip: str) -> None:
        self.msg_type = msg_type
        self.msg_text: str = msg_text
        self.msg_tip: str = msg_tip

'''
******************************************************************
Quality_Assurance_Reporter is a class that stores any errors or 
warnings found in the read file filed provided to ren_form.py. Any
information stored is then used by class Run_Reporter.
'''
class Quality_Assurance_Reporter:
    def __init__(self) -> None:
        self.error: Quality_Assurance_Message = None
        self.warnings: list[Quality_Assurance_Message] = []
    
    def format_message(self, message: Quality_Assurance_Message) -> str:
        return message.msg_type+':\n  '+message.msg_text+'\n  '+message.msg_tip
    
    def get_messages(self, read_path) -> None:
        res = Regular_Expressions()
        res.init_all()
        res.init_quality_assurance()
        no_start = True
        no_end = True
        line_num = 0
        with open(read_path, 'r', encoding='utf-8') as read_file:
                try:
                    for line in read_file:
                        warn_msg: Quality_Assurance_Message = None
                        error_msg: Quality_Assurance_Message = None
                        is_error: bool = False
                        is_warning: bool = False
                        msg_text: str = ''
                        msg_tip: str = ''
                        line_num += 1
                        if res.script_beg.match(line):
                            no_start = False
                            continue
                        elif res.script_end.match(line):
                            no_end = False
                            break
                        if not no_start:
                            if res.empty_line.match(line): continue
                            elif res.scene_headr.match(line): continue
                            elif res.chrct_name.match(line): continue
                            elif res.scene_trans.match(line): continue
                            elif res.chng_drct.match(line): continue
                            elif res.appr_drct.match(line): continue
                            elif res.rendr_style.match(line): continue
                            elif res.reset_rendr.match(line): continue
                            elif res.rendr_style.match(line): continue
                            elif res.reset_text.match(line): continue
                            elif res.text_style.match(line): continue # CHECK TEXT STYLES?
                            elif error_match := res.unknw_extn.match(line):
                                is_error = True
                                msg_text = 'Invalid Character Name Extension \''+error_match.group(1)+'\' found on line '+str(line_num)
                                msg_tip = 'The only valid Character extensions are \'V.O.\' and \'O.S.\''
                            elif error_match := res.unkwn_drct.match(line):
                                is_error = True
                                msg_text = 'Invalid Character Direction \''+error_match.group(1)+'\' found on line '+str(line_num)
                                msg_tip = 'Make sure Character Directions follow the EXACT format specified by the documentation'
                            elif error_match := res.unkwn_rendr.match(line):
                                is_error = True
                                msg_text = 'Invalid Render Style Statement \''+error_match.group(1)+'\' found on line '+str(line_num)
                                msg_tip = 'Make sure Render Style Statements follow the EXACT format specified by the documentation'
                            elif warn_match := res.potnt_headr.match(line):
                                is_warning = True
                                msg_text = 'Potential Scene Header \''+warn_match.group(1)+'\' found on line '+str(line_num)
                                msg_tip = 'If this was supposed to be a Scene Header, follow format specified in the documentation.'
                            elif warn_match := res.potnt_drct.match(line):
                                is_warning = True
                                msg_text = 'Potential Character Direction \''+warn_match.group(1)+'\' found on line '+str(line_num)
                                msg_tip = 'If this was supposed to be a Character Direction, follow format specified in the documentation.'
                            elif warn_match := res.potnt_rendr.match(line):
                                is_warning = True
                                msg_text = 'Potential Render Style Statement \''+warn_match.group(1)+'\' found on line '+str(line_num)
                                msg_tip = 'If this was supposed to be a Render Style Statement, follow format specified in the documentation.'
                            elif warn_match := res.potnt_text.match(line):
                                is_warning = True
                                msg_text = 'Potential Text Style Statement \''+warn_match.group(1)+'\' found on line '+str(line_num)
                                msg_tip = 'If this was supposed to be a Text Style Statement, follow format specified in the documentation.'
                            if is_error:
                                error_msg = Quality_Assurance_Message(QA_Keywords.error_type, msg_text, msg_tip)
                            elif is_warning:
                                warn_msg = Quality_Assurance_Message(QA_Keywords.warn_type, msg_text, msg_tip)
                            else:
                                continue
                        if error_msg != None:
                            self.error = error_msg
                            break
                        if warn_msg != None:
                            self.warnings.append(warn_msg)
                finally:
                    read_file.close()
        if no_start:
            msg_text = r"Script Start Statement '///SCRIPT BEG\\\' never found!"
            msg_tip = 'Add Script Start Statement to read file, or use the -a flag at excecution.'
            error_msg = Quality_Assurance_Message(QA_Keywords.error_type, msg_text, msg_tip)
            self.error = error_msg
        if no_end:
            msg_text = r"Script End Statement '\\\SCRIPT END///' never found!"
            msg_tip = 'If needed, add a Script End Statement to prevent unexpected output.'
            warn_msg = Quality_Assurance_Message(QA_Keywords.warn_type, msg_text, msg_tip)
            self.warnings.insert(0, warn_msg)

'''
******************************************************************
Run_Reporter is a class that reports on several aspects of the 
most recent ren_form.py run. All information regarding the report 
is written to a report file with the following name format:
    [label_name]_report.txt
Where [label_name] is the label name passed to ren_form.py using 
the -l flag.
'''
class Run_Reporter:
    def __init__(self, label_name: str) -> None:
        self.label_name = label_name
        self.report_name = label_name.lower()+'_report.md'
        self.lines_narrated = 0
        self.images_used = [] # not to be confused with sprites_used
    
    def gather_characters(self, chrctr_handlr: Character_Object_Handler) -> None:
        pass
    
    def write_report(self, qar: Quality_Assurance_Reporter, coh: Character_Object_Handler) -> None:
        coh.collect_characters()
        with open(self.report_name, 'w', encoding='utf-8') as write_file:
            try:
                write_file.write('# Report for Ren\'Py Label: \''+self.label_name+'\'\nDate:\n\n'+str(dt.now()))
                write_file.write('\n\n## Warnings:')
                for warning in qar.warnings:
                    write_file.write('\n* '+warning.msg_text+': '+warning.msg_tip)
                write_file.write('\n\n## Characters:')
                write_file.write('\n* NARRATOR spoke '+str(self.lines_narrated)+' time(s).')
                for chrctr in coh.all_chrctr:
                    write_file.write('\n* '+chrctr+' spoke '+str(coh.all_chrctr[chrctr].lines_spoken)+' time(s).')
                write_file.write('\n\n## Character Sprites Used:')
                for chrctr in coh.all_chrctr:
                    write_file.write('\n* '+chrctr+' used '+str(len(coh.all_chrctr[chrctr].sprites_used))+' sprite(s):')
                    for sprite in coh.all_chrctr[chrctr].sprites_used:
                        write_file.write('\n    * '+sprite)
                write_file.write('\n\n## Images Used:')
                for image in self.images_used:
                    write_file.write('\n* '+image)   
            finally:
                write_file.close()

'''
******************************************************************
Run_Helper is a class that helps Run_Manager by storing some 
information and providing helper methods which provide 
functionality that can't be pinpointed to any, or just one, of the 
previous classes.
'''
class Run_Helper:
    def __init__(self) -> None:
        self.in_script: bool = False
        self.wrote_empty: bool = False
        self.image_num: int = 0
        self.voice_next: bool = False
        
    def escape_chars(self, string: str) -> str:
        string = re.sub(r'(?<!\\)\\(?!\\)', r'\\\\', string)
        string = re.sub(r'(?<!\\)[\"]', '\\"', string)
        string = re.sub(r'(?<!\\)[\"]', "\\'", string)
        string = re.sub(r'(?<!{){(?!{)', r'{{', string)
        string = re.sub(r'(?<!\[)\[(?!\[)', r'[[', string)
        string = re.sub(r'(?<!%|\\)%(?!%)', r'\\%', string)
        string = re.sub(r'(?<!【)【(?!【)', '【【', string)
        return string
    
    def clean_str(self, string: str) -> str:
        string = string.replace('’', "'")
        string = string.replace('“', '"')
        string = string.replace('”', '"')
        return string.strip()
    
    def format_name(self, string: str) -> str:
        return string.replace(' ','_').lower()

'''
******************************************************************
Run_Manager is a class that manages the read and write files
passed into the Argv_Parser after being checked by Argv_Handler.
TO DO:
    - Finish audio 
    - Add more flags to program:
        - audio flags:
            - no audio
            - no music
            - no sound
            - no voice
            - voice over (lines are fully voice acted; not "barks"/sound bytes)
        - render style:
            (def render style 'COMMON' by default)
            - snap
            - idle
        - speak style:
            (def speak style 'AVL' by default)
            - nvl
            - bubbles
        - character info:
            - aliases (when character in script isn't the actual character's name used for images)
            - no sprite char (character does not have any associated sprites)
            - pov character 
THINGS TO ADD?:
    - Refactor Render_Style_Handler to behave more like 
      Text_Style_Handler?
    - Add Choice Menu Generation?
        - Jumps
        - Responses
    - Add pov handler/protagonist handler (don't show a character 
      whenever they speak)
    - Add character position handler/pov style
    - Add Daniel Westfall's Kinetic Text Tags as options?
'''
class Run_Manager:
    def __init__(self) -> None:
        pass
    
    def run(read_path: str, write_path: str, label_name: str) -> None:
        qar = Quality_Assurance_Reporter()
        qar.get_messages(read_path)
        if qar.error:
            print(qar.format_message(qar.error))
            # return
        line_indent = '    '
        rh = Run_Helper()
        rr = Run_Reporter(label_name)
        res = Regular_Expressions()
        res.init_all()
        coh = Character_Object_Handler(read_path)
        rsh = Render_Style_Handler()
        sch = Scene_Handler()
        tsh = Text_Style_Handler()
        with open(write_path, 'w', encoding='utf-8') as write_file:
            try:
                with open(read_path, 'r', encoding='utf-8') as read_file:
                    try:
                        write_file.write('label ' + label_name + ':\n')
                        write_file.write(line_indent+'$ narrator = Character(name=None) # DELETE IF REDUNDANT\n')
                        for chrct in coh.avl_chrctrs:
                            write_file.write(line_indent+coh.create_chrct_objs(chrct,coh.avl_objs))
                        for chrct in coh.bubl_chrctrs:
                            write_file.write(line_indent+coh.create_chrct_objs(chrct,coh.bubl_objs,kind='BUBBLE'))
                        for chrct in coh.nvl_chrctrs:
                            write_file.write(line_indent+coh.create_chrct_objs(chrct,coh.nvl_objs,kind='NVL'))
                        
                        line_num: int = 0
                        for line in read_file:
                            line_num += 1
                            line = rh.clean_str(line)
                            write_string: str = ''
                            if res.script_beg.match(line): rh.in_script = True
                            elif res.script_end.match(line): break
                            elif rh.in_script:
                                if res.empty_line.match(line):
                                    if rh.wrote_empty:
                                        continue
                                    else:
                                        if coh.is_spkng:
                                            coh.is_spkng = False
                                            coh.curr_prnth = ''
                                            if tsh.curr_cond == 'SPEAK' and tsh.is_active:
                                                tsh.reset_all()
                                        rh.wrote_empty = True
                                        write_string = line_indent+'\n'
                                else:
                                    if curr_match := res.scene_headr.match(line):
                                        image_name = 'bg '+rh.format_name(curr_match.group(1).replace('.',''))+'_'+rh.format_name(curr_match.group(2))
                                        if curr_match.group(3) is not None:
                                            image_name = image_name+'_'+rh.format_name(curr_match.group(3))
                                        if image_name not in rr.images_used:
                                            rr.images_used.append(image_name)
                                        if sch.is_atl:
                                            sch.is_atl = False
                                            sch.curr_trnstn = '\n'+line_indent+sch.format_atl(sch.curr_trnstn, sch.last_headr, image_name)
                                        write_string = line_indent+sch.format_header(image_name, sch.curr_trnstn)
                                        sch.last_headr = image_name
                                        coh.reset_onscreen()
                                    elif curr_match := res.chrct_name.match(line):
                                        coh.is_spkng = True
                                        if tsh.curr_cond == 'NARRATE':
                                            tsh.reset_all()
                                        coh.curr_chrct = curr_match.group(1)
                                        if curr_match.group(2) is not None:
                                            coh.curr_extnt = curr_match.group(2)
                                        else:
                                            coh.curr_extnt = ''
                                        continue
                                    elif curr_match := res.scene_trans.match(line):
                                        trnstn_name = rh.format_name(curr_match.group(1))
                                        if sch.is_predefined(curr_match.group(1)):
                                            sch.curr_trnstn = '\n'+line_indent+sch.format_predefined(trnstn_name)
                                        else:
                                            sch.is_atl = True
                                            sch.curr_trnstn = rh.format_name(trnstn_name)
                                        continue
                                    elif curr_match := res.reset_rendr.match(line):
                                        rsh.in_idle, rsh.in_snap = rsh.set_image_style('COMMON')
                                        rsh.in_bubl, rsh.in_nvl = rsh.set_speech_style('AVL')
                                        write_string = line_indent+rsh.redefine_narrator()
                                    elif curr_match := res.rendr_style.match(line):
                                        if curr_match.group(1) is not None:
                                            rsh.in_idle, rsh.in_snap = rsh.set_image_style(curr_match.group(1))
                                        elif curr_match.group(3) is not None:
                                            rsh.in_idle, rsh.in_snap = rsh.set_image_style(curr_match.group(3))
                                        if curr_match.group(2) is not None:
                                            rsh.in_bubl, rsh.in_nvl = rsh.set_speech_style(curr_match.group(2))
                                        if rsh.in_bubl:
                                            write_string = line_indent+rsh.redefine_narrator('BUBBLE')
                                        elif rsh.in_nvl:
                                            write_string = line_indent+rsh.redefine_narrator('NVL')
                                        else:
                                            write_string = line_indent+rsh.redefine_narrator()
                                    elif curr_match := res.reset_text.match(line):
                                        tsh.reset_all()
                                        continue
                                    elif curr_match := res.text_style.match(line):
                                        tsh.is_active = True
                                        tsh.get_text_styles(curr_match.group(1))
                                        continue
                                    elif curr_match := res.chng_drct.match(line):
                                        curr_sprite = (curr_match.group(1)+' '+curr_match.group(2)).strip().lower()
                                        if rsh.in_bubl:
                                            coh.bubl_ovrs[curr_match.group(1)].is_onscreen = True
                                            if curr_sprite not in coh.bubl_ovrs[curr_match.group(1)].sprites_used:
                                                coh.bubl_ovrs[curr_match.group(1)].sprites_used.append(curr_sprite)
                                        elif rsh.in_nvl:
                                            coh.nvl_ovrs[curr_match.group(1)].is_onscreen = True
                                            if curr_sprite not in coh.nvl_ovrs[curr_match.group(1)].sprites_used:
                                                coh.nvl_ovrs[curr_match.group(1)].sprites_used.append(curr_sprite)
                                        else:
                                            coh.avl_ovrs[curr_match.group(1)].is_onscreen = True
                                            if curr_sprite not in coh.avl_ovrs[curr_match.group(1)].sprites_used:
                                                coh.avl_ovrs[curr_match.group(1)].sprites_used.append(curr_sprite)
                                        write_string = line_indent+coh.format_show_chrctr(curr_match.group(1), curr_match.group(2))+'\n'
                                    elif curr_match := res.appr_drct.match(line):
                                        if curr_match.group(1) == 'ENTER':
                                            curr_sprite = (curr_match.group(2)).lower()
                                            if rsh.in_bubl:
                                                coh.bubl_ovrs[curr_match.group(2)].is_onscreen = True
                                                if curr_sprite not in coh.bubl_ovrs[curr_match.group(2)].sprites_used:
                                                    coh.bubl_ovrs[curr_match.group(2)].sprites_used.append(curr_sprite)
                                            elif rsh.in_nvl:
                                                coh.nvl_ovrs[curr_match.group(2)].is_onscreen = True
                                                if curr_sprite not in coh.nvl_ovrs[curr_match.group(2)].sprites_used:
                                                    coh.nvl_ovrs[curr_match.group(2)].sprites_used.append(curr_sprite)
                                            else:
                                                coh.avl_ovrs[curr_match.group(2)].is_onscreen = True
                                                if curr_sprite not in coh.avl_ovrs[curr_match.group(2)].sprites_used:
                                                    coh.avl_ovrs[curr_match.group(2)].sprites_used.append(curr_sprite)
                                            write_string = line_indent+coh.format_show_chrctr(curr_match.group(2))+'\n'
                                        else:
                                            if rsh.in_bubl:
                                                coh.bubl_ovrs[coh.curr_chrct].is_onscreen = False
                                            elif rsh.in_nvl:
                                                coh.nvl_ovrs[coh.curr_chrct].is_onscreen = False
                                            else:
                                                coh.avl_ovrs[coh.curr_chrct].is_onscreen = False
                                            write_string = line_indent+coh.format_hide_chrctr(curr_match.group(2))+'\n'
                                    elif curr_match := res.music_stmt.match(line):
                                        write_string = line_indent+'play music '+rh.format_name(curr_match.group(1))+'\n'
                                    elif curr_match := res.voice_stmt.match(line):
                                        write_string = line_indent+'play voice '+rh.format_name(curr_match.group(1))+'\n'
                                    elif curr_match := res.sound_stmt.match(line):
                                        write_string = line_indent+'play sound '+rh.format_name(curr_match.group(1))+'\n'
                                    elif curr_match := res.audio_stmt.match(line):
                                        write_string = line_indent+'play '+rh.format_name(curr_match.group(1))+' '+rh.format_name(curr_match.group(2))+'\n'
                                    elif coh.is_spkng:
                                        is_prnth: bool = False
                                        if curr_match := res.chrct_prnth.match(line):
                                            is_prnth = True
                                            coh.curr_prnth = curr_match.group(1)
                                        if rsh.in_snap and not is_prnth:
                                            image_name = rsh.format_image_name(label_name,rh.image_num)
                                            rr.images_used.append(image_name)
                                            write_string = line_indent+'show '+image_name+'\n'
                                            rh.image_num += 1
                                        elif rsh.in_idle:
                                            pass # Only Scene Headers can change the background while in an IDLE Style
                                        else:
                                            if coh.curr_extnt != 'O.S.':
                                                curr_sprite = (coh.curr_chrct+' '+coh.curr_prnth).strip().lower()
                                                write_show = False
                                                if rsh.in_bubl:
                                                    is_onscreen: bool = coh.bubl_ovrs[coh.curr_chrct].is_onscreen
                                                    if (not is_onscreen) or (coh.is_necessary_prnth(coh.curr_chrct,coh.curr_prnth,'BUBBLE') and is_onscreen):
                                                        write_show = True
                                                        coh.set_ovrs(coh.curr_chrct,True,coh.curr_prnth,'BUBBLE')
                                                        if curr_sprite not in coh.bubl_ovrs[coh.curr_chrct].sprites_used:
                                                            coh.bubl_ovrs[coh.curr_chrct].sprites_used.append(curr_sprite)
                                                elif rsh.in_nvl:
                                                    is_onscreen: bool = coh.nvl_ovrs[coh.curr_chrct].is_onscreen
                                                    if (not is_onscreen) or (coh.is_necessary_prnth(coh.curr_chrct,coh.curr_prnth,'NVL') and is_onscreen):
                                                        write_show = True
                                                        coh.set_ovrs(coh.curr_chrct,True,coh.curr_prnth,'NVL')
                                                        if curr_sprite not in coh.nvl_ovrs[coh.curr_chrct].sprites_used:
                                                            coh.nvl_ovrs[coh.curr_chrct].sprites_used.append(curr_sprite)
                                                else:
                                                    is_onscreen: bool = coh.avl_ovrs[coh.curr_chrct].is_onscreen
                                                    if (not is_onscreen) or (coh.is_necessary_prnth(coh.curr_chrct,coh.curr_prnth) and is_onscreen):
                                                        write_show = True
                                                        coh.set_ovrs(coh.curr_chrct,True,coh.curr_prnth)
                                                        if curr_sprite not in coh.avl_ovrs[coh.curr_chrct].sprites_used:
                                                            coh.avl_ovrs[coh.curr_chrct].sprites_used.append(curr_sprite)
                                                if write_show:
                                                    write_string = line_indent+coh.format_show_chrctr(coh.curr_chrct, coh.curr_prnth)+'\n'
                                            else:
                                                if rsh.in_bubl and coh.bubl_ovrs[coh.curr_chrct].is_onscreen == True:
                                                    coh.bubl_ovrs[coh.curr_chrct].is_onscreen = False
                                                    write_string = line_indent+coh.format_hide_chrctr(coh.curr_chrct)+'\n'
                                                elif rsh.in_nvl and coh.nvl_ovrs[coh.curr_chrct].is_onscreen == True:
                                                    coh.nvl_ovrs[coh.curr_chrct].is_onscreen = False
                                                    write_string = line_indent+coh.format_hide_chrctr(coh.curr_chrct)+'\n'
                                                elif coh.avl_ovrs[coh.curr_chrct].is_onscreen == True:
                                                    coh.avl_ovrs[coh.curr_chrct].is_onscreen = False
                                                    write_string = line_indent+coh.format_hide_chrctr(coh.curr_chrct)+'\n'
                                        if not is_prnth:
                                            line = rh.escape_chars(line)
                                            if tsh.is_active:
                                                true_conds = ['SPEAK', TS_Keywords.count_cond, 'INF']
                                                if tsh.curr_cond in true_conds:
                                                    if tsh.line_count != 0:
                                                        line = tsh.tag_prefix+tsh.apply_case(line)+tsh.tag_suffix
                                                        if tsh.line_count > 0:
                                                            tsh.line_count -= 1
                                                    if tsh.line_count == 0:
                                                        tsh.reset_all()
                                            if coh.curr_extnt != 'V.O.':
                                                if rsh.in_bubl:
                                                    write_string = write_string+line_indent+coh.format_chrctr_dialg(line,coh.curr_chrct,coh.bubl_objs)
                                                elif rsh.in_nvl:
                                                    write_string = write_string+line_indent+coh.format_chrctr_dialg(line,coh.curr_chrct,coh.nvl_objs)
                                                else:
                                                    write_string = write_string+line_indent+coh.format_chrctr_dialg(line,coh.curr_chrct,coh.avl_objs)
                                            else:
                                                write_string = write_string+line_indent+coh.format_chrctr_dialg(line)
                                            if rsh.in_bubl:
                                                coh.bubl_ovrs[coh.curr_chrct].lines_spoken += 1
                                            elif rsh.in_nvl:
                                                coh.nvl_ovrs[coh.curr_chrct].lines_spoken += 1
                                            else:
                                                coh.avl_ovrs[coh.curr_chrct].lines_spoken += 1
                                    elif res.cmmnt_line.match(line):
                                        write_string = line_indent+line.strip()
                                    else:
                                        line = rh.escape_chars(line)
                                        if tsh.is_active:
                                            true_conds = ['NARRATE', TS_Keywords.count_cond, 'INF']
                                            if tsh.curr_cond in true_conds:
                                                if tsh.line_count != 0:
                                                    line = tsh.tag_prefix+tsh.apply_case(line)+tsh.tag_suffix
                                                    if tsh.line_count > 0:
                                                        tsh.line_count -= 1
                                                if tsh.line_count == 0:
                                                    tsh.reset_all()
                                        write_string = line_indent+'\"'+line+'\"\n'
                                        rr.lines_narrated += 1
                                    rh.wrote_empty = False
                            write_file.write(write_string)
                    finally:
                        read_file.close()
                write_file.write(line_indent + 'return')
            finally:
                write_file.close()
        rr.write_report(qar,coh)    

'''
******************************************************************
The Help_Formatter class changes the format of the 
ArgumentParser's help menu (accessed via -h) to NOT show the 
metavar instead of showing it after every flag. Useful for visual 
clarity, and maintains metavar for access.
'''
class Help_Formatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        return ', '.join(action.option_strings)

'''
******************************************************************
The Argv_Parser class stores all of the flags used on the command 
line by using an ArgumentParser. Also adds flag information which 
can be accessed when entering the -h or --help flag on the command
line.
'''
class Argv_Parser:
    def __init__(self):
        # lambda for formatting help menu in argparser
        fmt = lambda prog: Help_Formatter(prog)
        self.parser = argparse.ArgumentParser(usage=sys.argv[0] + ' -r [file options] -t [prog params] [prog options]', description='A collection of flags used by ' + sys.argv[0] + ' for the command line interface.', formatter_class=fmt)
        self.parser._optionals.title = 'arguments' # risky line of code, can break ArgumentParser in a future update
        
        # flags for file arguments, stored as stirng values
        self.parser.add_argument('-r', '--read', dest='READ', help='(REQUIRED) set file program will read from', required=True)
        self.parser.add_argument('-w', '--write', dest='WRITE', help='(REQUIRED) set file program will write to', required=True)
        self.parser.add_argument('-l', '--label', dest='LABEL', help='(REQUIRED) set label name in rpy file', required=True)

'''
******************************************************************
The File_Validator class handels all the file validation before 
the program runs successfully. Raises expections when files cannot 
be accessed with the desired permisions, and if the file does not
contain the desired extension.
'''
class File_Validator:
    def __init__(self) -> None:
        return None
    
    def is_valid_mode(file: str, input_mode: str) -> None:
        valid_modes = ['r', 'a', 'w']
        valid_handle = ['', 't', 'b']
        valid_plus = ['', '+']
        for mode in valid_modes:
            for handle in valid_handle:
                for plus in valid_plus:
                    curr_mode = mode + handle + plus
                    if curr_mode == input_mode:
                        return None
        if input_mode == 'x':
            return None
        raise Exception('INVALID MODE: mode \"' + input_mode + '\" is not a valid mode to open the file \"' + file + '\"')
    
    def is_valid_access(file: str, mode: str) -> None:
        if mode == 'r' and not os.access(file, os.R_OK):
            raise Exception('INVALID ACCESS: file \"' + file + '\" does not allow read access')
        elif mode in ['a', 'w']:
            if os.path.exists(file) and not os.access(file, os.W_OK):
                raise Exception('INVALID ACCESS: file \"' + file + '\" does not allow write access')
            else:
                pass
        elif mode == 'x' and os.access(file, os.F_OK):
            raise Exception('INVALID ACCESS: file \"' + file + '\" already exists')
        
    def is_valid_file(file: str, extension: str, mode: str) -> None:
        if (file == ''):
            raise Exception('INVALID FILE: file \"' + file + '\" cannot be an empty string')
        if not os.path.exists(file) and mode not in ['a', 'w']:
            raise Exception('INVALID FILE: file \"' + file + '\" does not exist')
        File_Validator.is_valid_mode(file, mode)
        File_Validator.is_valid_access(file, mode)
        if not file.endswith(extension):
            raise Exception('INVALID FILE: file \"' + file + '\" is not a \"' + extension + '\" file')
    
    def is_valid_script(read_path: str) -> None:
        pass

'''
******************************************************************
The Argv_Handler class checks all the arguments parsed into
main.py using the Argv_Parser() class. This class guarantees that 
all arguments passed into the program are valid and ready for 
their use in Run_Manager.
'''
class Argv_Handler:
    def __init__(self) -> None:
        return None
    
    def check_args(args: argparse.Namespace) -> None:
        File_Validator.is_valid_file(args.READ, '.txt', 'r')
        File_Validator.is_valid_file(args.WRITE, '.rpy', 'w')
        return None

def main():
    arg_parse = Argv_Parser()
    args = arg_parse.parser.parse_args()
    ts = Text_Style_Handler()
    Argv_Handler.check_args(args)
    Run_Manager.run(args.READ, args.WRITE, args.LABEL)

if __name__ == '__main__':
    main()