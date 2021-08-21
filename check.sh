black -l 80 -t py38 --skip-string-normalization .
pylint $(git ls-files '*.py') 