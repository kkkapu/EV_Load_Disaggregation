import numpy as np
from scipy.stats import norm


class Disaggregation_tool:
    def __init__(self):
        pass

    def charging_status(self, row, Rate_EST):
        if row["consumption_x"] > max(
            Rate_EST + row["base_load"], row["consumption_y"] + Rate_EST * 1 / 2
        ):
            return 1
        elif row["consumption_x"] < Rate_EST + row["base_load"]:
            return -1000
        else:
            return 0

    def change_point_status_start(self, row, Rate_EST):
        threshold1 = Rate_EST * 3 / 4
        threshold2 = Rate_EST * 3 / 4
        if 5 <= row["Month"] <= 10:
            if row["dif1"] > threshold1 or row["dif2"] > threshold1:
                return 1
            else:
                return 0
        else:
            if row["dif1"] > threshold2 or row["dif2"] > threshold2:
                return 1
            else:
                return 0

    def change_point_status_end(self, row, Rate_EST):
        threshold1 = Rate_EST * 3 / 4
        threshold2 = Rate_EST * 3 / 4
        if 5 <= row["Month"] <= 10:
            if row["dif1"] < -threshold1 or row["dif2"] < -threshold1:
                return -1
            else:
                return 0
        else:
            if row["dif1"] < -threshold2 or row["dif2"] < -threshold2:
                return -1
            else:
                return 0

    def ChargingDetection(self, data, start, end, mean, std, Rate_EST, dic):
        cnt = 1

        if (
            not data.iloc[start]["forward"] * data.iloc[start]["backward"]
            or (end - start) >= 24
        ):
            return False

        if start - end >= 3:
            threshold = 0.01 / (end - start)
        else:
            threshold = 0.01 / (end - start)

        for k in range(start, end):
            if not data.iloc[k]["forward"] * data.iloc[k]["backward"]:
                return False

            normal_load = data.iloc[k]["consumption_x"] - Rate_EST
            if (
                (norm.cdf(x=normal_load, loc=mean, scale=std) < threshold)
                or normal_load < data.iloc[k]["base_load"]
            ) and start <= k < end - 1:
                return False

            if (
                (
                    norm.cdf(
                        x=data.iloc[k]["consumption_x"] - Rate_EST / 2,
                        loc=mean,
                        scale=std,
                    )
                    < threshold
                )
                or data.iloc[k]["consumption_x"] - Rate_EST / 2
                < data.iloc[k]["base_load"]
            ) and k >= end - 1:
                return False

            if data.iloc[k]["higher"] == 1:
                cnt += 1
            elif data.iloc[k]["higher"] < 0 and k < end - 1:
                cnt += data.iloc[k]["higher"]
            else:
                cnt -= 2
            if cnt < 0:
                return False

        return True

    def estimation(self, Rate_EST, n, Charging_period, bound):
        estimate = []
        for i in range(n):
            if i in Charging_period:
                estimate.append(Rate_EST)
            elif i in bound:
                estimate.append(Rate_EST / 2)
            else:
                estimate.append(0)
        return estimate

    def distribution(self, data, start, end, visited):
        normal = []
        cur = start - 1
        while len(normal) <= 7:
            if cur - 1 not in visited:
                normal.append(data.iloc[cur - 1]["consumption_x"])
                cur -= 1
            else:
                cur -= 1
        cur = end + 1
        while len(normal) <= 15:
            if cur + 1 >= len(data):
                break
            if cur + 1 not in visited:
                normal.append(data.iloc[cur + 1]["consumption_x"])
                cur += 1
            else:
                cur += 1
        return np.mean(normal), np.std(normal)

    def consecutive_filter(self, candidate):
        delete = set()
        for i in range(len(candidate) - 2):
            if (
                candidate[i][1] + 2 == candidate[i + 1][0]
                or candidate[i][1] + 1 == candidate[i + 1][0]
            ):
                delete.add(i)
                delete.add(i + 1)
        candidate_filter = []
        for i in range(len(candidate)):
            if i not in delete:
                candidate_filter.append(candidate[i])

        return candidate_filter
