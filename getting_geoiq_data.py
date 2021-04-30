from csv import reader
import csv
import json as js
import requests

def get_geoiq_data(lat_long, radius, variable_list):
    # make geoiq call
    variable_list_string = ','.join(variable_list)
    lat = lat_long[1]
    longit = lat_long[0]
    
    body =  {
        "key": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtYWlsSWRlbnRpdHkiOiJhcnlhbl9zcml2YXN0YXZhQGJyb3duLmVkdSJ9.lXjdA4likjj5xKjV0hksrZFs3n_ndOdV0leIDCrf1wY",
        "lat": lat,
        "lng": longit,
        "variables": variable_list_string,
        "radius": radius
        }


    headers = {'Content-Type': 'application/json'}
    r = requests.post(url = "https://data.geoiq.io/dataapis/v3.0/datageoiq", data = js.dumps(body), headers = headers)

    return (js.loads(r.text)['data'])


def get_lat_long_tuples():
    with open('mumbai_lat_longs_400.csv','r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Pass reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)
        return list_of_rows


def main():
    RADIUS = 200

    variable_list = [
        'tot_hh',
        'tot_illt',
        'tot_lit',
        'tot_pop',
        'tot_sc',
        'tot_st',
        'tot_w',
        'w_hh_income_10l_above_perc',
        'w_hh_income_5l_above_perc',
        'w_hh_income_20l_above_perc',
        'w_pop_tt',
        'pop_age_0_18_perc',
        'pop_age_18_60_perc',
        'pop_age_60_above_perc',
        'pop_ratio_fm',
        'avail_assets_comp_intnt_perc',
        'avail_assets_comp_no_intnt_perc',
        'avail_assets_tele_mob_mob_only_perc',
        'avail_assets_tv_perc',
        'f_illt_perc',
        'f_l6_perc',
        'f_lit_perc',
        'f_pop_perc',
        'f_sc_perc',
        'f_st_perc',
        'f_w_perc',
        'hh_sz_1_perc',
        'hh_sz_2_perc',
        'hh_sz_3_perc',
        'hh_sz_4_perc',
        'hh_sz_5_perc',
        'hh_sz_6_8_perc',
        'hh_sz_9_plus_perc',
        'm_illt_perc',
        'm_lit_perc',
        'm_pop_perc',
        'm_sc_perc',
        'm_st_perc',
        'm_w_perc',
        'mrd_cpl_1_perc',
        'mrd_cpl_2_perc',
        'mrd_cpl_3_perc',
        'mrd_cpl_4_perc',
        'mrd_cpl_5_plus_perc',
        'mrd_cpl_none_perc',
        'tot_illt_perc',
        'tot_lit_perc',
        'tot_sc_perc',
        'tot_st_perc',
        'tot_w_perc']

    lat_longs_list = get_lat_long_tuples()[1:]

    csv_columns = ['lat', 'long'] + variable_list 

    count = 0

    with open("mumbai_data_200.csv", "w") as csvfile: 

        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()

        for lat_long in lat_longs_list:

            data = get_geoiq_data(lat_long, RADIUS, variable_list)
            if not data:
                continue
            data['lat'] = lat_long[1]
            data['long'] = lat_long[0]

            count += 1
            print(count)

            writer.writerow(data)



if __name__ == '__main__':
    main()