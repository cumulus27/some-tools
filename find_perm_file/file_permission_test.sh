#!/usr/bin/env bash
# Find the file with given permission.

# exec 1>result.txt
# exec 2>error.txt

user="u"
perm="w"
path="."
head=""
number=""
result_path=data

while getopts ugorwxsp:aln: opt
do
   case "$opt" in
      u) user="u" ;;
      g) user="g" ;;
      o) user="o" ;;
      r) perm="r" ;;
      w) perm="w" ;;
      x) perm="x" ;;
      s) perm="s" ;;
      a) head="adb shell" ;;
      l) head="" ;;
      p) path=$OPTARG ;;
      n) number=$OPTARG ;;
      *) echo "Unknown option: $opt" >&2 ;;
   esac
done

# Check the exist of result path.
if [[ ! -e ${result_path} ]]
then
    mkdir -p ${result_path}
fi

# Check the adb connect.
if [[ -n ${number} ]]
then
    adb=`adb devices`
    echo ${adb}
fi

# Run the command.
if [[ -z ${number} ]]
then
    echo "Set user: $user, permission: $perm, Set path: $path"
    ${head}find ${path} -type f -perm /${user}=${perm} -exec ls -l {} 2>${result_path}/error_${user}${perm}.txt 1>${result_path}/result_${user}${perm}.txt \;
    echo "Run command finished, see result in ${result_path}/result_${user}${perm}.txt"
else
    echo "Set permission: $number, Set path: $path"
    ${head}find ${path} -type f -perm ${number} -exec ls -l {} 2>${result_path}/error_${number}.txt 1>${result_path}/result_${number}.txt \;
    echo "Run command finished, see result in ${result_path}/result_${number}.txt"
fi

