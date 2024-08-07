import json
from bs4 import BeautifulSoup
import requests

with open("out.json", "r") as file:
    arr = json.loads(file.read())

professors = set()


for i in arr:
    professors.add(i["lecture"]["prof"])

    if "prof" in i["lab"]:
        professors.add(i["lab"]["prof"])

professors.remove("")

with open("professors.json", "w") as file:
    file.write(json.dumps(list(professors)))

ratings = []


def algo(name: str):
    fName = name.split(",")[0].strip().split(" ")
    lName = name.split(",")[1].strip().split(" ")

    # name = Giroux, Cynthia Elaine (Cindy)
    # fName = ["Cynthia", "Elaine", "(Cindy)"]
    # lName = ["Giroux"]

    allCombinasion = [name]

    # first check will the full name
    # if can't fund it, search for a variant of the name

    for i in fName:
        for j in lName:
            allCombinasion.append(i + " " + j)

    allCombinasion += [name.split(",")[0], name.split(",")[1]]

    return allCombinasion


for i in professors:
    pArr = algo(i)
    print(pArr)
    length = len(pArr)

    score = 0
    avg = 0
    nRating = 0
    takeAgain = 0
    difficulty = 0
    name = ""
    status = ""

    # Bouras, Eugenia (Jenny)
    # [Bouras, Eugenia, (Jenny)]

    # try for every combinasion of their names
    for comb in pArr:
        p = "%20".join(comb.replace(",", "").split(" "))

        url = f"https://www.ratemyprofessors.com/search/professors/12050?q={p}"
        r = requests.get(url)

        if r.status_code != 200:
            raise

        soup = BeautifulSoup(r.text, "html.parser")

        script = soup.find_all("script")[-2]

        text = script.text.split(",")

        try:
            if not '"school":{"__ref":"U2Nob29sLTEyMDUw"}' in text:
                raise

            name = list(filter(lambda i: "firstName" in i or "lastName" in i, text))

            firstName = name[0].split(":")[1].replace('"', "")
            lastName = name[1].split(":")[1].replace('"', "")

            if firstName not in i or lastName not in i:
                raise

            avg = float(list(filter(lambda i: "avgRating" in i, text))[0].split(":")[1])
            nRating = float(
                list(filter(lambda i: "numRatings" in i, text))[0].split(":")[1]
            )
            takeAgain = float(
                list(filter(lambda i: "wouldTakeAgainPercent" in i, text))[0].split(
                    ":"
                )[1]
            )
            difficulty = float(
                list(filter(lambda i: "avgDifficulty" in i, text))[0].split(":")[1]
            )

            status = "found"

            break

        except:
            # continue to next iteration
            status = "foundn't"

    if avg != 0 and nRating != 0:
        score = round((((avg * nRating) + 5) / (nRating + 2)) * 100 / 5, 1)

    ratings.append(
        {
            "prof": i,
            "score": score,
            "avg": avg,
            "nRating": nRating,
            "takeAgain": takeAgain,
            "difficulty": difficulty,
            "status": status,
        }
    )


with open("ratings.json", "w") as file:
    file.write(json.dumps(ratings, indent=2))
