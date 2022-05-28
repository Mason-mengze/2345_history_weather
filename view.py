from pyecharts import options as opts
import pandas as pd
import numpy as np
from pyecharts.charts import WordCloud, Timeline, Bar, Map, Line
from pyecharts.globals import ThemeType
import config


def wordCloud(province):
    # 这里地区先写死
    df = pd.DataFrame(pd.read_csv(province +'.csv',  encoding='utf-8', parse_dates=True))
    df = df.dropna()                                        # 去空值
    df['最低温'] = df['最低温'].astype('int64')              # 转换 ['最低温]类型未int64
    df['日期'] = pd.to_datetime(df['日期']).dt.year         # 日期列只保留年份
    
    tl = Timeline(opts.InitOpts(bg_color='#FFF8D7', width='1500px', height='740px'))

    year_list = list(range(2011, 2023))

    for year in year_list:

        df_year = df.query('日期=={}'.format(str(year)))
        x_data = df_year['天气'].value_counts().index.tolist()
        y_data = df_year['天气'].value_counts().values.tolist()
        data_pair = [list(z) for z in zip(x_data, y_data)]

        wordCloud = (

            WordCloud(opts.InitOpts(bg_color='#FFF8D7', width='1510px', height='760px'))
            .add(series_name="天气词云分析", data_pair=data_pair, word_size_range=[10, 150],)
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="天气词云分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
                ),
                tooltip_opts=opts.TooltipOpts(is_show=True),
            )
            # .render_notebook()
        )
        tl.add(chart=wordCloud, time_point='{}年'.format(year))
        tl.add_schema(
        play_interval=3200,
        symbol_size=[10,10]
        )
    return tl.render_embed()

def tl_bar_max():
    year_list = list(range(2011, 2023))
    df_max_data = pd.DataFrame(columns=['日期', '最高温','最低温', '天气', '风力风向', '城市', '地区'])

    for csv_name in list(config.map.keys()):
        df = pd.read_csv(csv_name + '.csv', encoding='utf-8', parse_dates=True)   # 读取csv表
        df = df.dropna()
        df.loc[:, "地区"] = csv_name
        df['最低温'] = df['最低温'].astype('int64')
        df['日期'] = pd.to_datetime(df['日期']).dt.year  # 日期列只保留年份

        for year in year_list:
            df_year = df.query('日期=={}'.format(str(year)))
            df_max = df_year.query('最高温=={}'.format(df_year['最高温'].max())).iloc[:1]
            df_max_data = pd.concat([df_max_data, df_max])

    color_num = ['#D3D3D3','#EEE8AA','#FAF0E6','#FF0000','#006400','#B22222','#FAEBD7','#800000',\
                '#8FBC8F','#FFF0F5','#F0FFFF','#FF69B4','#778899','#C71585','#3CB371','#D8BFD8',\
                '#F0E68C','#FF00FF','#D2B48C','#8B008B','#FF4500','#BA55D3','#FFC0CB','#9932CC',\
                '#00FF7F','#8A2BE2','#FFEBCD','#7B68EE','#FFDAB9','#483D8B','#FFE4E1','#F8F8FF','#808080','#0000CD']

    N = 12
    color = [val for val in color_num for _ in range(N)]
    df_max_data['color'] = color
    
    tl = Timeline(opts.InitOpts(bg_color='#FFF8D7', width='1500px', height='740px'))
    for i in year_list:
        # ascending =是否升序排序，默认升序为True，降序则为False
        df_sub = df_max_data[df_max_data['日期'] == i].sort_values(by='最高温')
        province_list = list(df_sub['地区'])
        value_list = list(df_sub['最高温'])
        color_list = list(df_sub['color'])

        y = []
        for j in range(34):
            y.append(
                opts.BarItem(
                    name=province_list[j],
                    value=value_list[j],
                    itemstyle_opts=opts.ItemStyleOpts(color=color_list[j])
                )
            )
        bar = (
            Bar(init_opts=opts.InitOpts(bg_color='#FFF8D7', width='900px', height='500px', ))
            .add_xaxis(province_list)
            .add_yaxis('最高温度', y, bar_width=10, 
                        label_opts=opts.LabelOpts(position='right'), 
                        markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_='average')]),
                        markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max')])
                    )
            .reversal_axis()
            .set_global_opts(
                title_opts=opts.TitleOpts('各省/市最高温{}年'.format(i), 
                                            pos_left='10%'),
                legend_opts=opts.LegendOpts(pos_left='center'),
                xaxis_opts=opts.AxisOpts(
                    name='温度°C',
                    type_='value',
                    name_location='end',
                    name_textstyle_opts=opts.TextStyleOpts(
                        font_family='Times News Roma',
                        font_size=14,
                        color='red'
                    ),
                    min_=25,
                    max_=45,
                    interval=1,
                    axislabel_opts=opts.LabelOpts(
                        formatter='{value}',
                        font_size=14
                    )

                ),
                yaxis_opts = opts.AxisOpts(
                    name='地区',
                    # name_location='end',
                    #  坐标轴名称与轴线之间的距离。
                    name_gap=10,
                    axislabel_opts=opts.LabelOpts(
                        font_size=9,
                        interval=0
                    )
                )
            )
        )
        tl.add(chart=bar, time_point='{}年'.format(i))
        tl.add_schema(
        play_interval=1200,
        symbol_size=[10,10]
        )

    return tl.render_embed()


def tl_bar_min():
    year_list = list(range(2011, 2023))
    df_min_data = pd.DataFrame(columns=['日期', '最高温','最低温', '天气', '风力风向', '城市', '地区'])
    for csv_name in list(config.map.keys()):
        df = pd.read_csv(csv_name + '.csv', encoding='utf-8', parse_dates=True)   # 读取csv表
        df = df.dropna()
        df.loc[:, "地区"] = csv_name
        df['最低温'] = df['最低温'].astype('int64')
        df['日期'] = pd.to_datetime(df['日期']).dt.year  # 日期列只保留年份

        for year in year_list:

            df_year = df.query('日期=={}'.format(str(year)))
            df_min = df_year.query('最低温=={}'.format(df_year['最低温'].min())).iloc[:1]
            df_min_data = pd.concat([df_min_data, df_min])


    color_num = ['#D3D3D3','#EEE8AA','#FAF0E6','#FF0000','#006400','#B22222','#FAEBD7','#800000',\
                    '#8FBC8F','#FFF0F5','#F0FFFF','#FF69B4','#778899','#C71585','#3CB371','#D8BFD8',\
                    '#F0E68C','#FF00FF','#D2B48C','#8B008B','#FF4500','#BA55D3','#FFC0CB','#9932CC',\
                    '#00FF7F','#8A2BE2','#FFEBCD','#7B68EE','#FFDAB9','#483D8B','#FFE4E1','#F8F8FF','#808080','#0000CD']

    N = 12
    color = [val for val in color_num for _ in range(N)]
    df_min_data['color'] = color
    # df_min_data.head(5)

    tl = Timeline(opts.InitOpts(bg_color='#FFF8D7', width='1500px', height='740px'))
    for i in year_list:
        # ascending =是否升序排序，默认升序为True，降序则为False
        df_sub = df_min_data[df_min_data['日期'] == i].sort_values(by='最低温', ascending=False)
        province_list = list(df_sub['地区'])
        value_list = list(df_sub['最低温'])
        color_list = list(df_sub['color'])

        y = []
        for j in range(34):
            y.append(
                opts.BarItem(
                    name=province_list[j],
                    value=value_list[j],
                    itemstyle_opts=opts.ItemStyleOpts(color=color_list[j])
                )
            )
        bar = (
            Bar(init_opts=opts.InitOpts(bg_color='#FFF8D7', width='900px', height='500px', ))
            .add_xaxis(province_list)
            .add_yaxis('最低温度', y, bar_width=10, 
                        label_opts=opts.LabelOpts(position='right'), 
                        markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_='average')]),
                        markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min')])
                    )
            .reversal_axis()
            .set_global_opts(
                title_opts=opts.TitleOpts('各省/市最低温{}年'.format(i), 
                                            pos_left='10%'),
                legend_opts=opts.LegendOpts(pos_left='center'),
                xaxis_opts=opts.AxisOpts(
                    name='温度°C',
                    type_='value',
                    name_location='end',
                    name_textstyle_opts=opts.TextStyleOpts(
                        font_family='Times News Roma',
                        font_size=14,
                        color='red'
                    ),
                    min_=-45,
                    max_=15,
                    interval=5,
                    axislabel_opts=opts.LabelOpts(
                        formatter='{value}',
                        font_size=14
                    )

                ),
                yaxis_opts = opts.AxisOpts(
                    name='地区',
                    # name_location='end',
                    #  坐标轴名称与轴线之间的距离。
                    name_gap=10,
                    axislabel_opts=opts.LabelOpts(
                        font_size=9,
                        interval=0
                    )
                )
            )
        )
        tl.add(chart=bar, time_point='{}年'.format(i))
        tl.add_schema(
        play_interval=1200,
        symbol_size=[10,10]
        )

    return tl.render_embed()

    
def map_view():
    min_tem_list = []
    max_tem_list = []

    max_tem_mean_list = []
    min_tem_mean_list = []

    for csv_name in list(config.map.keys()):
        df = pd.read_csv(csv_name + '.csv', encoding='utf-8')   # 读取csv表
        df = df.dropna()                                        # 去空值
        df['最低温'] = df['最低温'].astype('int64')              # 转换 ['最低温]类型未int64
        min_tem = df['最低温'].min()                            # 求出[最低温]列中的最低温, 也就是每个省中2011-2022中最低温的天气
        max_tem = df['最高温'].max()                            # 同上 求[最高温]

        min_tem_mean = df['最低温'].mean()                      # 求出[最低温]的平均值
        max_tem_mean = df['最高温'].mean()                      # 同上 [最高温]

        min_tem_list.append(min_tem)                            # 将 [最低温]列中的最低温 加入列表
        max_tem_list.append(max_tem)                            # 同上 [最高温]

        min_tem_mean_list.append(min_tem_mean)                  # 将[最低温]的平均值加入列表
        max_tem_mean_list.append(max_tem_mean)                  # 同上 [最高温]加入列表

    mean_tem_list= np.mean([max_tem_mean_list,min_tem_mean_list],axis=0).tolist()   
    # dict_mean_tem =dict(zip(config.map.keys(), mean_tem_list))

    data_max = list(zip(config.map.keys(), map(int, max_tem_list)))
    data_min = list(zip(config.map.keys(), map(int, min_tem_list)))
    data_mean = list(zip(config.map.keys(), map(int, mean_tem_list)))

    # map_ = Map(init_opts=opts.InitOpts(bg_color='#FFF8D7', width='1080px', height='720px',page_title='地区气温分析' , theme=ThemeType.LIGHT))
    map_ = Map(init_opts=opts.InitOpts(bg_color='#FFF8D7', width='1500px', height='740px', page_title='地区气温分析'))


    map_.add(
        series_name='各省平均温度',
        data_pair= data_mean,
        maptype='china',
        zoom=1
    )
    map_.add(
        series_name='各省最高温度',
        data_pair= data_max,
        maptype='china',
        zoom=1,
        # is_roam= False,   #是否开启鼠标缩放和平移漫游。'scale'缩放

        is_selected = False
    )
    map_.add(
        series_name='各省最底温度',
        data_pair= data_min,
        maptype='china',
        zoom=1,
        is_selected = False
    )

    map_.set_global_opts(
        legend_opts = opts.LegendOpts(pos_left='center', selected_mode = 'single'),
        title_opts=opts.TitleOpts(
            title='2011-2022年各省份气温分布图',
            subtitle='数据来源：2345天气',
            pos_bottom='center',
            pos_top='5%'
        ),
        visualmap_opts=opts.VisualMapOpts(
            max_=43,
            min_=-45,
            range_color=['#CCFFFF', '#99FFCC' ,'#FFFFFF',  '#FFFF99','#FFCC99' ,'#FF9966', '#FF6666']
        )
    )
    return map_.render_embed()


def line_view(province):
    
    date_min_tem = []
    date_max_tem = []

    df = pd.read_csv(province  + '.csv', encoding='utf-8', parse_dates=True)   # 读取csv表
    df = df.dropna()
    df['最低温'] = df['最低温'].astype('int64')
    df['日期'] = pd.to_datetime(df['日期']).dt.strftime('%Y-%m')  # 日期列只保留年月
    date_list = sorted(list(set(df['日期'].values.tolist())))
    for date in date_list:
        min_tem = int(df[df['日期']== date]['最低温'].min())                            # 求出[最低温]列中的最低温, 也就是每个省中2011-2022中最低温的天气
        max_tem = int(df[df['日期']== date]['最高温'].max())                            # 同上 求[最高温]

        date_min_tem.append(min_tem)
        date_max_tem.append(max_tem)

    line = (

        Line(init_opts=opts.InitOpts(bg_color='#FFF8D7', width='1500px', height='740px'))
        .add_xaxis(date_list) #X轴
        .add_yaxis('最低温',date_min_tem, markline_opts=opts.MarkLineItem(type_='average')) #Y轴
        .add_yaxis('最高温',date_max_tem, markline_opts=opts.MarkLineItem(type_='average')) #Y轴
        .set_global_opts(

            legend_opts = opts.LegendOpts(pos_left='center', selected_mode = 'single'),
            title_opts=opts.TitleOpts(
                title="2011-2022年气温折线图"
            ),

            tooltip_opts=opts.TooltipOpts(
                is_show=True, 
                axis_pointer_type='cross'
                ),

            xaxis_opts=opts.AxisOpts(
                type_='time',
                name='时间',
                # type_='value',
                name_location='end',
                name_textstyle_opts=opts.TextStyleOpts(
                        font_family='Times News Roma',
                        font_size=14,
                        color='red'
                    ),

                max_interval = 3600 * 24 * 1000 * 275,
                axispointer_opts=opts.AxisPointerOpts(is_show=True, 
                                                        type_='shadow')),

            yaxis_opts=opts.AxisOpts(
                min_='dataMin',
                name='温度 ℃',
                name_textstyle_opts=opts.TextStyleOpts(
                        font_family='Times News Roma',
                        font_size=14,
                        color='red'
                    ),
                axislabel_opts=opts.LabelOpts(formatter='{value}°C')

            )) 
    )
    return line.render_embed()
