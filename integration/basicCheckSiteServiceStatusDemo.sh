#!/bin/bash

TEST_RESULT_FOLDER="/var/results"

echo '<?xml version="1.0" ?>
<testsuites>
    <testsuite errors="0" failures="0" id="0" name="Basic suite" tests="5">
        <testcase classname="test.service.action.dummy"        name="Test Action-Dummy" time="66.345000" Status="FAIL"/>
    </testsuite>
    <description>
        This is an example report which is generated only when your site is not in dev/qa/itg/prd.
        I am not an error.
    </description>
</testsuites>' > ${TEST_RESULT_FOLDER}/TEST-result_docker.xml

# cat ${TEST_RESULT_FOLDER}/TEST-result_docker.xml
