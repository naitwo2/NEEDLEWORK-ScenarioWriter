#/bin/sh

export PYTHONPATH=/NEEDLEWORK-ScenarioWriter 
if [ -z ${DISABLE_POLICY_OUTPUT} ]; then
    python /NEEDLEWORK-ScenarioWriter/main/gencsv.py /scenario.txt
elif [ "y" = ${DISABLE_POLICY_OUTPUT} ]; then
    python /NEEDLEWORK-ScenarioWriter/main/gencsv.py /scenario.txt y
elif [ "n" = ${DISABLE_POLICY_OUTPUT} ]; then
    python /NEEDLEWORK-ScenarioWriter/main/gencsv.py /scenario.txt n
fi
echo "=======CSVを出力します======="
CSV=$(ls -1 SSG_convert_*.csv)
cat $CSV