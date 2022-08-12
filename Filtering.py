class ACfilter:
    def __init__(self):
        self.visited = set()

    def filter1(self, row):
        if row["consumption"] > 2:
            return 1
        else:
            return 0

    def filter2(self, row, Tlow):
        if row["consumption"] > Tlow:
            return row["consumption"]
        else:
            return 0

    def duration(self, data, k):
        cur_length = 1
        while k + 1 < len(data) - 1 and data["consumption_th"][k + 1]:
            cur_length += 1
            k += 1

        return cur_length, k + 1

    def ACfiltering(self, data):
        data["Tlow"] = data.apply(lambda x: self.filter1(x), axis=1)

        data_sub = data[data["Tlow"] == 1]
        Tlow = max(2.5, 1 / (2 * len(data_sub)) * sum(data_sub["consumption"]))

        data["consumption_th"] = data.apply(lambda x: self.filter2(x, Tlow), axis=1)

        cur_position = 0
        T_seed = 15
        while cur_position <= len(data) - 1:
            if not data["consumption_th"][cur_position]:
                cur_position += 1
                continue

            cur_length, cur_position = self.duration(data, cur_position)
            if cur_length == 1:
                self.visited.add(cur_position - 1)
                break
            cur_position += 1

        prev_length, prev_position = cur_length, cur_position

        while cur_position <= len(data) - 1:
            if not data["consumption_th"][cur_position]:
                cur_position += 1
                continue

            cur_length, cur_position = self.duration(data, cur_position)
            if (
                cur_length <= 2.2 * prev_length
                and cur_position - cur_length - prev_position <= 3 * prev_length
                and cur_length <= 6
            ):
                for k in range(cur_position - cur_length, cur_position):
                    self.visited.add(k)
                prev_length, prev_position = cur_length, cur_position
            else:
                while cur_position <= len(data) - 1:
                    if not data["consumption_th"][cur_position]:
                        cur_position += 1
                        continue

                    cur_length, cur_position = self.duration(data, cur_position)
                    if cur_length == 1:
                        self.visited.add(cur_position - 1)
                        break
                    cur_position += 1
                prev_length, prev_position = cur_length, cur_position

        forward = [1] * len(data)
        for k in self.visited:
            forward[k] = 0

        data["forward"] = forward
        data = data.iloc[::-1]
        data.index = range(len(data))
        data["consumption_th"] = data.apply(lambda x: self.filter2(x, Tlow), axis=1)

        self.visited = set()
        cur_position = 0
        T_seed = 15
        while cur_position <= len(data) - 1:
            if not data["consumption_th"][cur_position]:
                cur_position += 1
                continue

            cur_length, cur_position = self.duration(data, cur_position)
            if cur_length == 1:
                self.visited.add(cur_position - 1)
                break
            cur_position += 1

        prev_length, prev_position = cur_length, cur_position

        while cur_position <= len(data) - 1:
            if not data["consumption_th"][cur_position]:
                cur_position += 1
                continue

            cur_length, cur_position = self.duration(data, cur_position)
            if (
                cur_length <= 2.2 * prev_length
                and cur_position - cur_length - prev_position <= 3 * prev_length
                and cur_length <= 6
            ):
                for k in range(cur_position - cur_length, cur_position):
                    self.visited.add(k)
                prev_length, prev_position = cur_length, cur_position
            else:
                while cur_position <= len(data) - 1:
                    if not data["consumption_th"][cur_position]:
                        cur_position += 1
                        continue
                    cur_length, cur_position = self.duration(data, cur_position)
                    if cur_length == 1:
                        self.visited.add(cur_position - 1)
                        break
                    cur_position += 1
                prev_length, prev_position = cur_length, cur_position

        backward = [1] * len(data)
        for k in self.visited:
            backward[k] = 0

        data["backward"] = backward
        data = data.iloc[::-1]
        data.index = range(len(data))

        return data
