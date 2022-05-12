echo "Sync up template"
git remote add upstream git@github.azc.ext.hp.com:BPSVCommonService/Action-ExecutorTemplate.git
git fetch upstream
git merge upstream/master --allow-unrelated-histories
git remote remove upstream