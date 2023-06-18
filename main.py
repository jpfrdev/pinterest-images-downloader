from pinterest_handler import PHandler

if __name__ == '__main__':
    words = input("Search for: ")
    while True:
        try:
            total = int(input("Total results: "))
            if total <= 0:
                raise Exception
        except Exception:
            print("ERROR: Please provide a number greater than 0")
            continue
        try:
            ph = PHandler()
            ph.download_images(words=words,total=total)
            break
        except Exception as e:
            print(f"ERROR: {e}")