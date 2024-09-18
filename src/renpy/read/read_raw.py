# Read class for .txt .fountain and .md

class Read_RenPy_Raw:
    def __init__(self) -> None:
        pass
    
    def read(read_path: str):
        with open(read_path, 'rb', encoding='utf-8') as read_file:
            try:
                for line in read_file:
                    print(line)
            finally:
                read_file.close()