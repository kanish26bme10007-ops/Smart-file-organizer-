import os
import shutil

FILE_TYPES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav"]
}

undo_data = []

def get_category(ext):
    for category, types in FILE_TYPES.items():
        if ext.lower() in types:
            return category
    return "Others"

def organize_files(folder):
    moved = 0
    for file in os.listdir(folder):
        source = os.path.join(folder, file)

        if os.path.isfile(source):
            ext = os.path.splitext(file)[1]
            category = get_category(ext)

            dest_folder = os.path.join(folder, category)
            os.makedirs(dest_folder, exist_ok=True)

            dest = os.path.join(dest_folder, file)
            shutil.move(source, dest)

            undo_data.append((dest, source))
            moved += 1

    print(f"\n {moved} files organized.")

def undo():
    if not undo_data:
        print("No operation to undo.")
        return

    for dest, source in reversed(undo_data):
        if os.path.exists(dest):
            shutil.move(dest, source)

    undo_data.clear()
    print(" Undo completed.")

def report(folder):
    total = 0
    print("\n--- REPORT ---")

    for category in list(FILE_TYPES.keys()) + ["Others"]:
        path = os.path.join(folder, category)

        if os.path.exists(path):
            count = len(os.listdir(path))
            print(f"{category}: {count} files")
            total += count

    print("Total Files:", total)

def main():
    folder = input("Enter folder path: ")

    if not os.path.exists(folder):
        print("Invalid path")
        return

    while True:
        print("\n1. Organize Files")
        print("2. Generate Report")
        print("3. Undo Organization")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            organize_files(folder)
        elif choice == "2":
            report(folder)
        elif choice == "3":
            undo()
        elif choice == "4":
            break
        else:
            print("Invalid choice")

main()
