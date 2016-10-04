function split(){
    mkdir -p file
    python3 Split.py $1 file
}

function mysql(){
    files=`ls file/*.xml`
    count=0
    number=3
    for file in $files
    do
        count=$((count + 1))
        args=`cut -d' ' -f2 property.txt`
        python3 MySQL.py $args $file &
        if [ $count -eq $number ]
        then
            wait
            count=0
        fi
    done
}

if [ $1 = "split" ]
then
    split $2
elif [ $1 = "mysql" ]
then
    mysql
fi
