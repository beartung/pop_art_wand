PALETTES=`ls palette`
for p in $PALETTES
do
    pid=`echo $p|sed 's/.palette//'`
    outfile="dd/dd-$pid.jpg"
    if [ -f $outfile ]
    then
        echo "$outfile already exists!"
    else
        echo ./pop_art palette/$p test/dd.jpg $outfile
        ./pop_art palette/$p test/dd.jpg dd/dd-$pid.jpg
    fi
done
