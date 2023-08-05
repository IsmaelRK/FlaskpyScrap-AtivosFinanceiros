# The 'main selector' or 'main url' must be completed with the url and the css selector from the page
# It isn't completed because of copywright

from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ind = 0
        tempvar = ''
        ac_list = []
        ac_list2 = []
        ac_list3 = []
        ac_listNF = []
        fii_Search = request.form["fii_Search"].lower().replace(' ', '')
        results = []
        results_AC = []
        results_ETF = []

        def scrapy(url, selector):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'DNT': '1',
                'Connection': 'close'
            }

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            value = soup.select_one(selector).text.strip()

            return value

        cont = 0
        for x in fii_Search:

            if x.isalpha():
                tempvar += x
                if len(tempvar) > 4:
                    ac_list.append(tempvar[0:4])
                    tempvar = tempvar[4]

            else:
                if int(x) != 1:
                    tempvar += x
                    ac_list.append(tempvar)
                    tempvar = ''
                    cont = 0

                elif int(x) == 1:
                    tempvar += x

                    if cont == 1:
                        ac_list.append(tempvar)
                        tempvar = ''
                        cont = 0

                    if len(tempvar) > 0:
                        cont = 1

        ac_list_Len = len(ac_list)

        def while_Scrap_FII(ind_Start):
            try:
                while ac_list_Len > ind_Start:
                    main_Url = "" + ac_list[ind_Start]
                    main_Selector = ""
                    prc = scrapy(main_Url, main_Selector)

                    main_Url2 = "" + ac_list[ind_Start]
                    main_Selector2 = ""
                    prc_Patr = scrapy(main_Url2, main_Selector2)

                    prc = prc.replace(',', '.')
                    prc_Patr = prc_Patr.replace(',', '.')

                    vvp = float(prc) / float(prc_Patr)
                    vvp = round(vvp, 2)

                    main_Selector3 = ""
                    yld1m = scrapy(main_Url, main_Selector3)

                    main_Selector4 = ""
                    yld12m = scrapy(main_Url, main_Selector4)

                    main_Selector5 = ""
                    last_R = scrapy(main_Url, main_Selector5)

                    print(ac_list[ind_Start])
                    program_Results = [ac_list[ind_Start], prc, prc_Patr, vvp, yld1m, yld12m, last_R]
                    results.append(program_Results)
                    ind_Start += 1
            except:
                ac_list2.append(ac_list[ind_Start])
                ind_Start += 1
                while_Scrap_FII(ind_Start)

        def while_Scrap_AC(ind_Start):
            try:
                while len(ac_list2) > ind_Start:
                    main_Url = "" + ac_list2[ind_Start]
                    print(ac_list2[ind_Start])
                    main_Selector = ""
                    prc = scrapy(main_Url, main_Selector)

                    main_Selector2 = ""
                    val_1M = scrapy(main_Url, main_Selector2)

                    # prc = prc.replace(',', '.')

                    main_Selector3 = ""
                    perc_Yld12 = scrapy(main_Url, main_Selector3)

                    main_Selector4 = ""
                    yld12m = scrapy(main_Url, main_Selector4)

                    main_Selector5 = ""
                    vvp = scrapy(main_Url, main_Selector5)

                    main_Selector6 = ""
                    val_12M = scrapy(main_Url, main_Selector6)

                    main_Selector7 = ""
                    min_52W = scrapy(main_Url, main_Selector7)

                    main_Selector8 = ""
                    min_1M = scrapy(main_Url, main_Selector8)

                    main_Selector9 = ""
                    max_52W = scrapy(main_Url, main_Selector9)

                    main_Selector10 = ""
                    max_1M = scrapy(main_Url, main_Selector10)

                    program_Results = [ac_list2[ind_Start], prc, min_52W, min_1M, max_52W, max_1M, perc_Yld12, yld12m,
                                       val_12M, val_1M, vvp]
                    results_AC.append(program_Results)

                    ind_Start += 1

            except:
                ac_list3.append(ac_list2[ind_Start])
                ind_Start += 1
                while_Scrap_AC(ind_Start)





        def while_Scrap_ETF(ind_Start):
            try:
                while len(ac_list3) > ind_Start:
                    main_Url = "" + ac_list3[ind_Start]
                    print(ac_list3[ind_Start])

                    main_Selector = ""
                    prc = scrapy(main_Url, main_Selector)

                    main_Selector2 = ""
                    min_52W = scrapy(main_Url, main_Selector2)

                    # prc = prc.replace(',', '.')

                    main_Selector3 = ""
                    min_1M = scrapy(main_Url, main_Selector3)

                    main_Selector4 = ""
                    max_52W = scrapy(main_Url, main_Selector4)

                    main_Selector5 = ""
                    max_1M = scrapy(main_Url, main_Selector5)

                    main_Selector6 = ""
                    val_12M = scrapy(main_Url, main_Selector6)

                    main_Selector7 = ""
                    val_1M = scrapy(main_Url, main_Selector7)

                    program_Results = [ac_list3[ind_Start], prc, min_52W, min_1M, max_52W, max_1M, val_12M, val_1M]
                    results_ETF.append(program_Results)
                    ind_Start += 1
            except:
                ac_listNF.append(ac_list3[ind_Start])
                ind_Start += 1
                while_Scrap_ETF(ind_Start)


        while_Scrap_FII(ind)
        while_Scrap_AC(ind)
        while_Scrap_ETF(ind)


        print('-------------------------------------')
        print()
        print(results)
        print(results_AC)
        print(results_ETF)
        print(ac_listNF)
        print()
        print('-------------------------------------')
        return render_template('index.html', results=results, results_AC=results_AC, results_ETF=results_ETF, ac_listNF=ac_listNF, n_elmnts=ac_list_Len)

    return render_template('index.html', n_elmnts=1)


if __name__ == '__main__':
    app.run()
