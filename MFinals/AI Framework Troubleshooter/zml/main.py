from v3.extracting import extract
from v3.preparing import prepare
from v3.model import model

def main():
    extract()
    print("✅ extract")
    prepare()
    print("✅ prepare")
    model()
    print("✅ model")
    
if __name__ == "__main__":
    main()
