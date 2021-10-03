import re
import openpyxl
from datetime import datetime, timedelta
import time
import API1
# from API1 import user

# userId = '100000108975356'
# user = API1.user(userId).get_all()

class API2:
    def __init__(self, id):
        self.user = API1.user(id).get_all()
        self.id = id

    def BDS(self):
        bds_point = 0

        kw_thue = ["thuê nhà", "phòng trọ", "nhà trọ", "thuê phòng"]
        kw_low = ["nhà tái định cư", "nhà tập thể", "khu tập thể"]
        mn_low = ["mua", "bán", "giới thiệu", "tư vấn", "xây dựng", "thuê", "kỹ thuật", "quản lý", "thiết kế",
                  "bất động sản", "nội thất", "bđs"]
        kw_mid = ["chung cư", "tòa nhà", "cư dân", "dân cư"]
        mn_mid = ["cao cấp", "đắt tiền", "highend", "high-end", "high end", "vinhomes", "gardens", "royal city",
                  "time city", "times city", "goldmark", "keangnam"]
        kw_high = ["chung cư", "tòa nhà", "cư dân", "căn hộ"]
        kw_VIP = ["biệt thự"]
        # Todo: group bds

        group_point = 0
        count_thue_gr = 0
        count_low_gr = 0
        count_mid_gr = 0
        count_high_gr = 0
        count_VIP_gr = 0

        for group in self.user["infor_group"]:
            name = group["name"].lower()
            # description = group["description"].lower()
            for i in kw_thue:
                if i in name:
                    count_thue_gr += 1
                    break
            for i in kw_low:
                if i in name:
                    check = True
                    for j in mn_low:
                        if j in name:
                            check = False
                            break
                    if check: count_low_gr += 1
                    break
            for i in kw_mid:
                if i in name:
                    check = True
                    for j in (mn_mid + mn_low):
                        if j in name:
                            check = False
                            break
                    if check: count_mid_gr += 1
                    break
            for i in kw_high:
                if i in name:
                    check = True
                    for j in mn_low:
                        if j in name:
                            check = False
                            break
                    if check:
                        check = False
                        for j in mn_mid:
                            if j in name:
                                check = True
                                break
                    if check: count_high_gr += 1
                    break
            for i in kw_VIP:
                if i in name:
                    check = True
                    for j in mn_low:
                        if j in name:
                            check = False
                            break
                    if check: count_VIP_gr += 1
                    break

        if 1 <= count_VIP_gr <= 5:
            group_point = 100
        elif 1 <= count_high_gr <= 5:
            group_point = 80
        elif 1 <= count_mid_gr <= 5:
            group_point = 50
        elif 1 <= count_low_gr <= 5:
            group_point = 20
        elif count_thue_gr > 1:
            bds_point -= 30
        elif count_thue_gr == 1:
            bds_point -= 15
        # Todo: Page bds
        page_point = 0
        count_low_pg = 0
        count_mid_pg = 0
        count_high_pg = 0
        count_VIP_pg = 0

        for page in self.user["infor_page"]:
            name = page["name"].lower()
            description = page["description"].lower()
            for i in kw_low:
                if i in name:
                    check = True
                    for j in mn_low:
                        if j in name:
                            check = False
                            break
                    if check: count_low_pg += 1
                    break
            for i in kw_mid:
                if i in name:
                    check = True
                    for j in (mn_mid + mn_low):
                        if j in name:
                            check = False
                            break
                    if check: count_mid_pg += 1
                    break
            for i in kw_high:
                if i in name:
                    check = True
                    for j in mn_low:
                        if j in name:
                            check = False
                            break
                    if check:
                        check = False
                        for j in mn_mid:
                            if j in name:
                                check = True
                                break
                    if check: count_high_pg += 1
                    break
            for i in kw_VIP:
                if i in name:
                    check = True
                    for j in mn_low:
                        if j in name:
                            check = False
                            break
                    if check: count_VIP_pg += 1
                    break

        if 1 <= count_VIP_pg <= 5:
            page_point += 100
        elif 1 <= count_high_pg <= 5:
            page_point += 80
        elif 1 <= count_mid_pg <= 5:
            page_point = 50
        elif 1 <= count_low_pg <= 5:
            page_point = 20

        bds_point = bds_point + 0.85 * group_point + 0.25 * page_point
        return min(100, bds_point)

    def oto(self):
        oto_point = 0

        combine = ["hội", "xe", "club", "clb", "câu lạc bộ"]
        normal_brand = ["ford", "kia", "honda civic", "honda city", "chevrolet", "hyundai", "huyndai", "toyota",
                        "mítubishi", "mazda", "nissan", "matiz"]
        luxury_brand = ["audi", "mercedes", "bmw", "volkswagen", "porsche", "volvo", "mini cooper", "infiniti", "lexus",
                        "maserati"]
        super_brand = ["ferrari", "lamborghini", "mclaren", "bugatti", "aston martin", "roll royce"]
        # Todo: group oto
        group_point = 0
        count_normal_brand_gr = 0
        count_luxury_brand_gr = 0
        count_super_brand_gr = 0

        for group in self.user["infor_group"]:
            name = group["name"].lower()
            # description = group["description"].lower()
            for i in normal_brand:
                if i in name:
                    check = False
                    for j in combine:
                        if j in name:
                            check = True
                            break
                    if check: count_normal_brand_gr += 1
                    break
            for i in luxury_brand:
                if i in name:
                    check = True
                    for j in normal_brand:
                        if j in name:
                            check = False
                            break
                    if check:
                        check = False
                        for j in combine:
                            if j in name:
                                check = True
                                break
                    if check: count_luxury_brand_gr += 1
                    break
            for i in super_brand:
                if i in name:
                    check = True
                    for j in (luxury_brand + normal_brand):
                        if j in name:
                            check = False
                            break
                    if check:
                        check = False
                        for j in combine:
                            if j in name:
                                check = True
                                break
                    if check: count_super_brand_gr += 1
                    break

        if count_luxury_brand_gr >= 1: oto_point += 30 * 1.3
        if count_normal_brand_gr >= 1: group_point += 30 + 5 * min(4, (count_normal_brand_gr - 1))

        if count_super_brand_gr >= 1: oto_point += 30 / 1.3
        # Todo: page oto
        page_point = 0
        count_normal_brand_pg = 0
        count_luxury_brand_pg = 0
        count_super_brand_pg = 0

        for page in self.user["infor_page"]:
            name = page["name"].lower()
            # description = group["description"].lower()
            for i in normal_brand:
                if i in name:
                    check = False
                    for j in combine:
                        if j in name:
                            check = True
                            break
                    if check: count_normal_brand_pg += 1
                    break
            for i in luxury_brand:
                if i in name:
                    check = True
                    for j in normal_brand:
                        if j in name:
                            check = False
                            break
                    if check:
                        check = False
                        for j in combine:
                            if j in name:
                                check = True
                                break
                    if check: count_luxury_brand_pg += 1
                    break
            for i in super_brand:
                if i in name:
                    check = True
                    for j in (luxury_brand + normal_brand):
                        if j in name:
                            check = False
                            break
                    if check:
                        check = False
                        for j in combine:
                            if j in name:
                                check = True
                                break
                    if check: count_super_brand_pg += 1
                    break

        if count_luxury_brand_pg >= 1: oto_point += 5 * 1.3
        if count_normal_brand_pg >= 1: page_point += 5 + 3 * min(5, (count_normal_brand_pg - 1))
        if count_super_brand_pg >= 1: page_point = 5 / 1.3

        oto_point = oto_point + page_point + group_point
        return min(100, oto_point)

    def soThich(self):
        soThich_point = 0

        sport_point = 0
        gym_point = 0
        spa_point = 0
        sothichkhac_point = 0
        hanghieu_point = 0
        sansale_point = 0
        # Todo: keyword so thich
        golf_tennis_kw = ["clb", "câu lạc bộ", "hội", "chơi", "club"]
        gym_kw = ["gym", "yoga", "fitness", "thể hình"]
        sothich_gym_combine = ["đam mê", "yêu thích", "chia sẻ", "giao lưu", "hội", "kiến thức"]
        trungtam_gym_combine = ["phòng", "trung tâm", "CLB", "club"]
        trungtam_gym_mn = ["thiết bị", "dụng cụ", "hải phòng", "thanh lý", "thiết kế", "thuê", "lắp đặt", "phụ kiện"]
        spa_low_kw = ["spa", "thẩm mỹ viện", "academy", "clinic"]
        spa_high_kw = ["spa", "thẩm mỹ viện"]
        spa_high_combine_kw = ["saigon smile", "sài gòn smile", "La Vie en Rose", "thiên hà", "De L'Amour",
                               "The Summit",
                               "shi", "Amadora", "Anam QT", "Oanh Beauty", "zen", "lavender", "thu cúc", "tropic",
                               "ngân hà"]
        spa_mn = ["thiết bị", "dụng cụ", "kinh doanh", "mẫu", "đào tạo", "dạy nghề", "học", "tuyển dụng"]
        choihoa_kw = ["hoa lan", "lan rừng", "lan đột biến", "chơi lan", "lan hồ điệp", "hội lan", "cây cảnh",
                      "hoa cảnh",
                      "hoa cây cảnh", "cây kiểng"]
        xiga_kw = ["xì gà", "cigar"]
        cacanh_kw = ["thủy sinh", "cá cảnh", "cá lóc cảnh", "tép cảnh", "cá koi"]
        suutamtem_kw = ["sưu tầm tem", "sưu tập tem", "trao đổi tem", "tem cổ"]
        doco_kw = ["đồ cổ", "cổ vật", "tiền cổ", "tiền xưa"]
        hanghieu_kw = ['louis vuitton', 'gucci', 'hermes', 'prada', 'ralph lauren', 'burberry', 'versace', 'chanel',
                       'd&g',
                       'armani', 'dior', 'givenchy', 'fendi', 'yves saint laurent', 'bottega veneta', 'balenciaga',
                       'dolce & gabbana', 'rolex', 'tom ford', 'mcm', 'calvin klein']
        sansale_kw = ["săn sale", "thanh lý", "đồ 2nd", "đồ secondhand", "hàng thùng", "đồ cũ"]
        # Todo: cac param count
        count_golf_gr = 0
        count_golf_pg = 0
        count_tennis_gr = 0
        count_tennis_pg = 0
        count_sothich_gym_gr = 0
        count_sothich_gym_pg = 0
        count_trungtam_gym_gr = 0
        count_trungtam_gym_pg = 0
        count_high_spa_gr = 0
        count_high_spa_pg = 0
        count_low_spa_gr = 0
        count_low_spa_pg = 0
        check_choihoa = False
        check_xiga = False
        check_cacanh = False
        check_suutamtem = False
        check_doco = False
        count_sansale_gr = 0
        count_sansale_pg = 0
        # Todo: group so thich
        for group in self.user["infor_group"]:
            name = group["name"].lower()
            # description = group["description"].lower()
            for i in golf_tennis_kw:
                if i in name and "golf" in name:
                    count_golf_gr += 1
                    break
                elif i in name and "tennis" in name:
                    count_tennis_gr += 1
                    break
            for i in gym_kw:
                if i in name:
                    check = False
                    for j in sothich_gym_combine:
                        if j in name:
                            check = True
                            break
                    if check:
                        count_sothich_gym_gr += 1
                        break
                    else:
                        check = True
                        for j in trungtam_gym_mn:
                            if j in name:
                                check = False
                                break
                        if check:
                            check = False
                            for j in trungtam_gym_combine:
                                if j in name:
                                    check = True
                                    break
                        if check: count_trungtam_gym_gr += 1
                        break
            for i in spa_low_kw:
                if i in name:
                    check = False
                    for j in spa_high_combine_kw:
                        if j in name:
                            check = True
                            break
                    if check: count_high_spa_gr += 1
                    break
            for i in spa_high_kw:
                if i in name:
                    check = True
                    for j in (spa_mn + spa_high_kw):
                        if j in name:
                            check = False
                            break
                    if check: count_low_spa_gr += 1
                    break
            for i in choihoa_kw:
                if i in name:
                    check_choihoa = True
                    sothichkhac_point += 10
                    break
            for i in xiga_kw:
                if i in name:
                    check_xiga = True
                    sothichkhac_point += 10
                    break
            for i in cacanh_kw:
                if i in name:
                    check_cacanh = True
                    sothichkhac_point += 10
                    break
            for i in suutamtem_kw:
                if i in name:
                    check_suutamtem = True
                    sothichkhac_point += 10
                    break
            for i in doco_kw:
                if i in name:
                    check_doco = True
                    sothichkhac_point += 10
                    break
            for i in sansale_kw:
                if i in name:
                    count_sansale_gr += 1
                    break
        # Todo: page so thich
        for page in self.user["infor_page"]:
            name = page["name"].lower()
            # description = group["description"].lower()
            for i in golf_tennis_kw:
                if i in name and "golf" in name:
                    count_golf_pg += 1
                    break
                elif i in name and "tennis" in name:
                    count_tennis_pg += 1
                    break
            for i in gym_kw:
                if i in name:
                    check = False
                    for j in sothich_gym_combine:
                        if j in name:
                            check = True
                            break
                    if check:
                        count_sothich_gym_pg += 1
                        break
                    else:
                        check = True
                        for j in trungtam_gym_mn:
                            if j in name:
                                check = False
                                break
                        if check:
                            check = False
                            for j in trungtam_gym_combine:
                                if j in name:
                                    check = True
                                    break
                        if check: count_trungtam_gym_pg += 1
                        break
            for i in spa_low_kw:
                if i in name:
                    check = False
                    for j in spa_high_combine_kw:
                        if j in name:
                            check = True
                            break
                    if check: count_high_spa_pg += 1
                    break
            for i in spa_high_kw:
                if i in name:
                    check = True
                    for j in (spa_mn + spa_high_kw):
                        if j in name:
                            check = False
                            break
                    if check: count_low_spa_pg += 1
                    break
            if not check_choihoa:
                for i in choihoa_kw:
                    if i in name:
                        check_choihoa = True
                        sothichkhac_point += 10
                        break
            if not check_xiga:
                for i in xiga_kw:
                    if i in name:
                        check_xiga = True
                        sothichkhac_point += 10
                        break
            if not check_cacanh:
                for i in cacanh_kw:
                    if i in name:
                        check_cacanh = True
                        sothichkhac_point += 10
                        break
            if not check_suutamtem:
                for i in suutamtem_kw:
                    if i in name:
                        check_suutamtem = True
                        sothichkhac_point += 10
                        break
            if not check_doco:
                for i in doco_kw:
                    if i in name:
                        check_doco = True
                        sothichkhac_point += 10
                        break
            for i in hanghieu_kw:
                if i in name:
                    hanghieu_point += 5
                    break
            for i in sansale_kw:
                if i in name:
                    count_sansale_pg += 1
                    break
        # Todo: tinh diem so thich
        if count_golf_gr >= 1: sport_point += 30 + 5 * (count_golf_gr - 1)
        if count_golf_pg >= 1: sport_point += 5 + 5 * (count_golf_pg - 1)
        if count_tennis_gr >= 1: sport_point += 15 + 5 * (count_tennis_gr - 1)
        if count_tennis_pg >= 1: sport_point += 5 + 5 * (count_tennis_pg - 1)
        sport_point = min(sport_point, 50)
        if count_trungtam_gym_gr >= 1: gym_point += 15 + 5 * (count_trungtam_gym_gr - 1)
        if count_trungtam_gym_pg >= 1: gym_point += 5 + 5 * (count_trungtam_gym_pg - 1)
        if count_sothich_gym_gr >= 1: gym_point += 10 + 5 * (count_sothich_gym_gr - 1)
        if count_sothich_gym_pg >= 1: gym_point += 5 + 5 * (count_sothich_gym_pg - 1)
        gym_point = min(20, gym_point)
        if count_high_spa_gr >= 1: spa_point += 15 + 5 * (count_high_spa_gr - 1)
        if count_high_spa_pg >= 1: spa_point += 5 + 5 * (count_high_spa_pg - 1)
        if count_low_spa_gr >= 1: spa_point += 10 + 5 * (count_low_spa_gr - 1)
        if count_low_spa_pg >= 1: spa_point += 5 + 5 * (count_low_spa_pg - 1)
        spa_point = min(20, spa_point)
        sothichkhac_point = min(40, sothichkhac_point)
        hanghieu_point = min(40, hanghieu_point)
        if count_sansale_gr >= 1: sansale_point -= 10 + 5 * (count_sansale_gr - 1)
        if count_sansale_pg >= 1: sansale_point -= 10 + 5 * (count_sansale_pg - 1)
        sansale_point = max(-40, sansale_point)

        soThich_point = sport_point + gym_point + spa_point + sothichkhac_point + hanghieu_point + sansale_point
        return min(100, soThich_point)

    def checkin(self):
        total_point = 0

        checkin_point = 0
        dulich_point = 0
        # todo: keyword checkin
        dulich_mn = ["sinh viên", "lái xe", "cao đẳng", "xe", "vé", "cđ", "học viện", "sv", "du học", "hướng dẫn viên",
                     "công ty", "cty", "hiệp hội"]
        checkin_city_mn = ["trường", "bệnh viện", "nhà tang lễ", "siêu thị", "cửa hàng"]
        bar_kw = ["bar", "pub", "club", "lounge"]
        resort_kw = ["resort", "khu nghỉ dưỡng", "golf"]
        novisa_asia = ['brunei', 'cambodia', 'indonesia', 'laos', 'malaysia', 'myanmar', 'philippines', 'thailand',
                       'singapore', 'nepal', 'india', 'maldives', 'sri lanka', 'uae', 'iran', 'timor-leste']
        visa_asia = ['kazakhstan', 'kyrgyzstan', 'tajikistan', 'turkmenistan', 'uzbekistan', 'mongolia ', 'japan',
                     'north korea', 'china', 'taiwan', 'korea', 'afghanistan', 'bangladesh', 'bhutan', 'pakistan',
                     'armenia', 'azerbaijan', 'bahrain', 'cyprus', 'georgia', 'iraq', 'israel', 'jordan', 'kuwait',
                     'lebanon',
                     'oman', 'palestine', 'qatar', 'arab', 'yemen']
        country_other = ['estonia', 'danish', 'ireland', 'lithuania', 'finland', 'england', 'iceland', 'latavia',
                         'norway',
                         'sweden', 'moldova', 'poland', 'czech', 'russia', 'slovakia', 'belarus', 'bulgaria', 'hungary',
                         'romania', 'ukraine', 'austria', 'germany', 'liechtenstein', 'monaco', 'switzerland',
                         'belgium',
                         'netherlands', 'luxembourg', 'france', 'greece', 'andorra', 'bosnia', 'herzegovina',
                         'macedonia',
                         'montenegro', 'serbia', 'spain', 'italy', 'albania', 'portugal', 'croatia', 'malta', 'san',
                         'mariano', 'slovenia', 'vatican']
        # todo: count param
        count_dulich = 0

        # todo: group du lich
        for group in self.user["infor_group"]:
            name = group["name"].lower()
            description = group["description"].lower()
            if "du lịch" in name:
                check = True
                for j in dulich_mn:
                    if j in (name or description):
                        check = False
                        break
                if check: count_dulich += 1
        # todo: page du lich
        for page in self.user["infor_page"]:
            name = page["name"].lower()
            description = page["description"].lower()
            if "du lịch" in name:
                check = True
                for j in dulich_mn:
                    if j in (name or description):
                        check = False
                        break
                if check: count_dulich += 1
        # todo: checkin
        if self.user["infor"]["checkin"]:

            checkin_city_point = 0
            bar_point = 0
            resort_point = 0
            country_novisa_asia_point = 0
            country_visa_asia_point = 0
            country_other_point = 0

            city = list()
            city_set = set()
            bar_day = []
            resort_date = []
            resort_name = set()
            country_date_novisa_asia = []
            country_name_novisa_asia = set()
            country_date_visa_asia = []
            country_name_visa_asia = set()
            country_date_other = []
            country_name_other = set()

            count_bar = 0
            count_resort = 0
            count_country_novisa_asia = 0
            count_country_visa_asia = 0
            count_country_other = 0

            for checkin in self.user["infor"]["checkin"]:
                try:
                    create_day = checkin["createTime"].split(" ")[0]
                    if checkin["place"]["location"]["country"] == 'Vietnam' and checkin["place"]["location"][
                        "city"] not in (
                            self.user["infor"]["hometowns"] and self.user["infor"]["locations"]) and (
                            self.user["infor"]["hometowns"] or self.user["infor"]["locations"]):
                        check = True
                        for i in checkin_city_mn:
                            if i in checkin["place"]["name"].lower():
                                check = False
                                break
                        if check:
                            city.append(checkin["place"]["location"]["city"])
                            city_set.add(checkin["place"]["location"]["city"])

                    for i in bar_kw:
                        if i in checkin["place"]["name"].lower():
                            if {checkin["place"]["name"].lower(): create_day} not in bar_day:
                                bar_day.append({checkin["place"]["name"].lower(): create_day})
                                count_bar += 1
                            break
                    for i in resort_kw:
                        if i in checkin["place"]["name"]:
                            resort_date.append({checkin["place"]["name"].lower(): checkin["createTime"]})
                            resort_name.add(checkin["place"]["name"].lower())
                            break
                    if checkin["place"]["location"]["country"].lower() in novisa_asia:
                        country_date_novisa_asia.append(
                            {checkin["place"]["location"]["country"].lower(): checkin["createTime"]})
                        country_name_novisa_asia.add(checkin["place"]["location"]["country"].lower())
                    if checkin["place"]["location"]["country"].lower() in visa_asia:
                        country_date_visa_asia.append(
                            {checkin["place"]["location"]["country"].lower(): checkin["createTime"]})
                        country_name_visa_asia.add(checkin["place"]["location"]["country"].lower())
                    if checkin["place"]["location"]["country"].lower() in country_other:
                        country_date_other.append(
                            {checkin["place"]["location"]["country"].lower(): checkin["createTime"]})
                        country_name_other.add(checkin["place"]["location"]["country"].lower())
                except:
                    continue
            # todo: calculate second checkin
            # todo: checkin_city_point:
            for i in city_set:
                count = 0
                for j in city:
                    if i == j: count += 1
                if count < 6: checkin_city_point += 5
            if count_bar > 0: bar_point = 7 + 5 * (count_bar - 1)
            # todo: resort_point:
            for i in resort_name:
                count_resort += 1
                datetime_obj = []
                for j in resort_date:
                    try:
                        datetime_obj.append(datetime.strptime(j[i], '%d-%m-%Y %H:%M:%S'))
                    except:
                        continue
                if len(datetime_obj) == 1: continue
                datetime_obj = sorted(datetime_obj)
                for j in range(1, len(datetime_obj)):
                    if datetime_obj[j] - datetime_obj[j - 1] > timedelta(days=7):
                        count_resort += 1
            if count_resort > 0: resort_point = 10 + 5 * (count_resort - 1)
            # todo: no visa asia point
            for i in country_name_novisa_asia:
                count_country_novisa_asia += 1
                datetime_obj = []
                for j in country_date_novisa_asia:
                    try:
                        datetime_obj.append(datetime.strptime(j[i], '%d-%m-%Y %H:%M:%S'))
                    except:
                        continue
                if len(datetime_obj) == 1: continue
                datetime_obj = sorted(datetime_obj)
                for j in range(1, len(datetime_obj)):
                    if datetime_obj[j] - datetime_obj[j - 1] > timedelta(days=30):
                        count_country_novisa_asia += 1
            if count_country_novisa_asia > 0: country_novisa_asia_point = 15 + 10 * (count_country_novisa_asia - 1)
            # todo: visa asia point
            for i in country_name_visa_asia:
                count_country_visa_asia += 1
                datetime_obj = []
                for j in country_date_visa_asia:
                    try:
                        datetime_obj.append(datetime.strptime(j[i], '%d-%m-%Y %H:%M:%S'))
                    except:
                        continue
                if len(datetime_obj) == 1: continue
                datetime_obj = sorted(datetime_obj)
                for j in range(1, len(datetime_obj)):
                    if datetime_obj[j] - datetime_obj[j - 1] > timedelta(days=30):
                        count_country_visa_asia += 1
            if count_country_visa_asia > 0: country_visa_asia_point = 30 + 10 * (count_country_visa_asia - 1)
            # todo: other country point
            for i in country_name_other:
                count_country_other += 1
                datetime_obj = []
                for j in country_date_other:
                    try:
                        datetime_obj.append(datetime.strptime(j[i], '%d-%m-%Y %H:%M:%S'))
                    except:
                        continue
                if len(datetime_obj) == 1: continue
                datetime_obj = sorted(datetime_obj)
                for j in range(1, len(datetime_obj)):
                    if datetime_obj[j] - datetime_obj[j - 1] > timedelta(days=30):
                        count_country_other += 1
            if count_country_other > 0: country_other_point = 50 + 20 * (count_country_other - 1)

            checkin_point = checkin_city_point + bar_point + resort_point + country_novisa_asia_point + country_visa_asia_point + country_other_point
        # todo: tinh diem total checkin
        dulich_point = 5 * count_dulich
        checkin_point = checkin_point

        total_point = dulich_point + checkin_point
        return min(100, total_point)

    # for checkin in user["infor"]["checkin"]:
    #     print(checkin["place"]["location"]["city"])
    def taiChinh(self):
        total_point = 0

        baohiem_point = 0
        dautu_point = 0
        cobac_point = 0

        ban_bh = False
        # todo: keyword
        baohiem_kw = ['bảo hiểm', 'bao hiem', 'bảo_hiểm', 'bao_hiem', 'bảohiểm', 'baohiem', 'bảo hiểm y tế', 'bhyt',
                      'bh_y_te', 'bh_y_tế', 'bhytế', 'bhyte', 'bh y tế', 'bh y te', 'bảo hiểm nhân thọ', 'bhnt',
                      'bh_nhan_tho', 'bh_nhân_thọ', 'bhnhantho', 'bhnhânthọ', 'bh nhân thọ', 'bh nhan tho',
                      'bảo hiểm sức khỏe', 'bhsk', 'bh_sức_khỏe', 'bh_suc_khoe', 'bhsứckhỏe', 'bhsuckhoe',
                      'bh sức khỏe',
                      'bh suc khoe', 'bảo hiểm bệnh hiểm nghèo', 'bảo hiểm chăm sóc sức khỏe', 'bh benh hiem ngheo',
                      'bhbệnhhiểmnghèo', 'bh bệnh hiểm nghèo', 'bhchămsócsứckhỏe', 'bhchamsocsuckhoe',
                      'bh cham soc suc khoe', 'bh chăm sóc sức khỏe', 'bảo hiểm thân thể', 'bhtt', 'bh_thân_thể',
                      'bh_than_the', 'bh thân thể', 'bhthânthể', 'bhthanthe', 'bh than the', 'bảo hiểm xe cơ giới',
                      'bhxecơgiới', 'bh xe cơ giới', 'bhxecogioi', 'bảo hiểm ô tô', 'bhôtô', 'bh_o_to', 'bh_ô_tô',
                      'bhoto',
                      'bh ô tô', 'bh o to', 'bảo hiểm xe máy', 'bhxemáy', 'bhxemay', 'bh_xe_máy', 'bh_xe_may',
                      'bh xe máy',
                      'bh xe may', 'bảo hiểm xã hội', 'bhxh', 'bh_xã_hội', 'bh_xa_hoi', 'bhxãhội', 'bhxahoi',
                      'bh xã hội',
                      'bh xa hoi', 'bảo hiểm tài chính', 'bhtaichinh', 'bh tài chính', 'bh tai chinh',
                      'bảo hiểm kinh doanh', 'bhkinhdoanh', 'bh kinh doanh', 'bảo hiểm tai nạn', 'bh_tai_nạn',
                      'bh_tai_nan',
                      'bhtainạn', 'bhtainan', 'bảo hiểm tài sản', 'bh_tài_sản', 'bh_tai_san', 'bh tài sản',
                      'bh_tài_sản',
                      'bhtaisan', 'bh tai san', 'bảo hiểm nhà', 'bhnhà', 'bhnha', 'bh nhà', 'bảo hiểm tín dụng',
                      'bhtindung', 'bh_tin_dung', 'bh_tín_dụng', 'bh tín dụng', 'bh tin dung', 'bảo hiểm hàng không',
                      'bhhangkhong', 'bh hàng không', 'bh hang khong', 'bảo hiểm thương mại', 'bhthươngmại',
                      'bhthuongmai',
                      'bh_thuong_mai', 'bh_thương_mại', 'bh thương mại', 'bh thuong mai', 'bảo hiểm hàng hóa',
                      'bhhanghoa',
                      'bh hàng hóa', 'bh hang hoa', 'bảo hiểm thiệt hại', 'bhthiệthại', 'bhthiethai', 'bh thiệt hại',
                      'bh thiet hai', 'bhnongnghiep', 'bh nông nghiệp', 'bh nong nghiep', 'bảo hiểm phi nhân thọ',
                      'bhphinhantho', 'bhphinhânthọ', 'bh phi nhân thọ', 'bh phi nhan tho', 'bhpnt', 'bảo hiểm cháy nổ',
                      'bhchayno', 'bh cháy nổ', 'bảo hiểm tổng hợp', 'bhtổnghợp', 'bhtonghop']
        mustnot = ['mũ bảo hiểm', 'mu bao hiem', 'mubaohiem', 'mũ bh', 'mũbảohiểm', 'nón bảo hiểm', 'non bao hiem',
                   'mũ bh',
                   'mu bh', 'nón bh', 'non bh', 'đồ bảo hiểm', 'do bao hiem', 'đồ bh', 'do bh', 'tuyển dụng',
                   'tuyen dung',
                   'phỏng vấn', 'phong van', 'tuyển', 'truyện', 'mu bh', 'game', 'trò chơi', 'chiêu mộ', 'hủy hợp đồng',
                   'khách hàng']
        # todo: baohiem point
        for post in self.user["infor_post"]:
            message = post["message"].lower()
            for i in baohiem_kw:
                if i in message:
                    check = True
                    for j in mustnot:
                        if j in message:
                            check = False
                            break
                    if check:
                        ban_bh = True
                    break
            if ban_bh:
                baohiem_point = 10
                break
        # todo: dautu point
        if len(self.user["infor"]["prediction"]["investment"]) > 0:
            for i in self.user["infor"]["prediction"]["investment"]:
                if i["type"].lower() == ("chứng khoán" or "vàng"):
                    dautu_point += 25
                elif i["type"].lower() == "ngoại hối":
                    dautu_point += 30
                else:
                    dautu_point += 15
        # todo: cobac point
        if len(self.user["infor"]["prediction"]["interest"]) > 0:
            for i in self.user["infor"]["prediction"]["interest"]:
                if i["type"].lower() == "cờ bạc":
                    cobac_point = -50
                    break
        # todo: total
        total_point = baohiem_point + dautu_point + cobac_point
        return min(70, total_point)

    def caNhan(self):
        canhan_point = 0

        is_student = False
        is_nghehot = False
        is_timviec = False
        is_nhanuoc = False
        is_doanhnghiep = False
        is_daihocdiemcao = False
        # todo: keyword
        daihoc_kw = open("acronymUniversity.txt", encoding="utf-8")
        nghehot_kw = ["pilot", "phi công", "ngân hàng", "marketing", "developer", "lập trình viên", "tiếp viên",
                      "bất động sản", "bác sĩ", "doctor", "bác sỹ", "bệnh viện", "quản lý nhân sự"]
        nghehot_mn = ["chém gió", "bôn ba", "thất tình", "ăn hàng ở không", "ăn hàng-ở không", "chem gio", "bộ phận",
                      "hạ bộ", "đi bộ", "bộ trưởng"]
        nhanuoc_kw = ['đảng', 'nhà nước', 'cơ quan', 'tổng cục', 'ủy ban', 'ủy viên', 'tòa án', 'công an',
                      'mặt trận tổ quốc']
        doanhnghiep_kw = ['viễn thông quân đội', 'vingroup', 'viettel', 'dầu khí việt nam', 'điện lực việt nam',
                          'uniliver', 'masan', 'tân hiệp phát', 'doji', 'fpt', 'vietcombank', 'mbbank', 'bidv']
        daihocdiemcao_kw = ['đại học ngoại thương', 'ftu', 'đại học bách khoa hà nội', 'hust', 'đại học công nghệ',
                            'uet', 'đại học quốc gia hà nội', 'đại học y hà nội', 'đại học ngoại ngữ',
                            'đại học kinh tế', 'đại học hà nội', 'hanoi university',
                            'đại học khoa học xã hội và nhân văn']

        # todo: group
        for group in self.user["infor_group"]:
            for i in daihoc_kw:
                if i.strip() in group["name"].lower():
                    is_student = True
                    break
            if "tìm việc" in group["name"].lower():
                is_timviec = True
        # todo: page
        if not is_student:
            for page in self.user["infor_page"]:
                for i in daihoc_kw:
                    if i in page["name"].lower():
                        is_student = True
                        break
                if "tìm việc" in page["name"].lower():
                    is_timviec = True
        # todo: work
        if not is_student or self.user["infor"]["birthYear"] < 1999:
            for work in self.user["infor"]["works"]:
                for i in nghehot_kw:
                    if i in (work["employer"].lower() or work["position"].lower()):
                        check = True
                        for j in nghehot_mn:
                            if j in (work["employer"].lower() or work["position"].lower()):
                                check = False
                                break
                        if check:
                            is_nghehot = True
                        break
                for i in nhanuoc_kw:
                    if i in (work["employer"].lower() or work["position"].lower()):
                        check = True
                        for j in nghehot_mn:
                            if j in (work["employer"].lower() or work["position"].lower()):
                                check = False
                                break
                        if check:
                            is_nhanuoc = True
                        break
                for i in doanhnghiep_kw:
                    if i in (work["employer"].lower() or work["position"].lower()):
                        check = True
                        for j in nghehot_mn:
                            if j in (work["employer"].lower() or work["position"].lower()):
                                check = False
                                break
                        if check:
                            is_doanhnghiep = True
                        break
        # todo: education
        for edu in self.user["infor"]["educations"]:
            for i in daihocdiemcao_kw:
                if i in edu["school"].lower():
                    is_daihocdiemcao = True
                    break
        # todo: tính điểm
        if is_student:
            canhan_point += 10
        elif is_nghehot:
            canhan_point += 50
        elif is_timviec:
            canhan_point -= 50
        if is_nhanuoc:
            canhan_point += 10
        if is_doanhnghiep:
            canhan_point += 30
        if is_daihocdiemcao:
            canhan_point += 10
        return canhan_point
    def total_point(self):
        point = self.BDS() + self.oto() + self.soThich() + self.checkin() + self.taiChinh() + self.caNhan()
        print(str(self.BDS()) + " " +str(self.oto()) + " "+str(self.soThich()) + " "+str(self.checkin()) + " "+str(self.taiChinh()) + " "+str(self.caNhan()))
        return point


# todo: check 50 id
id = open("livingclass.txt", encoding="utf-8")
list_id = []
for i in id:
    list_id.append(i.strip())
total_time = 0
for i in list_id:
    print("id :" + i + "\n")
    start_time = time.time()
    user_point = API2(i).total_point()
    print("user point: " + str(user_point) + "\n")
    end_time = time.time() - start_time
    print("end time: " + str(end_time) + "\n")
    total_time += end_time
avg_time = total_time/len(id)
print("avg_time: " + str(avg_time))

# user_point1 = API2('583656387').total_point()
# print(user_point1)
# user_point2 = API2('1325800193').total_point()
# print(user_point2)
# user_point3 = API2('100001094332330').total_point()
# print(user_point3)
