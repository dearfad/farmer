import streamlit as st
from page import item

st.set_page_config(page_title='Warframe Market Farmer', page_icon='👨‍🌾')


def main():
    pages = {
        '物品价格': item.page,
        # '战甲套装': warframe.page,
        # '噩梦收益': nightmare.page,
        # '虚空裂缝': relic.page
    }
    with st.sidebar:
        st.title('Warframe Market Farmer')
        page = st.radio("请选择：", pages.keys())
    pages[page]()


if __name__ == '__main__':
    main()
