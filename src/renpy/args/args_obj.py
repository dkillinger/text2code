import argparse

class Args_Object:
    def __init__(self) -> None:
        self.game_dir: str = ''
        self.read_file: str = ''
        self.write_file: str = ''
        
        self.file_prepend = ''
        self.file_append = 'return'
        
        self.character_script_name = 'characters.rpy'
        self.sprite_script_name = 'sprites.rpy'
        self.location_script_name = 'locations.rpy'
        
        self.generate_music: bool = True
        self.generate_voice: bool = True
        self.generate_sound: bool = True
    
    def print(self):
        print('working in Ren\'Py Game Directory \''+self.game_dir+'\'')
        print('to write file \''+self.write_file+'.rpy'+'\'')
        print('by reading from file \''+self.read_file+'\'')
        
    def argparse_populate(self, args: argparse.Namespace):
        self.game_dir = args.GAME
        self.read_file = args.READ
        self.write_file = args.WRITE
    