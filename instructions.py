
class Instruction:

    def __init__(self) -> None:
        self.file = open('instrucciones.txt', 'r', encoding= 'utf-8')
        

    def get_content_file(self):
        instruction = ''

        for line in self.file:
            instruction += line
        
        return instruction
        

if __name__ == '__main__':

    instruccion = InstruInstructionccion()
    instruccion.get_file()