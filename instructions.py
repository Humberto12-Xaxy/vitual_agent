
class Instruction:

    def __init__(self) -> None:
        self.file = None
        

    def set_file(self, path_intructions):
        self.file = open(path_intructions, 'r', encoding= 'utf-8')

    def get_content_file(self):
        instruction = ''

        for line in self.file:
            instruction += line
        
        return instruction
        