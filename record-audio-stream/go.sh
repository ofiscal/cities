url=$1

streamripper $url -a --debug \
  > "streamripper_log_$(date +\"%m-%d-%y-%T\")"

