from sklearn.preprocessing import MinMaxScaler
import ast


scaler = MinMaxScaler()


def extract_metrics(df):
    extracted_insights = []
    for i, insight in enumerate(df['data']):
        if type(insight)!=list:
            insight = ast.literal_eval(insight)
        
        engagement_value = 0
        impression_value = 0
        reach_value = 0
        saved_value = 0
        plays_value = 0
        shares_value = 0
        total_interactions_value = 0
        for metric in insight:
            # engagement
            if metric['name'] == 'engagement':
                engagement_value = metric['values'][0]['value']
            # impressions
            if metric['name'] == 'impressions':
                impression_value = metric['values'][0]['value']

            # reach
            if metric['name'] == 'reach':
                reach_value = metric['values'][0]['value']
            # saved
            if metric['name'] == 'saved':
                saved_value = metric['values'][0]['value']
            # plays
            try:
                if metric['name'] == 'plays':
                    plays_value = metric['values'][0]['value']
            except KeyError:
                    plays_value = 0
            # shares
            try:
                if metric['name'] == 'shares':
                    shares_value = metric['values'][0]['value']
            except KeyError:
                    shares_value = 0
            # total interactions
            try:
                if metric['name'] == 'total_interactions':
                    total_interactions_value = metric['values'][0]['value']
            except KeyError:
                    total_interactions_value = 0  
        data = (
                df['id'][i], engagement_value, 
                impression_value, reach_value, saved_value, 
                plays_value, shares_value, total_interactions_value
            )
        extracted_insights.append(data)
    return extracted_insights


def aggregate_by_product(df, column_targets, based_on='produk_1'):
    agg_df = df.groupby(based_on, as_index=False)[column_targets].sum()
    if based_on != 'produk':
        try:
            agg_df = agg_df.rename(columns={based_on: 'produk'})
        except KeyError:
            return agg_df
    return agg_df


def casting_int(x):
    x = str(x)
    if ',' in x:
        return int(x.replace(',', '_'))
    return int(x)


def data_scaling(df, col_name_list):
    df[col_name_list] = scaler.fit_transform(df[col_name_list])
    print(df)
    return df
