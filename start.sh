
for com in py python python3; do
    if ! command -v $com &> /dev/null; then
        # echo "$com not found"
        continue
    else
        # echo "$com found"
        if ! $com -m pip list | grep -F pygame &> /dev/null; then
            # echo "pygame not found under $com"
            PYTHONFOUND="$com"
        else
            # echo "pygame found under $com"
            FOUND="$com"
            break
        fi
    fi 
done

if [[ -v FOUND ]]; then
    $FOUND ./game_files/client.py
else
    if [[ -v PYTHONFOUND ]]; then
        while true; do
            read -p "Pygame could not be found but you have python installed. Do you want to install pygame? (y/n)" yn

            case $yn in
                [yY] ) $PYTHONFOUND -m pip install pygame; $PYTHONFOUND ./game_files/client.py; exit;;
                [nN] ) exit;;
                * ) echo "Invalid response";;
            esac
        done
    else
        echo "Neither python or pygame could be found. Once python is installed, run this script again to automatically install pygame."
    fi
fi

exit