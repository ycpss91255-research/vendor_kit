import json, sys
task, name = sys.argv[1], sys.argv[2]
r = json.load(open(f"tasks/{task}.output"))["result"]; m = r["merged"]
out = [f"# {name}", "", "## 一致"] + [f"- {x}" for x in m["agree"]] + ["", "## 分歧（含判斷）"] + [f"- {x['point']}：{x['my_take']}" for x in m["disagree"]] + ["", "## 對前例資料的更正"] + [f"- {x}" for x in m["agy_corrections"]] + ["", "## 最終建議", m["final_recommendation"], "", "## 要問使用者"] + [f"- {x}" for x in m["questions_for_user"]]
open(f"scratchpad/decisions/{name}.md", "w").write("\n".join(out)); print(name, "questions:", len(m["questions_for_user"]))
