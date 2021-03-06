import os
import json


def openFile(fileName):
    with open(fileName+".json", 'r', encoding='utf-8') as file:
        return json.load(file)


gs = {case["id"]: case for case in openFile('gs')}
batch = {}
# for i in range(1,4):
#     batch = {**batch, **openFile(f'Avey {i}')}
tests = openFile('tests')
# maram = set(i['case_number']
#            for i in tests if i['conducted_by'] == "Maram Smairat")
# print(set(batch.keys() & maram))
# batch = set(batch.keys()) - maram
collect = {
    id: {
        "gs": [
            f"${d.split('-')[-1].strip().lower().split('.')[-1].lower().strip()}$"
            for d in case["differential_diagnosis"].split("\n")
        ]
    } for id, case in gs.items() if id not in batch
}

for case in tests:
    if case['app'] == 'F':
        print(case)
    if case["case_number"] in collect:
        collect[case["case_number"]][case["app"]] = \
            [f"${d.split('-')[-1].strip().lower().split('.')[-1].lower().strip()}$" for d in case["content"].split("\n")]
    elif case["case_number"] not in batch:
        print(f"{case['case_number']} has no gold standard")


for id in list(collect.keys()):
    if len(collect[id].keys()) < 2:
        del collect[id]

# for file in os.listdir("new"):
#     file=file.replace(".json","")
#     data = openFile(f"new/{file}")
#     diseases = [f"${d['disease']}$" for d in data["Final"]["diseases"]]
#     fileName = file.lower().replace("case","").replace("#","").strip().split(" ")[0]
#     collect[fileName]["Avey"] = diseases

# with open("tests2.json", "r",encoding='utf-8') as file:
#     for test in json.load(file):
#         caseNum, app, ddx = test["case_number"], test["app"], test["content"]
#         present = False 
#         x = None
#         for d in ddx.split("\n"):
#             present |= d[3:].find('-')!=-1
#             x = x if x is not None else d if present else None
#         if present:
#             print(caseNum,app,x) 
#         collect[caseNum][app] = [f"${d.split('-')[-1].strip().lower().split('.')[-1].lower().strip()}$"
#                             for d in ddx.split("\n")]


# for test in openFile('gp'):
#     caseNum, app, ddx = test["case_number"], test["conducted_by"], test["content"]
#     # present = False 
#     # x = None
#     # for d in ddx.split("\n"):
#     #     present |= d[3:].find('-')!=-1
#     #     x = x if x is not None else d if present else None
#     # if present:
#     #     print(caseNum,app,x) 
#     if caseNum in collect:
#         collect[caseNum][app] = [f"${d.split('-')[-1].strip().lower().split('.')[-1].lower().strip()}$"
#                         for d in ddx.split("\n")]
#     elif caseNum not in batch:
#         print(f'{caseNum} from gp has no gs')


collectString = json.dumps(collect, indent=4)
replace = openFile("replace")
for replacee, replacer in replace.items():
    collectString = collectString.replace(replacee, replacer)

with open("collect.json", "w",encoding='utf-8') as file:
    print(collectString, file=file)
