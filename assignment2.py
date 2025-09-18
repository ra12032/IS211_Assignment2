import argparse
import urllib.request
import logging
import datetime
import ssl

def downloadData(url):
    """Downloads the data"""
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(url, context=context) as response:
        return response.read().decode('utf-8')

def processData(file_content):
    logger = logging.getLogger('assignment2')
    lines = file_content.splitlines()
    personData = {}
    for idx, line in enumerate(lines, start=1):
        parts = line.strip().split(',')
        if len(parts) != 3:
            continue
        id_str, name, birthday_str = parts
        try:
            id_num = int(id_str)
            birthday = datetime.datetime.strptime(birthday_str, "%d/%m/%Y").date()
            personData[id_num] = (name, birthday)
        except Exception:
            logger.error(f"Error processing line #{idx} for ID #{id_str}")
    return personData

def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday}")
    else:
        print("No user found with that id")

def main(url):
    print(f"Running main with URL = {url}...")

    logging.basicConfig(filename='errors.log', level=logging.ERROR)

    try:
        csvData = downloadData(url)
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    personData = processData(csvData)

    while True:
        try:
            user_input = int(input("Enter ID to look up (0 or negative to exit): "))
        except ValueError:
            print("Please enter a valid integer ID")
            continue
        if user_input <= 0:
            break
        displayPerson(user_input, personData)

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)