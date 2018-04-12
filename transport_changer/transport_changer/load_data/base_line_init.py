

def lineInit(linearr, lineId, baseLine, linePoints):
    linePoints[lineId] = 0
    for line in linearr:
        for coords in line:
            lat, lng = coords
            x = [0.001, 0.000, -0.001, 0.000, 0.000]
            y = [0.000, 0.001, 0.000, -0.001, 0.000]
            for i in range(0, 4):
                key = (round(lat, 3) + x[i], round(lng, 3) + y[i])
                nums = baseLine.get(key, set())

                nums.add(lineId)

                baseLine[key] = nums

            linePoints[lineId] += 1