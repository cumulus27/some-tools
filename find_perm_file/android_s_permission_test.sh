#!/usr/bin/env bash
# Find the file with given permission in android.

file_path=data/file_list
result_path=data/result

read=0
find=0

while getopts rf opt
do
   case "$opt" in
      r) read=1 ;;
      f) find=1 ;;
      *) echo "Unknown option: $opt" >&2 ;;
   esac
done

# Check the adb status.
adb=`adb devices`
echo ${adb}

# Get the phone id.
phone_id=None
for word in ${adb}
do
#    echo ${word}
    if [[ flag -eq 1 ]]
    then
        phone_id=${word}
        break
    fi

    if [[ ${word} = attached ]]
    then
        flag=1
    fi
done

echo ${phone_id}

if [[ read -eq 1 ]]
then
    # Check the exist of file path.
    if [[ ! -e ${file_path} ]]
    then
        mkdir -p ${file_path}
    fi

    # Pull the file list
    echo "Start to pull file list..."
    adb shell 'ls -l -R' 2>${file_path}/error_${phone_id}.txt 1>${file_path}/result_${phone_id}.txt
fi

if [[ find -eq 1 ]]
then
    # Check the exist of result path.
    if [[ ! -e ${result_path} ]]
    then
        mkdir -p ${result_path}
    fi

    # Find the given permission
    echo "Start to find the given permission"
    grep "[r-][w-][sStT][r-][w-].[r-][w-]." ${file_path}/result_${phone_id}.txt 2>${result_path}/error_${phone_id}.txt 1>${result_path}/result_${phone_id}.txt
fi
