IF EXIST conf_local.py (
  docker run -it --rm -v %cd%\conf_local.py:/app/conf_local.py pytoot
) ELSE (
  docker run -it --rm pytoot
)
