if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/AllOkOfficial/BOTx.git /BOTx
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /BOTx
fi
cd /BOTx
pip3 install -U -r requirements.txt
echo "Starting TeleMoviesRobot...."
python3 bot.py
