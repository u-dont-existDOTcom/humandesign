# ChineseAstro-11: independent Chinese official lunar-date parity (PROVISIONAL)

Root task OPEN. Isolated worktree from accepted source V9 and source-first partial Zi Wei mechanics branch b14cabf9e154b300f3b4ad4e15a551ce1ca52759. Chinese historical index remains **210 BaZi + 220 Zi Wei**, Western **13,044 Lilly +1,066 Ptolemy** unchanged.

Objective: compare two non-identical Chinese date-conversion implementations against immutable official Hong Kong Observatory lunar dates, preserving the distinction between Gregorian date, lunar-year boundary and solar-term Li Chun stem-year boundary. An independently calculated astronomical calendar across all historical regions/eras remains NOT proven. Do not feed local civil birth dates into a Hong Kong/Beijing lunar-date converter without an explicit time-zone/reference-calendar decision.

Official HKO doc: https://data.weather.gov.hk/weatherAPI/doc/HKO_Open_Data_API_Documentation.pdf ; official API: https://data.weather.gov.hk/weatherAPI/opendata/lunardate.php?date=YYYY-MM-DD ; official policy: https://www.hko.gov.hk/en/education/astronomy-and-time/time-service/00506-what-year-is-it-today.html .
Third party independent implementations: https://github.com/6tail/lunar-python and https://pypi.org/project/sxtwl/ ; installed in isolated /tmp only, no copies of libraries committed. Separate external software outputs are not evidence that Chinese astrology predicts human life.
