if [[ $# -lt 2 ]]
then
    echo 'usage: replace.sh old_string new_string'
    exit 1
fi

for file in $(find . -type f -name '*.p[yt]')
do
    echo $file
done
