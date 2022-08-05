#!/bin/bash
pushd /integration

echo "================================= Starting test ================================="
python -m pytest --log-cli-level=DEBUG -s -vvv -p no:warnings --junitxml=junit.xml
mkdir -p /var/results/
if [[ ${ENV} == 'dev' ]] ; then
    cp junit.xml /var/results/TEST-RESULT-DEV.xml
elif [[ ${ENV} == 'qa' ]] ; then
    cp junit.xml /var/results/TEST-RESULT-QA.xml
elif [[ ${ENV} == 'itg' ]] ; then
    cp junit.xml /var/results/TEST-RESULT-ITG.xml
elif [[ ${ENV} == 'prd' ]] ; then
    cp junit.xml /var/results/TEST-RESULT-PRD.xml
else
    /bin/bash ./basicCheckSiteServiceStatusDemo.sh
fi
ls /var/results/
echo "================================= End test ================================="

popd
