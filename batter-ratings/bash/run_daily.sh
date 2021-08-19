if [ $HOSTNAME = sportsites ]; then
  DIR='/home/snewman/code/basewinner.com/batter-ratings/'
  PYTHON='/home/snewman/.Envs/basewinner/bin/python'
else
  DIR='/Users/snewman/projects/python/basewinner.com/batter-ratings/'
  PYTHON='/Users/snewman/.Envs/basewinner/bin/python'
fi

cd $DIR

YESTERDAY=`date -d "1 day ago" +%Y-%m-%d`

$PYTHON fetch.py $YESTERDAY > /dev/null
$PYTHON batters.py ./public_html > /dev/null
$PYTHON aggregate.py ./public_html > /dev/null
