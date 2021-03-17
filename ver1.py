import time, json
from selenium import webdriver
from db_conn import push_prod_data, push_prod_data2

# 19238134 , 19223561 , 19227166
category_no = '19238134'
def multi_cate(cateno):
    driver = webdriver.Chrome('chromedriver')
    driver.implicitly_wait(2)
    driver.get(f'http://prod.danawa.com/list/?cate={cateno}')
    time.sleep(1)
    driver.find_element_by_css_selector('#productListArea > div.prod_list_opts > div.view_opt > div.view_item.view_qnt > select > option[value="90"]').click()
    time.sleep(1)

    def next_page():
        next_page = driver.find_element_by_css_selector('.now_on').text
        next_page = int(next_page) + 1
        try:
            driver.find_element_by_css_selector(f'[onclick^="javascript:movePage({next_page}"]').click()
            time.sleep(1)
        except Exception as e:
            try:
                driver.find_element_by_css_selector('.nav_next').click()
                time.sleep(1)
            except:
                return True
        return False

    def start():
        time.sleep(1)
        cnt = 0
        for ele in driver.find_elements_by_css_selector('li[id^="productItem"]'):
            # cnt += 1
            # if cnt == 2:
            #     break
            pcode = ele.get_attribute('id')
            pcode = pcode.replace('productItem', '')
            try:
                ele.find_element_by_css_selector('.more_prod_pricelist a').click()
            except:
                pass

            href = ele.find_element_by_css_selector('[name="productName"]').get_attribute('href')
            thumb = ele.find_element_by_css_selector('.thumb_link').get_attribute('href')
            prod_name = ele.find_element_by_css_selector('[name="productName"]').text
            desc = ele.find_element_by_css_selector('.spec_list').text

            push_prod_data({
                'pcode': pcode,
                'thumb': thumb,
                'prod_name': prod_name,
                'desc': desc,
                'href': href
            })

            for prod_detail in ele.find_elements_by_css_selector('li[id^="productInfoDetail"]'):
                price = prod_detail.find_element_by_css_selector('p.price_sect a strong').text
                detail_href = prod_detail.find_element_by_css_selector('p.price_sect a').get_attribute('href')
                detail_pcode = detail_href.split('&')
                detail_pcode = detail_pcode[0].split('pcode=')
                detail_desc = prod_detail.find_element_by_css_selector('.memory_sect').text

                sp = detail_desc.split('\n')
                
                ext2 = ''
                if len(sp) > 1:
                    ext2 = sp[1]
                    
                ext1 = sp[0]
                if '1위' in ext1:
                    ext1 = ext1.replace('1위 ', '')
                elif '2위' in ext1:
                    ext1 = ext1.replace('2위 ', '')
                elif '원' in ext1:
                    ext3 = ext1
                    ext1 = ext2
                    ext2 = ext3

                
                push_prod_data2({
                    'parent_pcode': pcode,
                    'pcode': detail_pcode[1],
                    'price': price,
                    'href': detail_href,
                    'ext1': ext1,
                    'ext2': ext2,
                })

catelist = ['19238134' , '19223561' , '19227166']
for c in catelist:
    multi_cate(c)
    COUNT = 0
    while True:
        COUNT += 1
        start()
        print(COUNT)
        if next_page():
            break
    
    driver.quit()

