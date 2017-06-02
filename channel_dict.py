import numpy as np

channel_dict = dict(board_0_channels=[7, 8, 9, 10, 11, 12, 42, 43, 44, 45, 46, 70, 71, 72, 73, 74, 93, 94, 95, 96,
                                      110, 111, 112, 122],
                    board_1_channels=[25, 26, 27, 28, 29, 30, 57, 58, 59, 60, 61, 82, 83, 84, 85, 86, 102, 103, 104,
                                      105, 116, 117, 118, 125],
                    board_2_channels=[13, 14, 15, 16, 17, 18, 47, 48, 49, 50, 51, 52, 75, 76, 77, 78, 79, 97, 98,
                                      99, 100, 113, 114, 123],
                    board_3_channels=[0, 31, 32, 33, 34, 35, 36, 37, 62, 63, 64, 65, 66, 67, 87, 88, 89, 90, 91,
                                      106, 107, 108, 119, 120],
                    board_4_channels=[19, 20, 21, 22, 23, 24, 53, 54, 55, 56, 80, 81, 101, 115, 124, 126],
                    board_5_channels=[1, 2, 3, 4, 5, 6, 38, 39, 40, 41, 68, 69, 92, 109, 121, 148],
                    board_6_channels=[127, 128, 129, 130, 131, 134, 135, 136, 137, 138, 139, 143, 144, 145,
                                      146, 147, 153, 154, 155, 156, 164, 165, 166, 176],
                    board_7_channels=[157, 158, 167, 168, 169, 177, 178, 179, 180, 181, 188, 189,
                                      190, 191, 192, 201, 202, 203, 204, 213, 214, 215, 224, 225],
                    board_8_channels=[132, 133, 140, 141, 142, 149, 150, 151, 152, 159, 160, 161, 162,
                                      163, 170, 171, 172, 173, 174, 175, 182, 183, 187, 193],
                    board_9_channels=[199, 200, 210, 211, 212, 220, 221, 222, 223, 229, 230, 231, 232, 233, 234,
                                      238, 239, 240, 241, 242, 244, 245, 246, 247],
                    board_10_channels=[184, 185, 186, 194, 195, 196, 197, 198, 205, 206, 207, 208, 209, 216,
                                       217, 218, 219, 226, 227, 228, 235, 236, 237, 243])

top_channels = channel_dict['board_0_channels'] + channel_dict['board_1_channels'] + \
                            channel_dict['board_2_channels'] + channel_dict['board_3_channels'] + \
                            channel_dict['board_4_channels'] + channel_dict['board_5_channels']

top_channels.remove(148)
channel_dict["top_channels"] = top_channels

bottom_channels = channel_dict['board_6_channels'] + channel_dict['board_7_channels'] + \
                               channel_dict['board_8_channels'] + channel_dict['board_9_channels'] + \
                               channel_dict['board_10_channels']
bottom_channels.append(148)
channel_dict["bottom_channels"] = bottom_channels

channel_dict["all_channels"] = top_channels+bottom_channels

channel_dict["top_outer_ring"] = list(np.arange(0, 36))

channel_dict["top_bulk"] = [ch for ch in channel_dict["top_channels"] if ch not in channel_dict["top_outer_ring"]]