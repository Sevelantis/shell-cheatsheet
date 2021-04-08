#!/bin/bash -eu

# ----Laborki nr 2----
# 3.0: Napisać skrypt, który przyjmuje 2 parametry – 2 ścieżki do katalogów.

DIR_NOT_FOUND=2
INVALID_ARGUMENT=22

if [[ $# -ne 2 ]]; then # 2 arguments must be provided! 
    echo "2 arguments must be provided in order to make script do its job!!!"
    exit INVALID_ARGUMENT
fi

DIR1=${1}
DIR2=${2}

if [[ ! -d ${DIR1} || ! -d ${DIR2} ]]; then
    echo "At least one of directories is not present: ${DIR1}, ${DIR2}"
    exit DIR_NOT_FOUND
fi

# cleenup - uncomment when needed
# rm -r $DIR2/*

for ITEM in $(ls ${DIR1}); do
    FILE="${DIR1}/${ITEM}"

    echo ${FILE}
    if [[ -d ${FILE} || -f ${FILE} ]]; then
        if [[ -d ${FILE} ]]; then   # dir
            echo "-dir"

            # parallel cp to DIR2 via symlincc
            file=${FILE#*/}
            file=${file%.*}

            ln -s ${PWD}/${FILE} "${DIR2}/${file}_ln"
        fi
        if [[ -f ${FILE} ]]; then
            echo "-regfile"        # regfile

            # parallel cp to DIR2 via symlincc
            file=${FILE#*/}
            file=${file%.*}
            ext=${FILE#*.}
            
            ln -s ${PWD}/${FILE} "${DIR2}/${file}_ln.${ext}"
        fi  
    fi
    
    if [[ -d ${FILE} ]]; then
        echo "-symlink"
    fi
done

# +0.5 - Napisać skrypt, który w zadanym katalogu (1. parametr) usunie wszystkie uszkodzone dowiązania symboliczne, a ich nazwy wpisze do pliku (2. parametr), wraz z dzisiejszą datą w formacie ISO 8601.

DATE=$(date +"%Y-%m-%d") # today RRRR-MM-DD
for ITEM in $(ls ${DIR1}); do
    FILE="${DIR1}/${ITEM}"
    if [[ ! -e ${FILE} ]]; then # corrupted symbolic links
        rm ${FILE}
        touch "${DIR2}/${DATE}_${ITEM}"
    fi
done

# +1.0 - Napisać skrypt, który w zadanym katalogu (jako parametr) każdemu:
for ITEM in $(ls ${DIR1}); do
    FILE="${DIR1}/${ITEM}"
    ext=${ITEM##*.}
    # filename=${FILE##*/}
    if [[ ${ext} == "bak" ]]; then
        # - plikowi regularnemu z rozszerzeniem .bak odbierze uprawnienia do edytowania dla właściciela i innych
        if [[ -f ${FILE} ]]; then
            chmod uo-w ${FILE}
        fi
        
        # - katalogowi z rozszerzeniem .bak (bo można!) pozwoli wchodzić do środka tylko innym
        if [[ -d ${FILE} ]]; then
            chmod o+x,ug-x ${FILE}
        fi

    # - w katalogach z rozszerzeniem .tmp pozwoli każdemu tworzyć i usuwać jego pliki
    elif [[ ${ext} == "tmp" ]]; then
        if [[ -d {$FILE} ]]; then
            chmod a+rw ${FILE}
        fi

    # - plikowi z rozszerzeniem .txt będą czytać tylko właściciele, edytować grupa właścicieli, wykonywać inni. Brak innych uprawnień
    elif [[ ${ext} == "txt" ]]; then
        chmod u=r,g=w,o=x ${FILE}

    # - pliki regularne z rozszerzeniem .exe wykonywać będą mogli wszyscy, ale zawsze wykonają się z uprawnieniami właściciela (można przetestować na skompilowanym https://github.com/szandala/SO2/blob/master/lab2/suid.c)
    elif [[ ${ext} == exe ]]; then
        if [[ -f ${FILE} ]]; then
            chmod a+s ${FILE}   # setuid bit
        fi
    fi
done

#reszta zadania w pliku .env