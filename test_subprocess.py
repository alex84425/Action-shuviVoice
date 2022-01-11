import subprocess

cmd = ["git", "ls-remote", "git@github.azc.ext.hp.com:BPSVCommonService/Action-ExecutorTemplateAlex_123.git"]
cmd = subprocess.list2cmdline((map(str, cmd)))
# print(cmd)
p = subprocess.run(cmd, capture_output=True, check=False, shell=True, encoding="utf-8")
print(p.stderr)
# print(p.stdout)"z"
if "Repository not found" in p.stderr:
    print("detect!")
print("Try to run: ", cmd)
