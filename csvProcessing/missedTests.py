import json

with open("failedCases.csv", "r") as file:
    data = file.readlines()

attach = False
lines = []
for line in data:
    if attach:
        lines[-1] += line
        lines[-1] = lines[-1].replace('"', "")
        if line.count('"') == 1:
            attach = False
    elif '"' in line:
        attach = True
        lines.append(line)
    else:
        lines.append(line)

lines = [line.lower().strip().split(",") for line in lines]
lines = {line[0].replace("#", ""): line[2:] for line in lines[1:]}

apps = {
    "Avey": {"session failed": [], "no disease found": [], },
    "Ada": {"session failed": [], "no disease found": [], },
    "Babylon": {"session failed": [], "no disease found": [], },
    "Buoy": {"session failed": [], "no disease found": [], },
    "K health": {"session failed": [], "no disease found": [], },
    "WebMD": {"session failed": [], "no disease found": [], }
}

for app, val in apps.items():
    app = app.lower()
    for case, res in lines.items():
        if app in res[0]:
            val["no disease found"].append(int(case))
        if True in [app in x for x in res[1:]]:
            val["session failed"].append(int(case))

with open("lines.json", "w") as file:
    print(json.dumps(lines, indent=4), file=file)

with open("fail.json","w") as file:
    json.dump(apps,file,indent=4)
