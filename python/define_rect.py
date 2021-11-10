ocr_results_a4 = [
([[254, 672], [480, 672], [480, 704], [254, 704]], 'ПАМР.741124.019', 0.9209840963255891),
([[264, 665], [524, 665], [524, 698], [264, 698]], 'ПАМР.3о1412.043СБ', 0.2481112000128859),
([[264, 666], [524, 666], [524, 696], [264, 696]], 'ПАМР.301261 О2осБ', 0.2747373384551577),
([[344, 955], [645, 955], [645, 993], [344, 993]], 'ПАМР.468367.016', 0.9412317528958435),
([[340, 890], [639, 890], [639, 931], [340, 931]], 'ПАМР.745236.009', 0.8787894616416699),
([[343, 903], [641, 903], [641, 941], [343, 941]], 'ПАМР.7413з1.002', 0.47338336786187796),
([[347, 909], [691, 909], [691, 947], [347, 947]], 'ПАМР.301417.О21СБ', 0.26995769544141246)
]

ocr_results_a3 = [
([[844, 682], [1068, 682], [1068, 712], [844, 712]], 'ПАМР.732158.007', 0.8950809534422955),
([[851, 671], [1112, 671], [1112, 704], [851, 704]], 'ПАМР.301241.ОЗ5СБ', 0.18802888765520634),
([[1117, 904], [1463, 904], [1463, 948], [1117, 948]], 'ПАМР.468З12 ООЗСБ', 0.37974318950462166),
([[1119, 907], [1462, 907], [1462, 949], [1119, 949]], 'ПАМР.687253.019СБ', 0.5009714459285862),
([[870, 624], [1068, 624], [1068, 648], [870, 648]], 'ПАМР.468373.0О3э3.', 0.5280290548979031),

]

a4_left_top_x = []
a4_left_top_y = []
a4_right_bot_x = []
a4_right_bot_y = []

for i in range(len(ocr_results_a4)):
    a4_left_top_x.append(ocr_results_a4[i][0][0][0])
    a4_left_top_y.append(ocr_results_a4[i][0][0][1])
    a4_right_bot_x.append(ocr_results_a4[i][0][2][0])
    a4_right_bot_y.append(ocr_results_a4[i][0][2][1])

a4_left_top_x_min = min(a4_left_top_x)
a4_left_top_y_min = min(a4_left_top_y)
a4_right_bot_x_max = max(a4_right_bot_x)
a4_right_bot_y_max = max(a4_right_bot_y)

a4_res = [a4_left_top_x_min, a4_left_top_y_min, a4_right_bot_x_max, a4_right_bot_y_max]

a3_left_top_x = []
a3_left_top_y = []
a3_right_bot_x = []
a3_right_bot_y = []

for i in range(len(ocr_results_a3)):
    a3_left_top_x.append(ocr_results_a3[i][0][0][0])
    a3_left_top_y.append(ocr_results_a3[i][0][0][1])
    a3_right_bot_x.append(ocr_results_a3[i][0][2][0])
    a3_right_bot_y.append(ocr_results_a3[i][0][2][1])

a3_left_top_x_min = min(a3_left_top_x)
a3_left_top_y_min = min(a3_left_top_y)
a3_right_bot_x_max = max(a3_right_bot_x)
a3_right_bot_y_max = max(a3_right_bot_y)

a3_res = [a3_left_top_x_min, a3_left_top_y_min, a3_right_bot_x_max, a3_right_bot_y_max]

print('a4 res:', a4_res)
print('a3 res:', a3_res)
