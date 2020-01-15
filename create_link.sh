#create a soft link from src ($2) to target ($)
#./create_link xxx yyy
# xxx is the new link
echo 'create_link',$1, $2

#gnome-terminal -x $SHELL -ic "echo $1 $2; ln -s $2 $1; bash"
ln -s $2 $1
