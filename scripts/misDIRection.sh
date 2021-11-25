secret=$(for i in $(unzip -P hackthebox misDIRection.zip | grep extracting|\
        cut -d ":" -f2|sort -t/ -k 3,3 -n);do echo "$i"| \
        cut -d"/" -f2|xargs echo -n;done)

# print the flag
echo "$secret" | base64 -d
echo ""