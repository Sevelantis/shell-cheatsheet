#!/bin/bash -eu

function print_help () {
    echo "This script allows to search over movies database"
    echo -e "-d DIRECTORY\n\tDirectory with files describing movies"
    echo -e "-a ACTOR\n\tSearch movies that this ACTOR played in"
    echo -e "-t QUERY\n\tSearch movies with given QUERY in title"
    echo -e "-f FILENAME\n\tSaves results to file (default: results.txt)"
    echo -e "-x\n\tPrints results in XML format"
    echo -e "-y\n\tPrints all movies newer than argument given as YEAR"
    echo -e "-h\n\tPrints this help message"
}

function print_error () 
{
    echo -e "\e[31m\033[1m""${*}""\033[0m" >&2
}

function get_movies_list () {
    local -r MOVIES_DIR=${1}
    local -r MOVIES_LIST=$(cd "${MOVIES_DIR}" && realpath ./*)
    echo "${MOVIES_LIST}"
}

function query_title () {
    # Returns list of movies from ${1} with ${2} in title slot
    local -r MOVIES_LIST=${1}
    local -r QUERY=${2}

    local RESULTS_LIST=()
    for MOVIE_FILE in ${MOVIES_LIST}; do
        if grep "| Title" "${MOVIE_FILE}" | grep -q "${QUERY}"; then
            RESULTS_LIST+=("${MOVIE_FILE}")
        fi
    done
    echo "${RESULTS_LIST[@]:-}"
}

function query_actor () {
    # Returns list of movies from ${1} with ${2} in actor slot
    local -r MOVIES_LIST=${1}
    local -r QUERY=${2}

    local RESULTS_LIST=()
    for MOVIE_FILE in ${MOVIES_LIST}; do
        if grep "| Actors" "${MOVIE_FILE}" | grep -q "${QUERY}"; then
            RESULTS_LIST+=("${MOVIE_FILE}")
        fi
    done
    echo "${RESULTS_LIST[@]:-}"
}

function query_year()
{
    # Returns list of movies from ${1} with ${2} in actor slot
    local -r MOVIES_LIST=${1}
    local -r YEAR_ARG=${2}

    local RESULTS_LIST=()
    
    for MOVIE_FILE in ${MOVIES_LIST}; do

        YEAR_FILE=$(grep "| Year" "${MOVIE_FILE}" | grep -Po "([0-9]){4}")

        if [[ ${YEAR_FILE} -gt ${YEAR_ARG} ]]; then
            RESULTS_LIST+=("${MOVIE_FILE}")
        fi

    done

    echo "${RESULTS_LIST[@]:-}"
}

function query_regex() {
    local -r MOVIES_LIST=${1}
    local -r QUERY=${2}

    local RESULTS_LIST=()

    if [[ "${IGNORE_LETTERCASE}" = true ]]; then
        for MOVIE_FILE in ${MOVIES_LIST}; do
            if grep "| Plot" "${MOVIE_FILE}" | grep -Pqi "${QUERY}"; then
                RESULTS_LIST+=("${MOVIE_FILE}")
            fi
        done
    else
        for MOVIE_FILE in ${MOVIES_LIST}; do
            if grep "| Plot" "${MOVIE_FILE}" | grep -Pq "${QUERY}"; then
                RESULTS_LIST+=("${MOVIE_FILE}")
            fi
        done
    fi

    echo "${RESULTS_LIST[@]:-}"
}

function print_xml_format (){
    local -r FILENAME=${1}

    local TEMP
    TEMP=$(cat "${FILENAME}")

    # kolejnosc wykonywanych komend ma znaczenie (zwla)
    # change others too
    TEMP=$(echo "${TEMP}" | sed -r 's/\| (.+): /<\1>/g')

    # append tag after each line
    TEMP=$(echo "${TEMP}" | sed -r 's/([A-Za-z]+).*/\0<\/\1>/')

    # change 'Author:' into <Author>
    TEMP="${TEMP//Author:/<Author>}"

    # replace the last line with </movie>
    TEMP=$(echo "${TEMP}" | sed '$s/===*/<\/movie>/')

    # replace first line of equals signs
    TEMP=$(echo "${TEMP}" | sed "s/===*/<movie>/1")

    echo "${TEMP}"
}

function print_movies () {
    local -r MOVIES_LIST=${1}
    local -r OUTPUT_FORMAT=${2}

    for MOVIE_FILE in ${MOVIES_LIST}; do
        if [[ "${OUTPUT_FORMAT}" == "xml" ]]; then
            print_xml_format "${MOVIE_FILE}"
        else
            cat "${MOVIE_FILE}"
        fi
    done
}


# exit codes
NOT_A_DIRECTORY=20
INVALID_ARGUMENT=22
# variables
ANY_ERRORS=false
IGNORE_LETTERCASE=false
DIR_CHECKED=false

while getopts ":hd:t:a:f:xiy:R:" OPT; do
  case ${OPT} in
    h)
        print_help
        exit ${NOT_A_DIRECTORY}
        ;;
    d)
        MOVIES_DIR=${OPTARG}
        if [[ ! -d ${MOVIES_DIR} ]];then
            echo "File ${MOVIES_DIR} is not a directory!"
            exit ${NOT_A_DIRECTORY}
        fi
        MOVIES_LIST=$(get_movies_list "${MOVIES_DIR}")
        
        DIR_CHECKED=true
        ;;
    t)
        SEARCHING_TITLE=true
        QUERY_TITLE=${OPTARG}
        ;;
    f)
        FILE_4_SAVING_RESULTS=${OPTARG}

        # + 0.5: Dotyczy opcji ‘-f’: jeżeli plik podany przez użytkownika nie posiada rozszerzenia '.txt' dodaj je
        if [[ ${FILE_4_SAVING_RESULTS: -4} != '.txt' ]]; then
            mv "${FILE_4_SAVING_RESULTS}" "${FILE_4_SAVING_RESULTS}"".txt"
            FILE_4_SAVING_RESULTS+='.txt'
        fi
        ;;
    a)
        SEARCHING_ACTOR=true
        QUERY_ACTOR=${OPTARG}
        ;;
    x)
        OUTPUT_FORMAT="xml"
        ;;

    #+ 1.0: Dodaj opcję -y ROK: wyszuka wszystkie filmy nowsze niż ROK. Pamiętaj o dodaniu opisu do -h
    y)
        SEARCHING_YEAR=true
        QUERY_YEAR=${OPTARG}
        ;;

    #+ 1.0: Dodaj wyszukiwanie po polu z fabułą, za pomocą wyrażenia regularnego. Np. -R 'Cap.*Amer' Jeżeli dodatkowo podamy parametr '-i' to ignoruje wielkość liter
    R) 
        SEARCHING_REGEX=true
        QUERY_REGEX=${OPTARG}
        ;;
    i)
        IGNORE_LETTERCASE=true
        ;;
    \?)
        print_error "ERROR: Invalid option: -${OPTARG}"
        ANY_ERRORS=true
        exit 1
        ;;
  esac
done

#+ 0.5: Dodaj sprawdzenie, czy na pewno wykorzystano opcję '-d' i czy jest to katalog
if [[ ${DIR_CHECKED} = false ]]; then
    echo "parametr '-d' niesprecyzowany!"
    exit ${INVALID_ARGUMENT}
fi

if ${SEARCHING_TITLE:-false}; then
    MOVIES_LIST=$(query_title "${MOVIES_LIST}" "${QUERY_TITLE}")
fi

if ${SEARCHING_ACTOR:-false}; then
    MOVIES_LIST=$(query_actor "${MOVIES_LIST}" "${QUERY_ACTOR}")
fi

if ${SEARCHING_REGEX:-false}; then
    MOVIES_LIST=$(query_regex "${MOVIES_LIST}" "${QUERY_REGEX}")
fi

if ${SEARCHING_YEAR:-false}; then
    MOVIES_LIST=$(query_year "${MOVIES_LIST}" "${QUERY_YEAR}")
fi

if [[ ${ANY_ERRORS} = true ]]; then
    echo "Arguments errors"
fi

if [[ "${#MOVIES_LIST}" -lt 1 ]]; then
    echo "Found 0 movies :-("
    exit 0
fi

if [[ "${FILE_4_SAVING_RESULTS:-}" == "" ]]; then
    print_movies "${MOVIES_LIST}" "${OUTPUT_FORMAT:-raw}"
else
    # TODO: add XML option
    print_movies "${MOVIES_LIST}" "raw" | tee "${FILE_4_SAVING_RESULTS}"
fi
