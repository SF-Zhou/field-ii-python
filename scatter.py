import widgets


das_res = [(64, 0.98), (64, 1.87), (128, 0.81), (128, 1.20), (256, 0.78), (256, 0.88)]
rdas_res = [(64, 0.99), (64, 1.90), (128, 0.82), (128, 1.22), (256, 0.79), (256, 0.90)]

sa_res = [(64, 0.81), (64, 0.76), (128, 0.82), (128, 0.82), (256, 0.84), (256, 0.82)]
rsa_res = [(64, 0.80), (64, 0.75), (128, 0.80), (128, 0.82), (256, 0.82), (256, 0.82)]

das_con = [(64, 0.86), (64, 0.60), (128, 0.87), (128, 0.75), (256, 0.86), (256, 0.79)]
rdas_con = [(64, 0.86), (64, 0.63), (128, 0.87), (128, 0.78), (256, 0.87), (256, 0.82)]

sa_con = [(64, 0.82), (64, 0.79), (128, 0.83), (128, 0.85), (256, 0.80), (256, 0.83)]
rsa_con = [(64, 0.82), (64, 0.80), (128, 0.84), (128, 0.86), (256, 0.82), (256, 0.84)]

das_cpu = [(64, 6.9), (128, 32.8), (256, 125.1)]
das_arm = [(64, 52.9), (128, 210.4), (256, 610.5)]
das_fpga = [(64, 2.4), (128, None), (256, None)]

rdas_cpu = [(64, 5.3), (128, 21.3), (256, 80.5)]
rdas_arm = [(64, 37.9), (128, 151.1), (256, 608.7)]
rdas_fpga = [(64, 2.1), (128, None), (256, 33.6)]

# sa_cpu = [(64, ), (128, ), (256, )]
# sa_arm = [(64, ), (128, ), (256, )]
sa_fpga = [(64, 18.9), (128, None), (256, None)]

# rsa_cpu = [(64, ), (128, ), (256, )]
# rsa_arm = [(64, ), (128, ), (256, )]
rsa_fpga = [(64, 17.0), (128, 134.2), (256, None)]

final_result = []


def add_result(time_data: list, result_data: list, label: str):
    for tc, t in time_data:
        for rc, v in result_data:
            if tc == rc and t is not None:
                final_result.append((t, v, label))


add_result(das_cpu, das_res, 'das_cpu')
add_result(das_arm, das_res, 'das_arm')
add_result(das_fpga, das_res, 'das_fpga')
add_result(rdas_cpu, rdas_res, 'rdas_cpu')
add_result(rdas_arm, rdas_res, 'rdas_arm')
add_result(rdas_fpga, rdas_res, 'rdas_fpga')

add_result(sa_fpga, sa_res, 'sa_fpga')
add_result(rsa_fpga, rsa_res, 'rsa_fpga')

w = widgets.ScatterChart()
w.add_points(final_result)
w.label_y = '半峰全宽 / mm'
w.vertical_threshold = 1.0
w.process()
w.export_to_pdf('/t/scatter_res.pdf')


final_result = []
add_result(das_cpu, das_con, 'das_cpu')
add_result(das_arm, das_con, 'das_arm')
add_result(das_fpga, das_con, 'das_fpga')
add_result(rdas_cpu, rdas_con, 'rdas_cpu')
add_result(rdas_arm, rdas_con, 'rdas_arm')
add_result(rdas_fpga, rdas_con, 'rdas_fpga')

add_result(sa_fpga, sa_con, 'sa_fpga')
add_result(rsa_fpga, rsa_con, 'rsa_fpga')

w = widgets.ScatterChart()
w.add_points(final_result)
w.label_y = '对比度'
w.vertical_threshold = 0.80
w.vertical_like = 1
w.process()
w.export_to_pdf('/t/scatter_con.pdf')
