#loading packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.display.max_columns = 100
pd.options.display.max_rows = 100


def fetch_country_column(filename):
    '''
    Function to return the country and year feature datframes.
    '''
    data_year_column = pd.read_excel(filename,engine="openpyxl")
    data_test = pd.melt(data_year_column, id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
                    var_name='Year', value_name='Value')
    data_test = data_test.pivot_table(index=['Year', 'Country Code', 'Indicator Name', 'Indicator Code'], columns='Country Name', values='Value').reset_index()
    data_test = data_test.drop_duplicates().reset_index()
    return data_year_column,data_test


data_years_c,data_country_c = fetch_country_column('world_bank_climate.xlsx')


def years_data(data,s,e,s_y):
    df_sub = data.copy()
    years=[i for i in range(s,e,s_y)]
    col_need=['Country Name','Indicator Name']
    col_need.extend(years)
    df_sub =  df_sub[col_need]
    df_sub = df_sub.dropna(axis=0, how="any") 
    return df_sub


data_year_sample = years_data(data_years_c,1975,2020,5)


countries_to_keep = data_year_sample['Country Name'].value_counts().index.tolist()[5:15]



def colum_select_field(data,column,values):
    df_temp= data.copy()
    df_required= df_temp[df_temp[column].isin(values)].reset_index(drop=True)
    return df_required


df_keep_country  = colum_select_field(data_year_sample,'Country Name',countries_to_keep)



country_dict = dict()
for i in range(df_keep_country.shape[0]):
    if df_keep_country['Country Name'][i] not in country_dict.keys():
        country_dict[df_keep_country['Country Name'][i]]=[df_keep_country['Indicator Name'][i]]
    else:
        country_dict[df_keep_country['Country Name'][i]].append(df_keep_country['Indicator Name'][i])
    
    

for k,v in country_dict.items():
    country_dict[k] = set(v)


inter = country_dict['Canada']
for v in country_dict.values():
    inter = inter.intersection(v)


print(data_year_sample.describe())

df_year_cereal= colum_select_field(data_year_sample,'Indicator Name',['Cereal yield (kg per hectare)'])


print(df_year_cereal.describe())


df_year_cereal_cont  = colum_select_field(df_year_cereal,'Country Name',countries_to_keep)



def country_bar_plot(data,indicator_variable):
    data_test = data.copy()
    data_test.set_index('Country Name', inplace=True)
    col_numer = data_test.columns[data_test.dtypes == 'float64']
    data_numeric_test = data_test[col_numer]
    plt.figure(figsize=(60, 60))
    data_numeric_test.plot(kind='bar')
    plt.title(indicator_variable)
    plt.xlabel('Country Name')    
    plt.legend(title='Year', bbox_to_anchor=(1.15, 1), loc='upper left')
    plt.show()


country_bar_plot(df_year_cereal_cont,'Cereal yield (kg per hectare)')



df_year_agr= colum_select_field(data_year_sample,'Indicator Name',['Agricultural land (% of land area)'])
df_year_agr  = colum_select_field(df_year_agr,'Country Name',countries_to_keep)


print(df_year_agr.describe())



country_bar_plot(df_year_agr,'Agricultural land (% of land area)')



df_year_nd= colum_select_field(data_year_sample,'Country Name',['Netherlands'])



def ind_filt_data(data):
    data_s=data.copy()
    # Melt the DataFrame
    data_melted_sample = data_s.melt(id_vars='Indicator Name', var_name='Year', value_name='Value')

    # Pivot the DataFrame
    data_pivoted_sample = data_melted_sample.pivot(index='Year', columns='Indicator Name', values='Value')

    # Reset index
    data_pivoted_sample.reset_index(inplace=True)
    data_pivoted_sample = data_pivoted_sample.apply(pd.to_numeric, errors='coerce')
    del data_pivoted_sample['Year']
    data_pivoted_sample = data_pivoted_sample.rename_axis(None, axis=1)
    return data_pivoted_sample

    
    

data_heat_map_nd= ind_filt_data(df_year_nd)




features_to_verify = ['Cereal yield (kg per hectare)',
 'Agricultural land (% of land area)',
 'CO2 intensity (kg per kg of oil equivalent energy use)',
 'Energy use (kg of oil equivalent per capita)',
 'Arable land (% of land area)',
 'Urban population growth (annual %)']



data_heat_map_nd_map = data_heat_map_nd[features_to_verify]


print(data_heat_map_nd_map.corr())


sns.heatmap(data_heat_map_nd_map.corr(), annot=True, cmap='YlGnBu', linewidths=.5, fmt='.3g')



df_year_arable= colum_select_field(data_year_sample,'Indicator Name',['Arable land (% of land area)'])
df_year_arable  = colum_select_field(df_year_arable,'Country Name',countries_to_keep)


print(df_year_arable.describe())



df_year_col_urban= colum_select_field(data_year_sample,'Indicator Name',['Urban population (% of total population)'])
df_year_col_urban  = colum_select_field(df_year_col_urban,'Country Name',countries_to_keep)



def plot_for_year(data,indicator_value):
    data_sample = data.copy()
    data_sample.set_index('Country Name', inplace=True)
    numerical_req = data_sample.columns[data_sample.dtypes == 'float64']
    df_numerical_req = data_sample[numerical_req]

    plt.figure(figsize=(12, 8))
    for count in df_numerical_req.index:
        plt.plot(df_numerical_req.columns, df_numerical_req.loc[count], label=count, linestyle='dashed', marker='o')

    plt.title(indicator_value)
    plt.xlabel('Year')
    plt.legend(title='Country', bbox_to_anchor=(1.20, 1), loc='upper left')

    plt.show()


plot_for_year(df_year_arable,'Arable land (% of land area)')



df_year_co2= colum_select_field(data_year_sample,'Indicator Name',['CO2 intensity (kg per kg of oil equivalent energy use)'])
df_year_co2 = colum_select_field(df_year_co2,'Country Name',countries_to_keep)


print(df_year_co2.describe())



plot_for_year(df_year_co2,'CO2 intensity (kg per kg of oil equivalent energy use)')




df_year_col_pol = colum_select_field(data_year_sample,'Country Name',['Poland'])
data_heat_map_pol = ind_filt_data(df_year_col_pol)
data_heat_map_pol_sub = data_heat_map_pol[features_to_verify]
sns.heatmap(data_heat_map_pol_sub.corr(), annot=True, cmap='YlGnBu', linewidths=.6, fmt='.4g')



df_year_col_swe= colum_select_field(data_year_sample,'Country Name',['Hungary'])
data_heat_map_swe = ind_filt_data(df_year_col_swe)
data_heat_map_swe_sub = data_heat_map_swe[features_to_verify]
sns.heatmap(data_heat_map_swe_sub.corr(), annot=True, cmap='YlGnBu', linewidths=.5, fmt='.3g')





