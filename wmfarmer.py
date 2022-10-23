from pandas.core import series
import streamlit as st
from scripts.wmmarket import get_items, get_item_info, get_item_orders
from scripts.core import get_item_price, get_warframe_price, get_weapon_price

st.set_page_config(page_title='Warframe Market Farmer', page_icon='👨‍🌾', layout="wide")

assets_url = "https://warframe.market/static/assets/"
item_url = "https://warframe.market/zh-hans/items/"

st.write("# Warframe Market Farmer! 👨‍🌾")

items = get_items()

# for url_name in items['items']['url_name'][:10]:
#     st.write(get_item_orders(url_name))

if items['time']=='failed':
    st.write(f"➖ ⏱️ **Get Items Failed** ➖ *️⃣ **Status Code: {items[items]}** ➖ 👨‍💼 **By: DEARFAD** ➖")
else:
    st.write(f"➖ ⏱️ **{items['time']}** ➖ *️⃣ **Total: {items['items'].shape[0]}** ➖ 👨‍💼 **By: DEARFAD** ➖")

search_col, empty_col, info_col = st.columns([5,1,8])

with search_col:
    input_name = st.text_input('模糊搜索：', '')
    search_result = items['items'][items['items']['item_name'].str.contains(input_name.strip(), case=False)]
    if search_result.empty:
        st.warning('未找到相关信息...')
        url_name = ''
    else:    
        selected_name = st.selectbox('已发现：', search_result['item_name'])
        url_name = search_result[search_result['item_name']==selected_name]['url_name'].values[0]

if url_name:
    item_info = get_item_info(url_name)
    item_orders = get_item_orders(url_name)
    item_price = get_item_price(item_orders['orders'])
    
    with info_col:
        st.write(f"#### **{item_info['info']['zh-hans']['item_name']}**")
        st.write(f"###### ![ducats](https://warframe.market/static/build/resources/images/icons/Ducats.b2f626d13cd31d84117a.png) **{item_info['info'].get('ducats', '0')}** - [WM]({item_url+url_name}) - [WIKI]({item_info['info']['zh-hans']['wiki_link']})")
        st.write(f"###### 最低卖价: {item_price['ingame_lowest_sell_platinum']}")
        st.write(f"###### 最高买价: {item_price['ingame_highest_buy_platinum']}")

warframe, weapon, mod = st.tabs(["战甲Prime", "武器Prime", "MOD"])

with warframe:
    warframe_price_df = get_warframe_price()
    col_1, col_2, col_3 = st.columns([1,1,1])
    with col_1:
        warframe_table = "|名 称|套 装|蓝 图|头 部|机 体|系 统|\n|:---:|:---:|:---:|:---:|:---:|:---:|\n"
        for index, row in warframe_price_df.iloc[:12,:].iterrows():
            price = f'|**{index.upper()}**|{row["set"]}|{row["blueprint"]}|{row["neuroptics"]}|{row["chassis"]}|{row["systems"]}|\n'
            warframe_table = warframe_table + price
        st.write(warframe_table)
    with col_2:
        warframe_table = "|名 称|套 装|蓝 图|头 部|机 体|系 统|\n|:---:|:---:|:---:|:---:|:---:|:---:|\n"
        for index, row in warframe_price_df.iloc[12:24,:].iterrows():
            price = f'|**{index.upper()}**|{row["set"]}|{row["blueprint"]}|{row["neuroptics"]}|{row["chassis"]}|{row["systems"]}|\n'
            warframe_table = warframe_table + price
        st.write(warframe_table)
    with col_3:
        warframe_table = "|名 称|套 装|蓝 图|头 部|机 体|系 统|\n|:---:|:---:|:---:|:---:|:---:|:---:|\n"
        for index, row in warframe_price_df.iloc[24:-1,:].iterrows():
            price = f'|**{index.upper()}**|{row["set"]}|{row["blueprint"]}|{row["neuroptics"]}|{row["chassis"]}|{row["systems"]}|\n'
            warframe_table = warframe_table + price
        warframe_table = warframe_table + f"| | | | |总计|{warframe_price_df.shape[0]}|\n" + f"| | | | |总计|{warframe_price_df.loc['time','set']}|\n"
        st.write(warframe_table)

with weapon:
    col_main_weapon, col_side_weapon, col_melee_weapon = st.columns([1,1,1])
    
    with col_main_weapon:
        st.write('##### 主武器')
        weapon_price_df = get_weapon_price()
        weapon_table = "|名 称|套 装|蓝 图|枪 机|枪 托|枪 管|\n|:---:|:---:|:---:|:---:|:---:|:---:|\n"
        for index, row in weapon_price_df.iterrows():
            price = f'|**{row["item_name"]}**|{row["set"]}|{row["blueprint"]}|{row["receiver"]}|{row["stock"]}|{row["barrel"]}|\n'
            weapon_table = weapon_table + price
        weapon_table = weapon_table + f"| | | | |总计|{weapon_price_df.shape[0]}|\n"
        st.write(weapon_table)

    with col_side_weapon:
        st.write("##### 副武器")

    with col_melee_weapon:
        st.write("##### 近战武器")