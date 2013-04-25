if [[ $# -lt 2 ]]
then
    echo 'usage: replace.sh old_string new_string'
    exit 1
fi

old_string=$1
new_string=$2

echo "Old string: $1"
echo "New string: $2"

find . -type f -exec sed -i "'s/${old_string}/${new_string}/g'" {} \;
mv templates/${old_string}.pt templates/${new_string}.pt
