#!/bin/bash

mkdir hyphenation-rules
cd hyphenation-rules
curl https://codeload.github.com/hyphenation/tex-hyphen/tar.gz/master | tar -xz --strip=2 --strip-components 7 tex-hyphen-master/hyph-utf8/tex/generic/hyph-utf8/patterns/txt
echo "https://web.archive.org/web/20221005181751/http://www.hyphenation.org/tex" > LICENSES.txt