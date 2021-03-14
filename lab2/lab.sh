#!/bin/bash

# -------------------------------------
# Systemy Operacyjne 2 - Laboratorium 2
# Miron Oskroba
# -------------------------------------

###
DFLT1="lab_uno"
DFLT2="2remove" # 'nie ma spacji w zadnych nazwach'
DFLT3="bakap"

# przypisz wartosc default lub wartosc odpowiedniego argumentu
SOURCE_DIR="${1:-${DFLT1}}"
RM_LIST="${SOURCE_DIR}/${2:-${DFLT2}}"
TARGET_DIR="${3:-${DFLT3}}"


###
# jesli nie istnieje katalog TARGET_DIR -> stworz go
if [[ ! -d ${TARGET_DIR} ]]; then
    mkdir ${TARGET_DIR}
    echo "Stworzono katalog '${TARGET_DIR}'."
fi

###
# jesli nie istnieje katalog SOURCE_DIR -> stworz go 
# oraz defaultowe pliki w nim - jeden bedzie usuniety, drugi nie
rm -r $SOURCE_DIR
if [[ ! -d ${SOURCE_DIR} ]]; then
    FILE1="${SOURCE_DIR}/file_to_be_removed_4"
    FILE2="${SOURCE_DIR}/file_not_to_be_removed_1"
    FILE3="${SOURCE_DIR}/directory_example_1"
    FILE4="${FILE3}/abc.d"

    mkdir ${SOURCE_DIR}
    touch "${FILE1}"
    touch "${FILE2}"
    mkdir "${FILE3}"
    touch "${FILE4}"

    echo "Stworzono katalog '${SOURCE_DIR}'."
    echo "Stworzono plik '${FILE1}'"
    echo "Stworzono plik '${FILE2}'"
    echo "Stworzono katalog '${FILE3}'"
    echo "Stworzono plik '${FILE4}'"


    ###
    # jesli nie istnieje plik RM_LIST -> stworz go i zainicjuj defaultowymi danymi
    if [[ ! -f ${RM_LIST} ]]; then
        echo "File not found!"
        touch "${RM_LIST}"
        for i in {1..4}; do
            echo "file_to_be_removed_$i" >> ${RM_LIST}
        done 
        echo "Stworzono plik '${RM_LIST}', wpisano do niego wartosci domyslne."
    fi
fi

echo -e "\nDrzewo przed usuwaniem:"
tree

###
# usuwanie plikow z listy pliku tekstowego, jezeli istnieja
for ITEM in $(cat ${RM_LIST}); do
    FILE="${SOURCE_DIR}/${ITEM}"

    if [[ -f ${FILE} ]]; then       # gdy plik istnieje w katalogu SOURCE_DIR
        rm ${FILE}                  # usun go
        echo "usuwanie pliku: ${FILE}"
    fi
done

### pliki ktorych nie ma na liscie:
# przenoszenie plikow z SOURCE_DIR do TARGET_DIR
for ITEM in $(ls ${SOURCE_DIR}); do # nie ma na liscie i:
    FILE="${SOURCE_DIR}/${ITEM}"

    if [[ -f ${FILE} ]]; then       # jest plikem
        mv ${FILE} ${TARGET_DIR}
        echo "Przenoszenie pliku: ${FILE} --> ${TARGET_DIR}"
    elif [[ -d ${FILE} ]]; then     # jest katalogiem
        cp -r "${FILE}/" "${TARGET_DIR}/"
        echo "Kopiowanie katalogu z zawartoscia: ${FILE} --> ${TARGET_DIR}"
    fi
done

echo -e "\nDrzewo po przenoszeniu:"
tree

###
# czy jeszcze cos zostalo? 
#       w przypadku katalogow, zostaly skopiowane, wiec wiadomo
#       ze i tak tam beda.
# katalog sie liczy jako 1.
echo -e "\n\n------------------------"
NR_OF_FILES=$(ls ${SOURCE_DIR} | wc -l)
if [[ ${NR_OF_FILES} -gt 0 ]]; then
    echo "jeszcze cos zostalo"
    
    if [[ ${NR_OF_FILES} -ge 2 ]]; then
        echo "zostaly co najmniej 2 pliki"

        if [[ ${NR_OF_FILES} -le 4 ]]; then 
            echo "zostalo plikow 2 lub 3 lub 4"
        fi
    fi

    if [[ ${NR_OF_FILES} -gt 4 ]];then
        echo "zostalo wiecej niz 4 pliki"
    fi

    else # nic nie zostalo
        echo "nic nie zostalo (tu byl Kononowicz)"
fi
echo -e "------------------------\n\n"

###
# obdbieranie praw do edycji plikom
for ITEM in $(ls ${TARGET_DIR}); do
    sudo chmod -R -w ${TARGET_DIR}/${ITEM} # rekursywnie '-R' dla wszystkich plikow
                                           # w podfolderach
done

echo -e "\nOdebrano prawo do edycji - 'w' "
ls -l ${TARGET_DIR}

###
# tworzenie pliku bakap_DATA.zip
# RRRR-MM-DD

DATE=$(date +"%Y-%m-%d") # today RRRR-MM-DD
ZIP_OUT="bakap_${DATE}.zip"
DIR_IN=${TARGET_DIR}

echo -e "\nGenerowanie pliku '${ZIP_OUT}'. Spakowano pliki z '${DIR_IN}'"

zip -r ${ZIP_OUT} ${DIR_IN}
