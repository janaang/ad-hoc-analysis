import json
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import dataframe_image as dfi

with open('transaction-data-adhoc-analysis.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data, columns = ['address', 'birthdate', 'mail', 'name', 'sex', 'username', 'transaction_items', 'transaction_value', 'transaction_date'])

modified_df =(df.set_index(['address','birthdate','mail','name','sex','username','transaction_value','transaction_date'])
.apply(lambda x: x.str.split(';').explode())
.reset_index())

month_as_number = modified_df['transaction_month'] = [x[7][6] for x in np.array(modified_df)]

def get_month(month_as_number):
    if month_as_number == '1':
        return 'January'
    elif month_as_number == '2':
        return 'February'
    elif month_as_number == '3':
        return 'March'
    elif month_as_number == '4':
        return 'April'
    elif month_as_number == '5':
        return 'May'
    elif month_as_number == '6':
        return 'June' 

modified_df['transaction_month'] = modified_df['transaction_month'].apply(get_month)

cond1 = modified_df['transaction_items'].str.contains('Beef Chicharon')
cond2 = modified_df['transaction_items'].str.contains('Kimchi and Seaweed')
cond3 = modified_df['transaction_items'].str.contains('Nutrional Milk')
cond4 = modified_df['transaction_items'].str.contains('Yummy Vegetables')
cond5 = modified_df['transaction_items'].str.contains('Gummy Vitamins')
cond6 = modified_df['transaction_items'].str.contains('Orange Beans')
cond7 = modified_df['transaction_items'].str.contains('Gummy Worms')

modified_df['beef_chicharon_order_qty'] = None
modified_df['beef_chicharon_order_qty']=np.where(cond1,modified_df.transaction_items,modified_df.beef_chicharon_order_qty)

modified_df['kimchi_and_seaweed_order_qty'] = None
modified_df['kimchi_and_seaweed_order_qty']=np.where(cond2,modified_df.transaction_items,modified_df.kimchi_and_seaweed_order_qty)

modified_df['nutrional_milk_order_qty'] = None
modified_df['nutrional_milk_order_qty']=np.where(cond3,modified_df.transaction_items,modified_df.nutrional_milk_order_qty)

modified_df['yummy_vegetables_order_qty'] = None
modified_df['yummy_vegetables_order_qty']=np.where(cond4,modified_df.transaction_items,modified_df.yummy_vegetables_order_qty)

modified_df['gummy_vitamins_order_qty'] = None
modified_df['gummy_vitamins_order_qty']=np.where(cond5,modified_df.transaction_items,modified_df.gummy_vitamins_order_qty)

modified_df['orange_beans_order_qty'] = None
modified_df['orange_beans_order_qty']=np.where(cond6,modified_df.transaction_items,modified_df.orange_beans_order_qty)

modified_df['gummy_worms_order_qty'] = None
modified_df['gummy_worms_order_qty']=np.where(cond7,modified_df.transaction_items,modified_df.gummy_worms_order_qty)

modified_df = modified_df.fillna(0)

modified_df['beef_chicharon_order_qty'] = modified_df['beef_chicharon_order_qty'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
modified_df['kimchi_and_seaweed_order_qty'] = modified_df['kimchi_and_seaweed_order_qty'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
modified_df['orange_beans_order_qty'] = modified_df['orange_beans_order_qty'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
modified_df['gummy_worms_order_qty'] = modified_df['gummy_worms_order_qty'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)

modified_df['nutrional_milk_order_qty'] = modified_df['nutrional_milk_order_qty'].str.findall('(\d+)').str[1]
modified_df['yummy_vegetables_order_qty'] = modified_df['yummy_vegetables_order_qty'].str.findall('(\d+)').str[1]
modified_df['gummy_vitamins_order_qty'] = modified_df['gummy_vitamins_order_qty'].str.findall('(\d+)').str[1]

modified_df = modified_df.fillna(0)

modified_df['nutrional_milk_order_qty'] = modified_df['nutrional_milk_order_qty'].astype(str).astype(int)
modified_df['yummy_vegetables_order_qty'] = modified_df['yummy_vegetables_order_qty'].astype(str).astype(int)
modified_df['gummy_vitamins_order_qty'] = modified_df['gummy_vitamins_order_qty'].astype(str).astype(int)

modified_df.groupby(['transaction_month'])[['beef_chicharon_order_qty', 'kimchi_and_seaweed_order_qty', 'nutrional_milk_order_qty', 'yummy_vegetables_order_qty', 'gummy_vitamins_order_qty', 'orange_beans_order_qty', 'gummy_worms_order_qty']].sum().reset_index()

#pivot table 1 - breakdown of count of each item/product per month
pivot = modified_df.pivot_table(index =['transaction_month'],
                       values =['beef_chicharon_order_qty', 'kimchi_and_seaweed_order_qty', 'nutrional_milk_order_qty', 'yummy_vegetables_order_qty', 'gummy_vitamins_order_qty', 'orange_beans_order_qty', 'gummy_worms_order_qty'],
                       aggfunc ='sum')

transaction_month = ['January', 'February', 'March', 'April', 'May', 'June']
pivot = pivot.reindex(transaction_month)
pivot

beef_chicharon_qty = modified_df['beef_chicharon_sale_value'] = [x[10] for x in np.array(modified_df)]

def get_beef_chicharon_revenue(beef_chicharon_qty):
    if beef_chicharon_qty != 0:
        return 1299*beef_chicharon_qty
    else:
        return 0 

modified_df['beef_chicharon_sale_value'] = modified_df['beef_chicharon_sale_value'].apply(get_beef_chicharon_revenue)

kimchi_and_seaweed_qty = modified_df['kimchi_and_seaweed_sale_value'] = [x[11] for x in np.array(modified_df)]

def get_kimchi_and_seaweed_revenue(kimchi_and_seaweed_qty):
    if kimchi_and_seaweed_qty != 0:
        return 799*kimchi_and_seaweed_qty
    else:
        return 0 

modified_df['kimchi_and_seaweed_sale_value'] = modified_df['kimchi_and_seaweed_sale_value'].apply(get_kimchi_and_seaweed_revenue)

nutrional_milk_qty = modified_df['nutrional_milk_sale_value'] = [x[12] for x in np.array(modified_df)]

def get_nutrional_milk_revenue(nutrional_milk_qty):
    if nutrional_milk_qty != 0:
        return 1990*nutrional_milk_qty
    else:
        return 0 

modified_df['nutrional_milk_sale_value'] = modified_df['nutrional_milk_sale_value'].apply(get_nutrional_milk_revenue)

yummy_vegetables_qty = modified_df['yummy_vegetables_sale_value'] = [x[13] for x in np.array(modified_df)]

def get_yummy_vegetables_revenue(yummy_vegetables_qty):
    if yummy_vegetables_qty != 0:
        return 500*yummy_vegetables_qty
    else:
        return 0 

modified_df['yummy_vegetables_sale_value'] = modified_df['yummy_vegetables_sale_value'].apply(get_yummy_vegetables_revenue)

gummy_vitamins_qty = modified_df['gummy_vitamins_sale_value'] = [x[14] for x in np.array(modified_df)]

def get_gummy_vitamins_revenue(gummy_vitamins_qty):
    if gummy_vitamins_qty != 0:
        return 1500*gummy_vitamins_qty
    else:
        return 0 

modified_df['gummy_vitamins_sale_value'] = modified_df['gummy_vitamins_sale_value'].apply(get_gummy_vitamins_revenue)

orange_beans_qty = modified_df['orange_beans_sale_value'] = [x[15] for x in np.array(modified_df)]

def get_orange_beans_revenue(orange_beans_qty):
    if orange_beans_qty != 0:
        return 199*orange_beans_qty
    else:
        return 0 

modified_df['orange_beans_sale_value'] = modified_df['orange_beans_sale_value'].apply(get_orange_beans_revenue)

gummy_worms_qty = modified_df['gummy_worms_sale_value'] = [x[16] for x in np.array(modified_df)]

def get_gummy_worms_revenue(gummy_worms_qty):
    if gummy_worms_qty != 0:
        return 150*gummy_worms_qty
    else:
        return 0 

modified_df['gummy_worms_sale_value'] = modified_df['gummy_worms_sale_value'].apply(get_gummy_worms_revenue)

#pivot 2 - breakdown of sale value of each item/product per month
pivot2 = modified_df.pivot_table(index =['transaction_month'],
                       values =['beef_chicharon_sale_value', 'kimchi_and_seaweed_sale_value', 'nutrional_milk_sale_value', 'yummy_vegetables_sale_value', 'gummy_vitamins_sale_value', 'orange_beans_sale_value', 'gummy_worms_sale_value'],
                       aggfunc ='sum')

column_names = ['beef_chicharon_sale_value', 'gummy_vitamins_sale_value', 'gummy_worms_sale_value', 'kimchi_and_seaweed_sale_value', 'nutrional_milk_sale_value', 'orange_beans_sale_value', 'yummy_vegetables_sale_value']
pivot2 = pivot2.reindex(columns=column_names)

transaction_month = ['January', 'February', 'March', 'April', 'May', 'June']
pivot2 = pivot2.reindex(transaction_month)
pivot2

customer_data_df = modified_df.groupby(['name', 'transaction_month'], as_index=False).first()
customer_data_df

array_agg = lambda x: '|'.join(x.astype(str))
customer_data_df = customer_data_df.groupby(['name']).agg({'transaction_month': array_agg})

for x in transaction_month:
    customer_data_df[x] = customer_data_df['transaction_month'].str.contains(x)

customer_data_df

separate_truth_table = customer_data_df.loc[:,transaction_month[0]:transaction_month[len(transaction_month)-1]]
separate_truth_table

for i, v in enumerate(transaction_month):
    if i == 0:
        repeater_customers = 0
        inactive_customers = 0
    else:
        repeater_rows = separate_truth_table.loc[(separate_truth_table[transaction_month[i]] == True) & (separate_truth_table[transaction_month[i-1]] == True)]
        repeater_customers = len(repeater_rows)
        
        january_to_current = separate_truth_table.loc[:, transaction_month[0]:v]
        currently_inactive = january_to_current.loc[(january_to_current[transaction_month[i]] == False)]
        atleast1true = list(currently_inactive.sum(axis = 1))
        inactive_customers = np.count_nonzero(atleast1true)
    
    january_to_current = separate_truth_table.loc[:, transaction_month[0]:v]
    currently_engaged = january_to_current.loc[(january_to_current[transaction_month[i]] == True)]
    all_columns = list(currently_engaged.sum(axis=1))
    engaged_customers = all_columns.count(i+1)
    
    print(v, ":", repeater_customers, "repeaters", inactive_customers, "inactive", engaged_customers, "engaged")    

#table 3 - repeater,inactive, engaged
customer_activity_data = {'January': [0,0, 6588],'February': [5172, 1416, 5172],'March': [5216, 1747, 4126], 'April': [5154, 1909, 3289], 'May': [5110, 1917, 2667], 'June': [5193, 1835, 2190]}
customer_activity_df = pd.DataFrame(customer_activity_data)
customer_activity_df.index = ['Repeater', 'Inactive', 'Engaged']
customer_activity_df

#deeper inights -- focus: sale stats 

##total qty of EACH product sold 
total_qty = pivot.sum()
df_total_qty = total_qty.rename_axis('Product').to_frame().reset_index()
df_total_qty.rename(columns={0: 'Total Count of Each Product Sold'}, inplace=True)
df_total_qty['Product'] = df_total_qty['Product'].replace(['beef_chicharon_order_qty','gummy_vitamins_order_qty', 'gummy_worms_order_qty', 'kimchi_and_seaweed_order_qty', 'nutrional_milk_order_qty', 'orange_beans_order_qty', 'yummy_vegetables_order_qty'],['Beef Chicharon','Gummy Vitamins', 'Gummy Worms', 'Kimchi and Seaweed', 'Nutrional Milk', 'Orange Beans', 'Yummy Vegetables'])
df_total_qty

#january to june
per_month = pivot.sum(axis = 1)
df_per_month = per_month.to_frame()
df_per_month = per_month.rename_axis('Transaction Month').to_frame().reset_index()
df_per_month.rename(columns={0: 'Total Count of All Products Sold'}, inplace=True)
df_per_month

plt.rcParams["figure.figsize"] = (10, 5)
plt.barh(y=df_total_qty['Product'], width=df_total_qty['Total Count of Each Product Sold'], color ='b')
plt.xlabel('Count')
plt.ylabel('Product')
plt.title('Total Count of Each Product Sold from January to June')
plt.xlim(58000, 60000)
matplotlib.rcParams.update({'font.size': 10})
plt.savefig("totalcount.jpg")
plt.show()

#total products sold per month
plt.rcParams["figure.figsize"] = (10, 5)
plt.plot(df_per_month['Transaction Month'],df_per_month['Total Count of All Products Sold'], 'r') #r is the color red
plt.xlabel('Transaction Month')
plt.ylabel('Count')
plt.title('Total Count of Products Sold Each Month')
plt.savefig("permonth.jpg")
matplotlib.rcParams.update({'font.size':10})
plt.show()

#sale value total codes
total_sale_value = pivot2.sum()
df_total_sale_value = total_sale_value.to_frame()
df_total_sale_value = total_sale_value.rename_axis('Product').to_frame().reset_index()
df_total_sale_value['Product'] = df_total_sale_value['Product'].replace(['beef_chicharon_sale_value','gummy_vitamins_sale_value', 'gummy_worms_sale_value', 'kimchi_and_seaweed_sale_value', 'nutrional_milk_sale_value', 'orange_beans_sale_value', 'yummy_vegetables_sale_value'],['Beef Chicharon','Gummy Vitamins', 'Gummy Worms', 'Kimchi and Seaweed', 'Nutrional Milk', 'Orange Beans', 'Yummy Vegetables'])
df_total_sale_value.rename(columns={0: 'Total Sale Value/Revenue Earned Per Product'}, inplace=True)
df_total_sale_value

sale_value_per_month = pivot2.sum(axis = 1)
df_sale_value_per_month = sale_value_per_month.to_frame()
df_sale_value_per_month = sale_value_per_month.rename_axis('Transaction Month').to_frame().reset_index()
df_sale_value_per_month.rename(columns={0: 'Total Sale Value/Revenue Earned Per Month'}, inplace=True)
df_sale_value_per_month

#graph of total revenue per product
plt.rcParams["figure.figsize"] = (10, 5)
plt.barh(y=df_total_sale_value['Product'], width=df_total_sale_value['Total Sale Value/Revenue Earned Per Product'], color ='b')
plt.xlabel('Revenue')
plt.ylabel('Product')
plt.title('Total Revenue Accumulated by Each Product from January to June')
plt.savefig("revenueeachitem.jpg")
plt.show()

#graph of total revenue per month
plt.rcParams["figure.figsize"] = (10, 5)
plt.plot(df_sale_value_per_month['Transaction Month'],df_sale_value_per_month['Total Sale Value/Revenue Earned Per Month'], 'r') #r is the color red
plt.xlabel('Transaction Month')
plt.ylabel('Revenue')
plt.title('Total Revenue Accumulated Each Month')
plt.savefig("revenueeachmonth.jpg")
plt.show()

#pivot  
plt.rcParams["figure.figsize"] = (16, 9)
pivot1_modified = pivot.rename_axis('Transaction Month').reset_index()
pivot1_modified.plot(x = 'Transaction Month', y=['beef_chicharon_order_qty','gummy_vitamins_order_qty', 'gummy_worms_order_qty', 'kimchi_and_seaweed_order_qty', 'nutrional_milk_order_qty', 'orange_beans_order_qty', 'yummy_vegetables_order_qty'], kind = 'bar', width = 0.7)
plt.ylim(9000, 10350)
plt.title('Breakdown of Count of Each Item Sold Per Month')
plt.savefig("countpermonth.jpg")
plt.show()

#pivot2 (sale value)
plt.rcParams["figure.figsize"] = (16, 9)
pivot2_modified = pivot2.rename_axis('Transaction Month').reset_index()
pivot2_modified.plot(x = 'Transaction Month', y=['beef_chicharon_sale_value','gummy_vitamins_sale_value', 'gummy_worms_sale_value', 'kimchi_and_seaweed_sale_value', 'nutrional_milk_sale_value', 'orange_beans_sale_value', 'yummy_vegetables_sale_value'], kind = 'line')
plt.title('Breakdown of the Total Sale Value per Item per Month')
plt.savefig("svpermonth.jpg")
plt.show()

#market segmentation by sex
customer_segmentation = modified_df.groupby(['name'], as_index=False).first()
customer_segmentation

print((customer_segmentation.sex == 'M').sum())
print((customer_segmentation.sex == 'F').sum())

customer_base = {4209, 4278}
customer_base = pd.DataFrame(customer_base)
customer_base['Sex'] = ['M', 'F']
customer_base.rename(columns={0: 'Total Count Within Customer Base'}, inplace=True)
customer_base[['Sex', 'Total Count Within Customer Base']]

customer_segmentation = modified_df.groupby(['name', 'transaction_month'], as_index=False).first()
breakdown_by_sex_per_month = customer_segmentation.groupby(["transaction_month", "sex"])["name"].count()
breakdown_by_sex_per_month

breakdown_by_sex_per_month = {'January': [3301,3287],'February': [3360, 3271],'March': [3314, 3308], 'April': [3318, 3238], 'May': [3293, 3275], 'June': [3335, 3317]}
breakdown_by_sex_per_month = pd.DataFrame(breakdown_by_sex_per_month)
breakdown_by_sex_per_month.index = ['F', 'M']
breakdown_by_sex_per_month

breakdown_by_sex_per_month2 = breakdown_by_sex_per_month.transpose()
breakdown_by_sex_per_month2 = breakdown_by_sex_per_month2.rename_axis('Transaction Month').reset_index()
breakdown_by_sex_per_month2

#overall customer base
sex_data = [4209, 4278]
label = ['M', 'F']
plt.rcParams["figure.figsize"] = (20, 9)
plt.pie(sex_data, labels=label, autopct='%1.1f%%', startangle=90)
plt.title('Customer Segmentation by Sex')
plt.savefig("customersegmentationbysex.jpg")
plt.show()

#breakdown each month
plt.rcParams["figure.figsize"] = (10, 5)
breakdown_by_sex_per_month2.plot(x = 'Transaction Month', y=['F','M'], kind = 'bar', width = 0.6)
plt.ylim(3000, 3500)
plt.title('Customer Segmentation by Sex Per Month')
plt.savefig("customersegmentationbysexpermonth.jpg")
plt.show()

#market segmentation by address
customer_segmentation_address = modified_df.groupby(['name'], as_index=False).first()

extract_state = customer_segmentation_address['state'] = [x[1][-8:-6] for x in np.array(customer_segmentation_address)]

def get_state(extract_state):
    if extract_state == 'AL':
        return 'Alabama'
    elif extract_state == 'AK':
        return 'Alaska'
    elif extract_state == 'AS':
        return 'American Samoa'
    elif extract_state == 'AZ':
        return 'Arizona'
    elif extract_state == 'AR':
        return 'Arkansas'
    elif extract_state == 'CA':
        return 'California'
    elif extract_state == 'CO':
        return 'Colorado'
    elif extract_state == 'CT':
        return 'Connecticut'
    elif extract_state == 'DE':
        return 'Delaware'
    elif extract_state == 'DC':
        return 'District of Columbia'
    elif extract_state == 'FM':
        return 'Federated States of Micronesia'
    elif extract_state == 'FL':
        return 'Florida'
    elif extract_state == 'GA':
        return 'Georgia'
    elif extract_state == 'GU':
        return 'Guam'
    elif extract_state == 'HI':
        return 'Hawaii'
    elif extract_state == 'ID':
        return 'Idaho'
    elif extract_state == 'IL':
        return 'Illinois'
    elif extract_state == 'IN':
        return 'Indiana'
    elif extract_state == 'IA':
        return 'Iowa'
    elif extract_state == 'KS':
        return 'Kansas'
    elif extract_state == 'KY':
        return 'Kentucky'
    elif extract_state == 'LA':
        return 'Louisiana'
    elif extract_state == 'ME':
        return 'Maine'
    elif extract_state == 'MH':
        return 'Marshall Islands'
    elif extract_state == 'MD':
        return 'Maryland'
    elif extract_state == 'MA':
        return 'Massachusetts'
    elif extract_state == 'MI':
        return 'Michigan'
    elif extract_state == 'MN':
        return 'Minnesota'
    elif extract_state == 'MS':
        return 'Mississipi'
    elif extract_state == 'MO':
        return 'Missouri'
    elif extract_state == 'MT':
        return 'Montana'
    elif extract_state == 'NE':
        return 'Nebraska'
    elif extract_state == 'NV':
        return 'Nevada'
    elif extract_state == 'NH':
        return 'New Hampshire'
    elif extract_state == 'NJ':
        return 'New Jersey'
    elif extract_state == 'NM':
        return 'New Mexico'
    elif extract_state == 'NY':
        return 'New York'
    elif extract_state == 'NC':
        return 'North Carolina'
    elif extract_state == 'ND':
        return 'North Dakota'
    elif extract_state == 'MP':
        return 'Northern Mariana Islands'
    elif extract_state == 'OH':
        return 'Ohio'
    elif extract_state == 'OK':
        return 'Oklahoma'
    elif extract_state == 'OR':
        return 'Oregon'
    elif extract_state == 'PA':
        return 'Pennsylvania'
    elif extract_state == 'PR':
        return 'Puerto Rico'
    elif extract_state == 'RI':
        return 'Rhode Island'
    elif extract_state == 'SC':
        return 'South Carolina'
    elif extract_state == 'SD':
        return 'South Dakota'
    elif extract_state == 'TN':
        return 'Tennessee'
    elif extract_state == 'TX':
        return 'Texas'
    elif extract_state == 'UT':
        return 'Utah'
    elif extract_state == 'VT':
        return 'Vermont'
    elif extract_state == 'VA':
        return 'Virginia'
    elif extract_state == 'VI':
        return 'Virgin Islands'
    elif extract_state == 'WA':
        return 'Washington'
    elif extract_state == 'WV':
        return 'West Virginia'
    elif extract_state == 'WI':
        return 'Wisconsin'
    elif extract_state == 'WY':
        return 'Wyoming'
    elif extract_state == 'AA':
        return 'Armed Forces the Americas'
    elif extract_state == 'AE':
        return 'Armed Forces Europe'
    elif extract_state == 'AP':
        return 'Armed Forces Pacific' 
    else:
        return 'Other'
    
customer_segmentation_address['state'] = customer_segmentation_address['state'].apply(get_state)

state_count = customer_segmentation_address['state'].value_counts().to_frame()
state_count

plt.rcParams["figure.figsize"] = (80, 52)
state_count.plot(kind='pie', y = 'state', autopct='%1.1f%%', legend = None)
plt.title('Customer Segmentation by State Address')
matplotlib.rcParams.update({'font.size': 20})
plt.savefig("customersegmentationbystate.jpg")
plt.show()

customer_activity_df2 = customer_activity_df.transpose()
plt.rcParams["figure.figsize"] = (8, 6)
customer_activity_df2 = customer_activity_df2.rename_axis('Transaction Month').reset_index()

customer_activity_df2.plot(x = 'Transaction Month', y=['Repeater', 'Inactive', 'Engaged'], kind = 'line')
plt.title('Customer Activity Per Month')
matplotlib.rcParams.update({'font.size': 8})

#age demographic
#generation 
customer_segmentation_age = modified_df.groupby(['name'], as_index=False).first()

birthyear = customer_segmentation_age['generation'] = [x[2][0:4] for x in np.array(customer_segmentation_age)]

def get_generation(birthyear):
    if birthyear in [str(birthyear) for birthyear in range(1901, 1925)]:
        return 'The Greatest Generation'
    elif birthyear in [str(birthyear) for birthyear in range(1925, 1946)]:
        return 'Silent Generation/Traditionalists'
    elif birthyear in [str(birthyear) for birthyear in range(1946, 1965)]:
        return 'Baby Boomers'
    elif birthyear in [str(birthyear) for birthyear in range(1965, 1981)]:
        return 'Generation X'
    elif birthyear in [str(birthyear) for birthyear in range(1981, 1997)]:
        return 'Millennials'
    elif birthyear in [str(birthyear) for birthyear in range(1997, 2013)]:
        return 'Generation Z' 
    elif birthyear in [str(birthyear) for birthyear in range(2013, 2025)]:
        return 'Generation Alpha'
    
customer_segmentation_age['generation'] = customer_segmentation_age['generation'].apply(get_generation)

generation_count = customer_segmentation_age['generation'].value_counts().to_frame()
plt.rcParams["figure.figsize"] = (50, 10)
generation_count.plot(kind='pie', y = 'generation', autopct='%1.1f%%', legend = None)
plt.savefig("customersegmentationbygeneration.jpg")
plt.title('Customer Segmentation by Generation')
plt.show()

#birthday promos
birthmonth = customer_segmentation_age['birth_month'] = [x[2][6] for x in np.array(customer_segmentation_age)]

def get_birthmonth(birthmonth):
    if birthmonth == '1':
        return 'January'
    elif birthmonth == '2':
        return 'February'
    elif birthmonth == '3':
        return 'March'
    elif birthmonth == '4':
        return 'April'
    elif birthmonth == '5':
        return 'May'
    else:
        return 'June'
    
customer_segmentation_age['birth_month'] = customer_segmentation_age['birth_month'].apply(get_birthmonth)
customer_segmentation_age

birthmonth_count = customer_segmentation_age['birth_month'].value_counts().to_frame()
birthmonth_count = birthmonth_count.reindex(transaction_month)
birthmonth_count

plt.rcParams["figure.figsize"] = (50, 10)
birthmonth_count.plot(kind='pie', y = 'birth_month', autopct='%1.1f%%', legend = None)
plt.title('Birth Months of Customers (Potentially for Future Birthday Promos and Loyalty Rewards)')
matplotlib.rcParams.update({'font.size': 10})
plt.savefig("customerbirthmonths.jpg")
plt.show()