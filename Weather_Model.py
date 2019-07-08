from Arima import *


class ProcessData:
    def __init__(self, dataa, predict_yearr, data_type):
        self.data = dataa
        self.predict_year = predict_yearr
        self.data_type = data_type

def process_minmax(self):
    if self.data_type == 'max':
        max_data = self.data['tmax']
    elif self.data_type == 'min':
        max_data = self.data['tmin']

    data_year = self.data['date']
    begin_year = data_year[0:1].dt.year
    end_year = data_year[-1:].dt.year

    predict_month = data_year[0:1].dt.month
    predict_day = data_year[0:1].dt.day

    # convert to 1D array

    max_data = pd.Series(max_data)
    max_data.index = pd.Index(sm.tsa.datetools.dates_from_range(str(begin_year.values[0]), str(end_year.values[0])))

    Arma_mod39 = sm.tsa.ARMA(max_data,(0,4)).fit()
    predict_end_year = end_year.values[0]+self.predict_year
    predict_dta = Arma_mod39.predict(str(end_year.values[0]), str(predict_end_year), dynamic=True)

    print('**********************************************')
    print(predict_dta)

    predict_dta.to_json(self.data_type+'.json', date_format='iso')
    json_date = fjd.format_json(self.data_type+'.json', str(predict_month.values[0]), str(predict_day.values[0]))

    print(json_date)

    fig, ax = plt.subplots(figsize=(12,8))
    ax = max_data.ix[str(begin_year.values[0]):].plot(ax=ax)
    Arma_mod39.plot_predict(str(end_year.values[0]),str(predict_end_year), dynamic=True, ax=ax, plot_insample=False)

    plt.show()
    plt.savefig(self.data_type+'.png',dpi=100)

    #send file

    send=SendFile(fileName=self.data_type+'.png')
    send.send()